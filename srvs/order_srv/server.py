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
from rocketmq.client import PushConsumer

from grpc_opentracing import open_tracing_server_interceptor
from jaeger_client import Config
from grpc_opentracing.grpcext import intercept_server


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from order_srv.settings import settings

from order_srv.handler import order

from order_srv.proto import order_pb2, order_pb2_grpc

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
    config = Config(
        config={  # usually read from some yaml config
            "sampler": {
                "type": "const",  # 全部
                "param": 1,  # 1 开启全部采样 0 表示关闭全部采样
            },
            "local_agent": {
                "reporting_host": "127.0.0.1",
                "reporting_port": "6831",
            },
            "logging": True,
        },
        service_name="order-srv",
        validate=True,
    )
    tracer = config.initialize_tracer()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip", nargs="?", type=str, default="127.0.0.1", help="bind ip"
    )
    parser.add_argument("--port", nargs="?", type=int, default=0, help="bind port")

    args = parser.parse_args()

    if args.port == 0:
        args.port = get_free_tcp_port()

    logger.add("logs/order_srv_{time}.log")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tracing_interceptor = open_tracing_server_interceptor(tracer)
    server = intercept_server(server, tracing_interceptor)

    # 注册订单服务
    order_pb2_grpc.add_OrderServicer_to_server(order.OrderServicer(), server)

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

    logger.info(f"order_srv start, listen on {args.ip}:{args.port}")
    server.start()

    logger.info("订单服务 注册开始")
    register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)

    if not register.register(
        name=settings.SERVICE_NAME,
        service_id=service_id,
        address=args.ip,
        port=args.port,
        tags=settings.SERVICE_TAGS,
    ):
        logger.error("订单服务 注册失败")
        sys.exit(1)

    logger.info("订单服务 注册成功")

    # 监听超时订单消息
    consumer = PushConsumer("star_mall_order")
    consumer.set_name_server_address(
        f"{settings.ROCKETMQ_HOST}:{settings.ROCKETMQ_PORT}"
    )
    consumer.subscribe("order_timeout", callback=order.order_timeout)
    consumer.start()

    server.wait_for_termination()
    consumer.shutdown()


if __name__ == "__main__":
    logging.basicConfig()
    settings.client.add_config_watcher(
        settings.NACOS["DataId"], settings.NACOS["Group"], settings.update_config
    )
    serve()
