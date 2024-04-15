import time

from loguru import logger

from user_srv.model.models import User
from user_srv.proto import user_pb2, user_pb2_grpc


class UserServicer(user_pb2_grpc.UserServicer):
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

            resp.data.append(user_info_resp)
        return resp
