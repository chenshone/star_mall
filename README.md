# star_mall

[web服务端](backend/README.md)

[rpc服务端](srvs/README.md)


## Tips
mall-master和online-store中需要python2以及node13


服务注册选择consul
```bash
docker run -d -p 8500:8500 -p 8301:8301 -p 8302:8302 -p 8600:8600/udp consul consul agent -dev -client=0.0.0.0
```

配置中心选择nacos
```bash
docker run --name nacos-standalone -e MODE=standalone -e JVM_XMS=512m -e JVM_XMX=512m -e JVM_XMN=256m -p 8848:8848 -d nacos/nacos-server:latest
```
