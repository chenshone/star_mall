import json

import redis
import nacos
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
from loguru import logger


# 使用peewee的连接池， 使用ReconnectMixin来防止出现连接断开查询失败
class ReconnectMysqlDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass


NACOS = {
    "Host": "127.0.0.1",
    "Port": 8848,
    "NameSpace": "b288cf74-a88a-4596-9ff2-ed9604dd79fa",
    "DataId": "inventory-srv",
    "Group": "dev",
}

client = nacos.NacosClient(
    f'{NACOS["Host"]}:{NACOS["Port"]}',
    namespace=NACOS["NameSpace"],
)

# get config
data = client.get_config(NACOS["DataId"], NACOS["Group"])
data = json.loads(data)
logger.info(data)


def update_cfg(args):
    print("配置产生变化")
    print(args)


# consul的配置
CONSUL_HOST = data["consul"]["host"]
CONSUL_PORT = data["consul"]["port"]

# 服务相关的配置
SERVICE_NAME = data["name"]
SERVICE_TAGS = data["tags"]

ROCKETMQ_HOST = data["rocketmq"]["host"]
ROCKETMQ_PORT = data["rocketmq"]["port"]

REDIS_HOST = data["redis"]["host"]
REDIS_PORT = data["redis"]["port"]
REDIS_DB = data["redis"]["db"]

# 配置一个连接池
pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
REDIS_CLIENT = redis.StrictRedis(connection_pool=pool)

DB = ReconnectMysqlDatabase(
    data["mysql"]["db"],
    host=data["mysql"]["host"],
    port=data["mysql"]["port"],
    user=data["mysql"]["user"],
    password=data["mysql"]["password"],
)


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
