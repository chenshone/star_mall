import json
from loguru import logger
import nacos
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin


class ReconnectMysqlDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass


NACOS = {
    "Host": "127.0.0.1",
    "Port": 8848,
    "Namespace": "a14b099c-ec1d-45ba-82ff-ca73bab38852",
    "DataId": "user-srv",
    "Group": "dev",
}

client = nacos.NacosClient(
    f"{NACOS['Host']}:{NACOS['Port']}", namespace=NACOS["Namespace"]
)

data = client.get_config(NACOS["DataId"], NACOS["Group"])

data = json.loads(data)

logger.info(f"获取配置：{data}")


DB = ReconnectMysqlDatabase(
    data["mysql"]["db"],
    host=data["mysql"]["host"],
    port=data["mysql"]["port"],
    user=data["mysql"]["user"],
    password=data["mysql"]["password"],
)

# consul配置
CONSUL_HOST = data["consul"]["host"]
CONSUL_PORT = data["consul"]["port"]


# 服务相关配置
SERVICE_NAME = data["name"]
SERVICE_TAGS = data["tags"]


def update_config(args):
    try:
        args = json.loads(args["content"])
        logger.info("配置发生变化, 配置更新中...")
        # 更新数据库连接
        global DB
        DB = ReconnectMysqlDatabase(
            args["mysql"]["db"],
            host=args["mysql"]["host"],
            port=args["mysql"]["port"],
            user=args["mysql"]["user"],
            password=args["mysql"]["password"],
        )
        # 更新Consul配置
        global CONSUL_HOST, CONSUL_PORT
        CONSUL_HOST = args["consul"]["host"]
        CONSUL_PORT = args["consul"]["port"]

        # 更新服务相关配置
        global SERVICE_NAME, SERVICE_TAGS
        SERVICE_NAME = args["name"]
        SERVICE_TAGS = args["tags"]

        logger.info("配置更新完成")
    except Exception as e:
        logger.error(f"配置更新失败: {e}")
