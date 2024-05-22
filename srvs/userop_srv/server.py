import argparse
from functools import partial
import logging
import os
import signal
import socket
import sys
from concurrent import futures
import uuid

import grpc
from loguru import logger


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from userop_srv.settings import settings


from userop_srv.proto import message_pb2, message_pb2_grpc
from userop_srv.proto import address_pb2, address_pb2_grpc
from userop_srv.proto import userfav_pb2, userfav_pb2_grpc


from userop_srv.handler.message import MessageServicer
from userop_srv.handler.address import AddressServicer
from userop_srv.handler.user_fav import UserFavServicer

from grpc_health.v1 import health, health_pb2, health_pb2_grpc

from common.register import consul


def on_exit(sig_no, frame, service_id):
    register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)

    logger.info(f"{service_id} 注销服务开始")
    register.deregister(service_id)
    logger.info(f"{service_id} 注销服务成功")

    sys.exit(0)


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    _, port = tcp.getsockname()
    tcp.close()
    return port


def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip", nargs="?", type=str, default="127.0.0.1", help="bind ip"
    )
    parser.add_argument("--port", nargs="?", type=int, default=0, help="bind port")

    args = parser.parse_args()

    if args.port == 0:
        args.port = get_free_tcp_port()

    logger.add("logs/userop_srv_{time}.log")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 注册服务
    message_pb2_grpc.add_MessageServicer_to_server(MessageServicer(), server)
    address_pb2_grpc.add_AddressServicer_to_server(AddressServicer(), server)
    userfav_pb2_grpc.add_UserFavServicer_to_server(UserFavServicer(), server)

    # 注册健康检查服务
    health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)

    server.add_insecure_port(f"{args.ip}:{args.port}")

    service_id = settings.SERVICE_NAME + str(uuid.uuid1())

    # 主进程退出信号监听
    signal.signal(signal.SIGINT, partial(on_exit, service_id=service_id))  # ctrl+c
    signal.signal(
        signal.SIGTERM,
        lambda sig_no, frame: on_exit(sig_no, frame, service_id=service_id),
    )  # kill

    logger.info(f"userop_srv start, listen on {args.ip}:{args.port}")
    server.start()

    logger.info("用户操作服务 注册开始")
    register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)

    if not register.register(
        name=settings.SERVICE_NAME,
        service_id=service_id,
        address=args.ip,
        port=args.port,
        tags=settings.SERVICE_TAGS,
    ):
        logger.error("用户操作服务 注册失败")
        sys.exit(1)

    logger.info("用户操作服务 注册成功")
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    settings.client.add_config_watcher(
        settings.NACOS["DataId"], settings.NACOS["Group"], settings.update_config
    )
    serve()
