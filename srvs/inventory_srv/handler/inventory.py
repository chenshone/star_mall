import grpc
from loguru import logger
import redis
from inventory_srv.proto import inventory_pb2, inventory_pb2_grpc
from google.protobuf import empty_pb2
from inventory_srv.model.models import Inventory
from inventory_srv.settings import settings
from common.lock.py_redis_lock import Lock


from peewee import DoesNotExist


class InventoryServicer(inventory_pb2_grpc.InventoryServicer):
    @logger.catch
    def Sell(self, request: inventory_pb2.SellInfo, context):
        # 扣减库存
        # 避免超卖问题，需要事务txn
        with settings.DB.atomic() as txn:
            for item in request.goodsInfo:
                lock = Lock(
                    settings.REDIS_CLIENT,
                    f"lock:goods_{item.goodsId}",
                    auto_renewal=True,
                    expire=10,
                )
                lock.acquire()
                try:
                    goods_inv = Inventory().get(Inventory.goods == item.goodsId)
                except DoesNotExist as e:
                    txn.rollback()  # 回滚事务
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    lock.release()
                    return empty_pb2.Empty()

                if goods_inv.stocks < item.num:
                    txn.rollback()  # 回滚事务
                    context.set_code(grpc.StatusCode.OUT_OF_RANGE)
                    context.set_details("库存不足")
                    lock.release()
                    return empty_pb2.Empty()
                else:
                    # TODO: 可能会引起数据不一致 - 分布式锁
                    goods_inv.stocks -= item.num
                    goods_inv.save()
                lock.release()

        return empty_pb2.Empty()

    @logger.catch
    def Reback(self, request: inventory_pb2.GoodsInvInfo, context):
        # 库存的归还， 有两种情况会归还： 1. 订单超时自动归还 2. 订单创建失败 ，需要归还之前的库存 3. 手动归还
        with settings.DB.atomic() as txn:
            for item in request.goodsInfo:
                # 查询库存
                try:
                    goods_inv = Inventory.get(Inventory.goods == item.goodsId)
                except DoesNotExist as e:
                    txn.rollback()  # 事务回滚
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return empty_pb2.Empty()

                # TODO 这里可能会引起数据不一致 - 分布式锁
                goods_inv.stocks += item.num
                goods_inv.save()

            return empty_pb2.Empty()

    @logger.catch
    def SetInv(self, request: inventory_pb2.GoodsInvInfo, context):
        force_insert = False
        invs = (
            Inventory()
            .select()
            .where(
                Inventory.goods == request.goodsId,
            )
        )
        if not invs:
            inv = Inventory()
            inv.goods = request.goodsId
            force_insert = True
        else:
            inv = invs[0]

        inv.stocks = request.num
        inv.save(force_insert=force_insert)

        return empty_pb2.Empty()

    @logger.catch
    def InvDetail(self, request: inventory_pb2.GoodsInvInfo, context):
        # 获取某个商品的库存详情
        try:
            inv = Inventory.get(Inventory.goods == request.goodsId)
            return inventory_pb2.GoodsInvInfo(goodsId=inv.goods, num=inv.stocks)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("没有库存记录")
            return inventory_pb2.GoodsInvInfo()
