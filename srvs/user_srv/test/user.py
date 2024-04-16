import grpc

from user_srv.proto import user_pb2_grpc, user_pb2


class UserTest:
    def __init__(self):
        channel = grpc.insecure_channel("127.0.0.1:50051")
        self.stub = user_pb2_grpc.UserStub(channel)

    def getUserList(self):
        resp = self.stub.GetUserList(user_pb2.PageInfo(pn=2, pSize=2))
        print(resp.total)
        for user1 in resp.data:
            print(user1.mobile, user1.birthday)

    def getUserById(self, id):
        resp = self.stub.GetUserById(user_pb2.IdRequest(id=id))
        print(resp.mobile)

    def createUser(self, nickname, password, mobile):
        resp = self.stub.CreateUser(user_pb2.CreateUserInfo(nickname=nickname, password=password, mobile=mobile))

        print(resp.id)


if __name__ == '__main__':
    user = UserTest()
    # user.getUserList()
    # user.getUserById(100)
    
    user.createUser("test", "123456", "13812345678")
