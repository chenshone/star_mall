import grpc

from user_srv.proto import user_pb2_grpc, user_pb2


class UserTest:
    def __init__(self):
        channel = grpc.insecure_channel("127.0.0.1:50051")
        self.stub = user_pb2_grpc.UserStub(channel)

    def user_list(self):
        resp = self.stub.GetUserList(user_pb2.PageInfo(pn=2, pSize=2))
        print(resp.total)
        for user1 in resp.data:
            print(user1.mobile, user1.birthday)


if __name__ == '__main__':
    user = UserTest()
    user.user_list()
