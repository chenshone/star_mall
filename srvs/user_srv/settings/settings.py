from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin


class ReconnectMysqlDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass


MYSQL_DB = "star_mall_user_srv"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"

DB = ReconnectMysqlDatabase(
    MYSQL_DB, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD
)

# consul配置
CONSUL_HOST = "127.0.0.1"
CONSUL_PORT = 8500


# 服务相关配置
SERVICE_NAME = "user_srv"
SERVICE_TAGS = ["user_srv", "python", "srv"]
