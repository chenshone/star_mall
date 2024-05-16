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

from inventory_srv.settings import settings

from inventory_srv.handler import inventory

from inventory_srv.proto import inventory_pb2, inventory_pb2_grpc

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

    logger.add("logs/inventory_srv_{time}.log")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 注册商品服务
    inventory_pb2_grpc.add_InventoryServicer_to_server(
        inventory.InventoryServicer(), server
    )

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

    logger.info(f"inventory_srv start, listen on {args.ip}:{args.port}")
    server.start()

    logger.info("库存服务 注册开始")
    register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)

    if not register.register(
        name=settings.SERVICE_NAME,
        service_id=service_id,
        address=args.ip,
        port=args.port,
        tags=settings.SERVICE_TAGS,
    ):
        logger.error("库存服务 注册失败")
        sys.exit(1)

    logger.info("库存服务 注册成功")
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    settings.client.add_config_watcher(
        settings.NACOS["DataId"], settings.NACOS["Group"], settings.update_config
    )
    serve()
