import json
import pprint
import grpc
import consul

from google.protobuf import empty_pb2

import sys
import os

# 获取当前文件的父目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录路径（假设为父目录的父目录）
project_root = os.path.dirname(os.path.dirname(current_dir))
# 将项目根目录添加到模块搜索路径
sys.path.append(project_root)

from goods_srv.proto import goods_pb2, goods_pb2_grpc
from goods_srv.settings import settings


class GoodsTest:
    def __init__(self):
        # 连接grpc服务器
        c = consul.Consul(host="127.0.0.1", port=8500)
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
        self.goods_stub = goods_pb2_grpc.GoodsStub(channel)

    def goods_list(self):
        rsp: goods_pb2.GoodsListResponse = self.goods_stub.GoodsList(
            goods_pb2.GoodsFilterRequest(keyWords="电饭煲")
        )
        for item in rsp.data:
            print(item.name, item.shopPrice)

    def batch_get(self):
        ids = [1, 2]
        rsp: goods_pb2.GoodsListResponse = self.goods_stub.BatchGetGoods(
            goods_pb2.BatchGoodsIdInfo(id=ids)
        )
        for item in rsp.data:
            print(item.name, item.shopPrice)

    def get_detail(self, id):
        rsp = self.goods_stub.GetGoodsDetail(goods_pb2.GoodInfoRequest(id=id))
        print(rsp.name)

    def category_list(self):
        rsp = self.goods_stub.GetAllCategorysList(empty_pb2.Empty())
        data = json.loads(rsp.jsonData)
        pprint.pprint(data)


if __name__ == "__main__":
    goods = GoodsTest()
    # goods.goods_list()

    # goods.batch_get()
    # goods.get_detail(1)
    goods.category_list()
