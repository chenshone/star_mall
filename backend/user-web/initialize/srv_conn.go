package initialize

import (
	"fmt"

	_ "github.com/mbobakov/grpc-consul-resolver"

	"star_mall_api/user-web/global"
	"star_mall_api/user-web/proto"

	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func InitSrvConn() {
	consulInfo := global.ServerConfig.ConsulInfo
	userConn, err := grpc.Dial(fmt.Sprintf("consul://%s:%d/%s?wait=15s", consulInfo.Host, consulInfo.Port, global.ServerConfig.UserSrvInfo.Name),
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy": "round_robin"}`),
	)
	if err != nil {
		zap.S().Fatalw("[InitSrvConn] 连接 【用户服务失败】")
	}

	global.UserSrvClient = proto.NewUserClient(userConn)
}
