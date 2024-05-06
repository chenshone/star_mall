# web服务端

## 技术选型
1. gin作为web框架
2. 日志选择zap
3. 配置库选择viper
4. 表单验证库选择github.com/go-playground/validator/v10
5. 手机验证码仅模拟，未接入短信平台，redis作为缓存，保存验证码
6. 图片验证码选择base64Captcha库
7. grpc作为rpc框架


## 生成grpc文件
``` bash
protoc --go_out=. --go_opt=paths=source_relative \
         --go-grpc_out=. --go-grpc_opt=paths=source_relative \
         user.proto
```

## 项目结构
    .
    ├── test 临时测试
    └── user-web user-web端
        ├── api 接口
        ├── config 配置结构
        ├── form 表单结构
        ├── global 全局配置
        │   └── response
        ├── initialize 初始化
        ├── middleware 中间件
        ├── model 数据库model
        ├── proto proto定义文件以及生成的go文件
        ├── router 路由
        ├── temp 临时测试
        ├── util 工具
        └── validator 验证器
