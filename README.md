# star_mall

[web服务端](backend/README.md)

[rpc服务端](srvs/README.md)


## Tips
mall-master和online-store中需要python2以及node13


服务注册选择consul
```bash
docker run -d -p 8500:8500 -p 8301:8301 -p 8302:8302 -p 8600:8600/udp consul consul agent -dev -client=0.0.0.0
```
