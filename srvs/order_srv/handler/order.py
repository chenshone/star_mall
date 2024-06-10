import json
import time
import grpc
from loguru import logger

from peewee import DoesNotExist

from google.protobuf import empty_pb2

from rocketmq.client import (
    Producer,
    TransactionMQProducer,
    TransactionStatus,
    Message,
    SendStatus,
    ConsumeStatus
)

import opentracing


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


local_execute_dict = {}


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
        # 拿到拦截器中的span
        parent_span = context.get_active_span()
        local_execute_dict[parent_span.context.span_id] = parent_span
        # 先准备好一个half消息
        producer = TransactionMQProducer("star_mall", self.check_callback)
        producer.set_name_server_address(
            f"{settings.ROCKETMQ_HOST}:{settings.ROCKETMQ_PORT}"
        )
        producer.start()
        msg = Message("order_reback")
        msg.set_keys("star_mall")
        msg.set_tags("order")

        # 先生成好order_sn, 订单号作为local_execute_dict的key, 来分辨不同的消息
        order_sn = generate_order_sn(request.userId)
        msg_body = {
            "orderSn": order_sn,
            "userId": request.userId,
            "address": request.address,
            "name": request.name,
            "mobile": request.mobile,
            "post": request.post,
            "parent_span_id": parent_span.context.span_id,
        }
        msg.set_body(json.dumps(msg_body))

        ret = producer.send_message_in_transaction(
            msg, self.local_execute, user_args=None
        )
        logger.info(f"half消息发送成功: {ret.msg_id}, 发送状态: {ret.status}")

        if ret.status != SendStatus.SEND_OK:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details("新建订单失败")
            return order_pb2.OrderInfoResponse()

        # 此处直接往下执行，会导致各种问题，这里采取全局变量的形式将local_execute的执行结果传递给本地事务

        while True:
            if order_sn in local_execute_dict:
                context.set_code(local_execute_dict[order_sn]["code"])
                context.set_details(local_execute_dict[order_sn]["detail"])
                producer.shutdown()
                if local_execute_dict[order_sn]["code"] == grpc.StatusCode.OK:
                    return order_pb2.OrderInfoResponse(id=local_execute_dict[order_sn]["order"]["id"],
                                                       orderSn=local_execute_dict[order_sn]["order"]["orderSn"],
                                                       total=local_execute_dict[order_sn]["order"]["total"])
                else:
                    return order_pb2.OrderInfoResponse()
            time.sleep(0.1)

    @logger.catch
    def check_callback(self, msg):
        msg_body = json.loads(msg.body.decode("utf-8"))
        order_sn = msg_body["orderSn"]

        # 查询本地数据库 看一下order_sn的订单是否已经入库了
        orders = OrderInfo.select().where(OrderInfo.order_sn == order_sn)
        if orders:
            return TransactionStatus.ROLLBACK
        else:
            return TransactionStatus.COMMIT

    @logger.catch
    def local_execute(self, msg, user_args):
        msg_body = json.loads(msg.body.decode("utf-8"))
        order_sn = msg_body["orderSn"]
        local_execute_dict[order_sn] = {}

        parent_span =local_execute_dict[msg_body["parent_span_id"]]
        tracer = opentracing.global_tracer()

        with settings.DB.atomic() as txn:
            goods_ids = []
            goods_nums = {}
            order_goods_list = []
            goods_sell_info = []
            order_amount = 0
            # 获取购物车中已选中的商品
            with tracer.start_span("select_shopcart", child_of=parent_span) as select_shopcart_span:
                for cart_item in ShoppingCart.select().where(
                    ShoppingCart.user == msg_body["userId"],
                    ShoppingCart.checked == True,
                ):
                    goods_ids.append(cart_item.goods)
                    goods_nums[cart_item.goods] = cart_item.nums

                if not goods_ids:
                    """
                        {"order_sn":{
                            "code":"",
                            "detail":"",
                        }}
                    """
                    local_execute_dict[order_sn]["code"] = grpc.StatusCode.NOT_FOUND
                    local_execute_dict[order_sn]["detail"] = "购物车中没有选中的商品"
                    return TransactionStatus.ROLLBACK

            # 查询商品信息
            with tracer.start_span("query_goods", child_of=parent_span) as query_goods_span:
                register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)
                goods_srv_host, goods_srv_port = register.get_host_port(
                    f'Service == "{settings.GOODS_SRV_NAME}"'
                )
                if not goods_srv_host:
                    local_execute_dict[order_sn]["code"] = grpc.StatusCode.UNAVAILABLE
                    local_execute_dict[order_sn]["detail"] = "商品服务不可用"
                    return TransactionStatus.ROLLBACK

                goods_channel = grpc.insecure_channel(f"{goods_srv_host}:{goods_srv_port}")
                goods_stub = goods_pb2_grpc.GoodsStub(goods_channel)

                # 批量获取商品信息
                try:
                    goods_info_resp = goods_stub.BatchGetGoods(
                        goods_pb2.BatchGoodsIdInfo(id=goods_ids)
                    )
                except grpc.RpcError as e:
                    local_execute_dict[order_sn]["code"] = grpc.StatusCode.UNAVAILABLE
                    local_execute_dict[order_sn]["detail"] = f"商品服务不可用: {str(e)}"
                    return TransactionStatus.ROLLBACK

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
            with tracer.start_span("query_inv", child_of=parent_span) as query_inv_span:
                inventory_srv_host, inventory_srv_port = register.get_host_port(
                    f'Service == "{settings.INVENTORY_SRV_NAME}"'
                )
                if not inventory_srv_host:
                    local_execute_dict[order_sn]["code"] = grpc.StatusCode.UNAVAILABLE
                    local_execute_dict[order_sn]["detail"] = "库存服务不可用"
                    return TransactionStatus.ROLLBACK

                inventory_channel = grpc.insecure_channel(
                    f"{inventory_srv_host}:{inventory_srv_port}"
                )
                inventory_stub = inventory_pb2_grpc.InventoryStub(inventory_channel)

                try:
                    # 扣减库存如果失败，情况比较复杂
                    inventory_stub.Sell(inventory_pb2.SellInfo(goodsInfo=goods_sell_info, orderSn=order_sn))
                except grpc.RpcError as e:
                    local_execute_dict[order_sn]["code"] = grpc.StatusCode.INTERNAL
                    local_execute_dict[order_sn]["detail"] = f"扣减库存失败: {str(e)}"
                    err_code = e.code()
                    if err_code == grpc.StatusCode.UNKNOWN or err_code == grpc.StatusCode.DEADLINE_EXCEEDED:
                        # 未知错误或者服务超时，需要归还库存，发送归还库存消息
                        return TransactionStatus.COMMIT
                    else:
                        # 其他错误，不会发生库存扣减的情况，所以不需要归还库存
                        return TransactionStatus.ROLLBACK

                # 创建订单
                # 原本比较简单的逻辑应该是： 1. 本地开始half消息 - 扣减库存 2. 执行本地事务 3. 确定应该确认消息还是回滚消息
                # 1. 基于可靠消息的最终一致性 只确保自己发送出去的消息是可靠的， 不能确保消费者能正确的执行
                # 2. 积分服务 - 这里有一个隐含的点： 你的消费者必要保证能成功
                # 3. 但是库存服务比较特殊 - 库存是有限的 如果本地事务执行失败应该调用规划库存 - TCC ：1. 并发没有那么高 2. 很复杂
            with tracer.start_span("insert_order", child_of=parent_span) as insert_order_span:
                try:
                    order = OrderInfo()
                    order.order_sn = order_sn
                    order.order_mount = order_amount
                    order.address = msg_body["address"]
                    order.signer_name = msg_body["name"]
                    order.signer_mobile = msg_body["mobile"]
                    order.post = msg_body["post"]
                    order.user = msg_body["userId"]
                    order.save()

                    # 批量插入
                    for order_goods in order_goods_list:
                        order_goods.order = order.id
                    OrderGoods.bulk_create(order_goods_list)

                    # 删除购物车记录
                    ShoppingCart.delete().where(
                        ShoppingCart.user == msg_body["userId"], ShoppingCart.checked == True
                    ).execute()
                    local_execute_dict[order_sn] = {
                        "code": grpc.StatusCode.OK,
                        "detail": "订单创建成功",
                        "order": {
                            "id": order.id,
                            "order_sn": order_sn,
                            "total": order_amount
                        }
                    }

                    # 发送延时消息，订单超时可取消订单
                    msg = Message("order_timeout")
                    msg.set_delay_time_level(5) # 超时时间1分钟
                    msg.set_keys("star_mall")
                    msg.set_tags("cancel")
                    msg.set_body(json.dumps({"orderSn": order_sn}))
                    sync_producer = Producer("cancel") # 此处的groupid不能和之前的重复
                    sync_producer.set_name_server_address(f"{settings.ROCKETMQ_HOST}:{settings.ROCKETMQ_PORT}")
                    sync_producer.start()

                    ret = sync_producer.send_sync(msg)
                    if ret.status != SendStatus.OK:
                        raise Exception("发送延时消息失败")

                    print(f"发送时间: {datetime.now()}")
                    sync_producer.shutdown()

                except Exception as e:
                    """
                    调用库存归还接口的问题：
                        1. 在调用接口之前，程序出现了异常
                        2. 在调用接口之前非程序异常（比如物理问题，磁盘满了、断电宕机等），都可能会导致接口调用失败
                        3. 调用接口的时候网络出现抖动 - 幂等性机制

                    在扣减库存失败后, 发送一条rocketmq的可靠消息
                        事务消息：
                            1. 在扣减库存之前先准备好一个half消息
                            2. 如果库存扣减失败：
                                确认消息 -> 库存服务就可以确定归还库存
                            3. 如果库存扣减成功：
                                取消消息 -> 库存服务就可以确定库存扣减成功
                                但是，返回的时候网络出现抖动，导致超时机制认为这个调用失败
                                    确认消息 -> 库存服务就可以确定归还库存
                                        库存服务需要记录一下之前的订单是否已经归还
                            4. 扣减成功
                                1. 但是本地事务执行失败 -> 确认消息
                                2. 本地宕机：
                                    rocketmq就会启动回查机制:
                                        本地的回查业务: 通过消息中的订单号在本地查询数据库中是否有数据取消消息
                                    查询到没有数据:
                                        确认消息 -> 库存服务就可以确定归还库存
                    """
                    txn.rollback()
                    local_execute_dict[order_sn]["code"] = grpc.StatusCode.INTERNAL
                    local_execute_dict[order_sn]["detail"] = f"订单创建失败: {str(e)}"
                    return TransactionStatus.COMMIT

        return TransactionStatus.ROLLBACK


def generate_order_sn(user_id):
    # 当前时间+user_id+随机数
    from random import Random

    return f'{time.strftime("%Y%m%d%H%M%S")}{user_id}{Random().randint(10, 99)}'

def order_timeout(msg):
    msg_body_str = msg.body.decode("utf-8")
    print(f"超时消息接收时间: {datetime.now()}, 消息内容: {msg_body_str}")
    msg_body = json.loads(msg_body_str)
    order_sn = msg_body["orderSn"]

    # 查询订单
    with settings.DB.atomic() as txn:
        try:
            order = OrderInfo().get(OrderInfo.order_sn == order_sn)
            if order.status != "TRADE_SUCCESS":
                order.status = "TRADE_CLOSED"
                order.save()

                # 给库存服务发送归还库存的消息
                msg = Message("order_reback")
                msg.set_keys("star_mall")
                msg.set_tags("reback")
                msg.set_body(json.dumps({"orderSn": order_sn}))
                sync_producer = Producer("order_sender") # 此处的groupid不能和之前的重复
                sync_producer.set_name_server_address(f"{settings.ROCKETMQ_HOST}:{settings.ROCKETMQ_PORT}")
                sync_producer.start()

                ret = sync_producer.send_sync(msg)
                if ret.status != SendStatus.OK:
                    raise Exception("发送归还库存的消息失败")

                print(f"发送时间: {datetime.now()}")
                sync_producer.shutdown()
        except Exception as e:
            print(e)
            txn.rollback()
            return ConsumeStatus.RECONSUME_LATER

    return ConsumeStatus.CONSUME_SUCCESS


