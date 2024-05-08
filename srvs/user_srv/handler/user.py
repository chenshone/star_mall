import time
from datetime import date

import grpc
import peewee
from google.protobuf import empty_pb2
from loguru import logger
from passlib.hash import pbkdf2_sha256

from user_srv.model.models import User
from user_srv.proto import user_pb2, user_pb2_grpc


class UserServicer(user_pb2_grpc.UserServicer):

    def convertUser2Resp(self, user):
        # 将user的model对象转成message对象
        user_info_resp = user_pb2.UserInfoResponse()
        user_info_resp.id = user.id
        user_info_resp.password = user.password
        user_info_resp.mobile = user.mobile
        user_info_resp.role = user.role
        if user.nickname:
            user_info_resp.nickname = user.nickname
        if user.gender:
            user_info_resp.gender = user.gender
        if user.birthday:
            user_info_resp.birthday = int(time.mktime(user.birthday.timetuple()))

        return user_info_resp

    @logger.catch
    def GetUserList(self, request, context):
        resp = user_pb2.UserListResponse()
        users = User.select()
        resp.total = users.count()

        start = 0
        per_page_num = 10
        if request.pSize:
            per_page_num = request.pSize
        if request.pn:
            start = per_page_num * (request.pn - 1)

        users = users.limit(per_page_num).offset(start)

        for user in users:
            resp.data.append(self.convertUser2Resp(user))
        return resp

    @logger.catch
    def GetUserById(self, request, context):
        try:
            user = User.get(User.id == request.id)
            return self.convertUser2Resp(user)

        except peewee.DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return user_pb2.UserInfoResponse()

    @logger.catch
    def GetUserByMobile(self, request, context):
        try:
            user = User.get(User.mobile == request.mobile)
            return self.convertUser2Resp(user)
        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return user_pb2.UserInfoResponse()

    @logger.catch
    def CreateUser(self, request, context):
        try:
            _ = User.get(User.mobile == request.mobile)

            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("User already exists")
            return user_pb2.UserInfoResponse()
        except peewee.DoesNotExist:
            pass

        user = User()
        user.nickname = request.nickname
        user.mobile = request.mobile
        user.password = pbkdf2_sha256.hash(request.password)

        user.save()

        return self.convertUser2Resp(user)

    @logger.catch
    def UpdateUser(self, request, context):
        try:
            user = User.get(User.id == request.id)

            user.nickname = request.nickname
            user.gender = request.gender
            user.birthday = date.fromtimestamp(request.birthday)

            user.save()

            return empty_pb2.Empty()
        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return empty_pb2.Empty()

    @logger.catch
    def CheckPassword(self, request, context):
        return user_pb2.CheckResponse(
            success=pbkdf2_sha256.verify(request.password, request.encryptedPassword)
        )
