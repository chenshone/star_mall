import json
import grpc
import consul

from google.protobuf import empty_pb2

import sys

sys.path.insert(0, "/home/chenshone/stu/star_mall/srvs")

from inventory_srv.proto import inventory_pb2, inventory_pb2_grpc
from inventory_srv.settings import settings


class InventoryTest:
    def __init__(self):
        # 连接grpc服务器
        c = consul.Consul(host=settings.CONSUL_HOST, port=settings.CONSUL_PORT)
        services = c.agent.services()
        ip = ""
        port = ""
        for key, value in services.items():
            if value["Service"] == settings.SERVICE_NAME:
                ip = value["Address"]
                port = value["Port"]
                break
        if not ip:
            raise Exception()
        channel = grpc.insecure_channel(f"{ip}:{port}")
        self.inventory_stub = inventory_pb2_grpc.InventoryStub(channel)

    def set_inv(self):
        rsp = self.inventory_stub.SetInv(
            inventory_pb2.GoodsInvInfo(goodsId=10, num=110)
        )

    def get_inv(self):
        rsp = self.inventory_stub.InvDetail(inventory_pb2.GoodsInvInfo(goodsId=3))
        print(rsp)

    def sell(self):
        goods_list = [(1, 3), (3, 5)]
        request = inventory_pb2.SellInfo()
        for goodsId, num in goods_list:
            request.goodsInfo.append(
                inventory_pb2.GoodsInvInfo(goodsId=goodsId, num=num)
            )
        rsp = self.inventory_stub.Sell(request)

    def reback(self):
        goods_list = [(1, 3), (3, 5)]
        request = inventory_pb2.SellInfo()
        for goodsId, num in goods_list:
            request.goodsInfo.append(
                inventory_pb2.GoodsInvInfo(goodsId=goodsId, num=num)
            )
        rsp = self.inventory_stub.Reback(request)


if __name__ == "__main__":
    inv = InventoryTest()
    # inv.set_inv()
    # inv.get_inv()
    # inv.sell()
    inv.reback()
