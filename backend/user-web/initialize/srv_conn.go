package initialize

import (
	"fmt"
	"star_mall_api/user-web/global"
	"star_mall_api/user-web/proto"

	"github.com/hashicorp/consul/api"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func InitSrvConn() {
	// 从注册中心获取用户服务信息
	cfg := api.DefaultConfig()
	cfg.Address = fmt.Sprintf("%s:%d", global.ServerConfig.ConsulInfo.Host, global.ServerConfig.ConsulInfo.Port)

	client, err := api.NewClient(cfg)
	if err != nil {
		panic(err)
	}

	data, err := client.Agent().ServicesWithFilter(fmt.Sprintf(`Service == "%s"`, global.ServerConfig.UserSrvInfo.Name))
	if err != nil {
		panic(err)
	}

	var userSrvHost string
	var userSrvPort int
	for _, v := range data {
		userSrvHost = v.Address
		userSrvPort = v.Port
		break
	}

	if userSrvHost == "" {
		zap.S().Errorw("[InitSrvConn] 连接 【用户服务失败】")
		return
	}

	userConn, err := grpc.Dial(fmt.Sprintf("%s:%d", userSrvHost, userSrvPort), grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		zap.S().Errorw("[GetUserList] 连接 【用户服务失败】", "msg", err.Error())
		return
	}

	zap.S().Infow("[InitSrvConn] 连接 【用户服务成功】")

	/**
	  TODO:
	      1. 后续用户服务下线了
	      2. gai端口了
	      3. 改ip了

	      使用负载均衡
	*/
	// 已经事先创建了连接，后续就不用再进行tcp三次握手了
	// 一个连接，多个goroutine共用，可能会有性能问题 -> 连接池/负载均衡
	global.UserSrvClient = proto.NewUserClient(userConn)
}
