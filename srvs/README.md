# rpc服务端

## 技术选型
1. peewee作为orm框架
2. passlib库加密、验证密码，可以自动加盐
3. grpc作为rpc框架
4. 日志选择loguru
5. 数据库使用mysql
6. grpc健康检查使用grpcio-health-checking库
7. py-consul库实现服务注册
8. 选择redis做分布式锁, 使用python-redis-lock库实现


## 生成grpc文件
```bash
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --pyi_out=. -I. user.proto
```

## 项目结构
    .
    ├── common 公共工具
    │   └── register 各种注册类
    ├── goods_srv goods_srv端
    │   ├── handler rpc接口实现
    │   ├── logs 日志
    │   ├── model 数据库模型
    │   ├── proto proto定义文件以及生成的py文件
    │   ├── settings 配置文件
    │   ├── sql mock数据
    │   └── test 测试文件
    └── user_srv user_srv端
        ├── handler rpc接口实现
        ├── logs 日志
        ├── model 数据库模型
        ├── proto proto定义文件以及生成的py文件
        └── settings 配置文件
