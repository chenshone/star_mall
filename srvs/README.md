orm库使用peewee

passlib库加密、验证密码，可以自动加盐

### 生成grpc文件

```bash
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. user.proto

```