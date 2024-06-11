# star_mall

[web服务端](backend/README.md)

[rpc服务端](srvs/README.md)


## Tips
mall-master和online-store中需要python2以及node13



## 技术选型

### 数据库选择mysql

### 缓存选择redis

### 服务注册选择consul
```bash
docker run -d -p 8500:8500 -p 8301:8301 -p 8302:8302 -p 8600:8600/udp consul consul agent -dev -client=0.0.0.0
```

### 配置中心选择nacos
```bash
docker run --name nacos-standalone -e MODE=standalone -e JVM_XMS=512m -e JVM_XMX=512m -e JVM_XMN=256m -p 8848:8848 -p 9848:9848 -p 9849:9849 -d nacos/nacos-server:latest
```

### 服务调用选择grpc

### 文件服务选择阿里云oss
采用阿里云oss提供的web前端直传的方式，即前端访问gin获取签名并携带callback，然后前端直传到oss，最后前端访问oss获取文件

### 消息队列选择rocketmq
> rocketmq选择docker构建
>
> 参考：[RocketMQ-Docker](https://github.com/apache/rocketmq-docker)


## 链路追踪选择jaeger
> docker run --rm --name jaeger -p6831:6831/udp -p16686:16686 jaegertracing/all-in-one:latest

## 流量控制，熔断限流选择sentinel
