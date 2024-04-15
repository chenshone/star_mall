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


def on_exit(sig_no, frame):
    logger.info("进程中断")
    sys.exit(0)


def serve():
    logger.add("logs/user_srv_{time}.log")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    server.add_insecure_port("[::]:50051")

    # 主进程退出信号监听
    signal.signal(signal.SIGINT, on_exit)  # ctrl+c
    signal.signal(signal.SIGTERM, on_exit)  # kill

    logger.info('User server is listening on port 50051...')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
