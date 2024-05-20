import time
import grpc
from loguru import logger

from peewee import DoesNotExist

from google.protobuf import empty_pb2

from order_srv.proto import (
    order_pb2_grpc,
    order_pb2,
    goods_pb2_grpc,
    goods_pb2,
    inventory_pb2_grpc,
    inventory_pb2,
)
from order_srv.model.models import *

from common.register import consul

from order_srv.settings import settings


class OrderServicer(order_pb2_grpc.OrderServicer):
    @logger.catch
    def CartItemList(self, request: order_pb2.UserInfo, context):
        # 获取购物车信息
        items = ShoppingCart.select().where(ShoppingCart.user == request.id)
        resp = order_pb2.CartItemListResponse(total=items.count())

        for item in items:
            item_resp = order_pb2.ShopCartInfoResponse()
            item_resp.id = item.id
            item_resp.userId = item.user
            item_resp.goodsId = item.goods
            item_resp.nums = item.nums
            item_resp.checked = item.checked

            resp.data.append(item_resp)

        return resp

    @logger.catch
    def CreateCartItem(self, request: order_pb2.CartItemRequest, context):
        # 添加商品到购物车
        existed_items = ShoppingCart.select().where(
            ShoppingCart.goods == request.goodsId,
            ShoppingCart.user == request.userId,
        )

        # 如果记录已经存在则合并购物车
        if existed_items:
            item = existed_items[0]
            item.nums += request.nums
        else:
            item = ShoppingCart()
            item.user = request.userId
            item.goods = request.goodsId
            item.nums = request.nums
        item.save()

        return order_pb2.ShopCartInfoResponse(id=item.id)

    @logger.catch
    def UpdateCartItem(self, request: order_pb2.CartItemRequest, context):
        # 更新购物车-数量和选中状态
        try:
            item = ShoppingCart.get(
                ShoppingCart.user == request.userId,
                ShoppingCart.goods == request.goodsId,
            )
            item.checked = request.checked
            if request.nums:
                item.nums = request.nums
            item.save()

        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("购物车记录不存在")

        finally:
            return empty_pb2.Empty()

    @logger.catch
    def DeleteCartItem(self, request: order_pb2.CartItemRequest, context):
        # 删除购物车记录
        try:
            item = ShoppingCart.get(
                ShoppingCart.user == request.userId,
                ShoppingCart.goods == request.goodsId,
            )
            item.delete_instance()

        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("购物车记录不存在")

        finally:
            return empty_pb2.Empty()

    @logger.catch
    def OrderList(self, request: order_pb2.OrderFilterRequest, context):
        orders = OrderInfo.select()
        if request.userId:
            orders = orders.where(OrderInfo.user == request.userId)

        resp = order_pb2.OrderListResponse(total=orders.count())

        # 分页
        per_page_num = request.pagePerNums if request.pagePerNums else 10
        start = per_page_num * (request.pages - 1) if request.pages else 0

        orders = orders.limit(per_page_num).offset(start)

        for order in orders:
            order_resp = order_pb2.OrderInfoResponse()
            order_resp.id = order.id
            order_resp.userId = order.user
            order_resp.orderSn = order.order_sn
            order_resp.payType = order.pay_type
            order_resp.status = order.status
            order_resp.post = order.post
            order_resp.total = order.order_mount
            order_resp.address = order.address
            order_resp.name = order.signer_name
            order_resp.mobile = order.signer_mobile
            order_resp.addTime = order.add_time.strftime("%Y-%m-%d %H:%M:%S")

            resp.data.append(order_resp)

        return resp

    @logger.catch
    def OrderDetail(self, request: order_pb2.OrderRequest, context):
        # 订单详情
        resp = order_pb2.OrderInfoDetailResponse()

        try:
            if request.userId:
                order = OrderInfo.get(
                    OrderInfo.id == request.id, OrderInfo.user == request.userId
                )
            else:
                order = OrderInfo.get(OrderInfo.id == request.id)

            resp.orderInfo.id = order.id
            resp.orderInfo.userId = order.user
            resp.orderInfo.orderSn = order.order_sn
            resp.orderInfo.payType = order.pay_type
            resp.orderInfo.status = order.status
            resp.orderInfo.post = order.post
            resp.orderInfo.total = order.order_mount
            resp.orderInfo.address = order.address
            resp.orderInfo.name = order.signer_name
            resp.orderInfo.mobile = order.signer_mobile

            order_goods = OrderGoods.select().where(OrderGoods.order == order.id)
            for order_good in order_goods:
                order_goods_resp = order_pb2.OrderItemResponse()

                order_goods_resp.goodsId = order_good.goods
                order_goods_resp.goodsName = order_good.goods_name
                order_goods_resp.goodsImage = order_good.goods_image
                order_goods_resp.goodsPrice = float(order_good.goods_price)
                order_goods_resp.nums = order_good.nums

                resp.data.append(order_goods_resp)

        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("订单不存在")

        finally:
            return resp

    @logger.catch
    def UpdateOrderStatus(self, request: order_pb2.OrderStatus, context):
        # 更新订单的支付状态
        OrderInfo.update(status=request.status).where(
            OrderInfo.order_sn == request.orderSn
        ).execute()
        return empty_pb2.Empty()

    @logger.catch
    def CreateOrder(self, request: order_pb2.OrderRequest, context):
        """
        新建订单
            1. 价格 - 访问商品服务
            2. 库存的扣减 - 访问库存服务
            3. 订单基本信息表 - 订单的商品信息表
            4. 从购物车中获取到选中的商品
            5. 从购物车中删除已购买的商品
        """
        with settings.DB.atomic() as txn:
            goods_ids = []
            goods_nums = {}
            order_goods_list = []
            goods_sell_info = []
            order_amount = 0
            # 获取购物车中已选中的商品
            for cart_item in ShoppingCart.select().where(
                ShoppingCart.user == request.userId,
                ShoppingCart.checked == True,
            ):
                goods_ids.append(cart_item.goods)
                goods_nums[cart_item.goods] = cart_item.nums

            if not goods_ids:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("购物车中没有选中的商品")
                return order_pb2.OrderInfoResponse()

            # 查询商品信息
            register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)
            goods_srv_host, goods_srv_port = register.get_host_port(
                f'Service == "{settings.GOODS_SRV_NAME}"'
            )
            if not goods_srv_host:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details("商品服务不可用")
                return order_pb2.OrderInfoResponse()

            goods_channel = grpc.insecure_channel(f"{goods_srv_host}:{goods_srv_port}")
            goods_stub = goods_pb2_grpc.GoodsStub(goods_channel)

            # 批量获取商品信息
            try:
                goods_info_resp = goods_stub.BatchGetGoods(
                    goods_pb2.BatchGoodsIdInfo(id=goods_ids)
                )
            except grpc.RpcError as e:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details(f"商品服务不可用: {str(e)}")
                return order_pb2.OrderInfoResponse()

            for goods_info in goods_info_resp.data:
                order_amount += goods_info.shopPrice * goods_nums[goods_info.id]

                order_goods = OrderGoods(
                    goods=goods_info.id,
                    goods_name=goods_info.name,
                    goods_image=goods_info.goodsFrontImage,
                    goods_price=goods_info.shopPrice,
                    nums=goods_nums[goods_info.id],
                )

                order_goods_list.append(order_goods)
                goods_sell_info.append(
                    inventory_pb2.GoodsInvInfo(
                        goodsId=goods_info.id, num=goods_nums[goods_info.id]
                    )
                )
            # 扣减库存
            inventory_srv_host, inventory_srv_port = register.get_host_port(
                f'Service == "{settings.INVENTORY_SRV_NAME}"'
            )
            if not inventory_srv_host:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details("库存服务不可用")
                return order_pb2.OrderInfoResponse()

            inventory_channel = grpc.insecure_channel(
                f"{inventory_srv_host}:{inventory_srv_port}"
            )
            inventory_stub = inventory_pb2_grpc.InventoryStub(inventory_channel)

            try:
                inventory_stub.Sell(inventory_pb2.SellInfo(goodsInfo=goods_sell_info))
            except grpc.RpcError as e:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"扣减库存失败: {str(e)}")
                return order_pb2.OrderInfoResponse()

            # 创建订单
            try:
                order = OrderInfo()
                order.order_sn = generate_order_sn(request.userId)
                order.order_mount = order_amount
                order.address = request.address
                order.signer_name = request.name
                order.signer_mobile = request.mobile
                order.post = request.post
                order.user = request.userId
                order.save()

                # 批量插入
                for order_goods in order_goods_list:
                    order_goods.order = order.id
                OrderGoods.bulk_create(order_goods_list)

                # 删除购物车记录
                ShoppingCart.delete().where(
                    ShoppingCart.user == request.userId, ShoppingCart.checked == True
                ).execute()

            except Exception as e:
                txn.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"订单创建失败: {str(e)}")
                return order_pb2.OrderInfoResponse()

            return order_pb2.OrderInfoResponse(
                id=order.id, orderSn=order.order_sn, total=order_amount
            )


def generate_order_sn(user_id):
    # 当前时间+user_id+随机数
    from random import Random

    return f'{time.strftime("%Y%m%d%H%M%S")}{user_id}{Random().randint(10, 99)}'
