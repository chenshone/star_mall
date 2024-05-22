package initialize

import (
	"fmt"

	_ "github.com/mbobakov/grpc-consul-resolver"

	"star_mall_api/userop-web/global"
	"star_mall_api/userop-web/proto"

	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func InitSrvConn() {
	consulInfo := global.ServerConfig.ConsulInfo
	goodsConn, err := grpc.Dial(fmt.Sprintf("consul://%s:%d/%s?wait=15s", consulInfo.Host, consulInfo.Port, global.ServerConfig.GoodsSrvInfo.Name),
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy": "round_robin"}`),
	)
	if err != nil {
		zap.S().Fatalw("[InitSrvConn] 连接 【商品服务失败】")
	}

	global.GoodsClient = proto.NewGoodsClient(goodsConn)

	userOpConn, err := grpc.Dial(fmt.Sprintf("consul://%s:%d/%s?wait=15s", consulInfo.Host, consulInfo.Port, global.ServerConfig.UserOpSrvInfo.Name),
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy": "round_robin"}`),
	)
	if err != nil {
		zap.S().Fatalw("[InitSrvConn] 连接 【用户操作服务失败】")
	}

	global.MessageClient = proto.NewMessageClient(userOpConn)
	global.AddressClient = proto.NewAddressClient(userOpConn)
	global.UserFavClient = proto.NewUserFavClient(userOpConn)
}
