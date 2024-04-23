import argparse
import logging
import os
import signal
import sys
from concurrent import futures

import grpc
from loguru import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from user_srv.handler.user import UserServicer
from user_srv.proto import user_pb2_grpc

# from grpc_health.v1 import health, health_pb2, health_pb2_grpc

from common.grpc_health.v1 import health_pb2_grpc, health_pb2
from common.grpc_health.v1 import health


def on_exit(sig_no, frame):
    logger.info("进程中断")
    sys.exit(0)


def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", nargs="?", type=str, default="127.0.0.1", help="bind ip")
    parser.add_argument("--port", nargs="?", type=int, default=50051, help="bind port")

    args = parser.parse_args()

    logger.add("logs/user_srv_{time}.log")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 注册用户服务
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)

    # 注册健康检查服务
    health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(),server)
    # health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)
    # configure_health_server(server, "user_srv")

    server.add_insecure_port(f"{args.ip}:{args.port}")

    # 主进程退出信号监听
    signal.signal(signal.SIGINT, on_exit)  # ctrl+c
    signal.signal(signal.SIGTERM, on_exit)  # kill

    logger.info(f'user_srv start, listen on {args.ip}:{args.port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
