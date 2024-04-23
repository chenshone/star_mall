# star_mall


## Tips
mall-master和online-store中需要python2以及node13


peewee作为orm框架，gin作为web框架，redis作为缓存，mysql作为数据库

python日志选择loguru, go日志选择zap

gin配置库选择viper

用户认证选择jwt

表单验证库选择github.com/go-playground/validator/v10

手机验证码仅模拟，未接入短信平台，redis作为缓存，保存验证码

图片验证码选择base64Captcha库

服务注册选择consul
```bash
docker run -d -p 8500:8500 -p 8301:8301 -p 8302:8302 -p 8600:8600/udp consul consul agent -dev -client=0.0.0.0
```
python配置grpc健康检查使用grpcio-health-checking库

使用py-consul库实现服务注册
