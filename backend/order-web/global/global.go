package global

import (
	"star_mall_api/order-web/config"
	"star_mall_api/order-web/proto"

	ut "github.com/go-playground/universal-translator"
)

var (
	NacosConfig *config.NacosConfig = &config.NacosConfig{}

	ServerConfig *config.ServerConfig = &config.ServerConfig{}

	Trans ut.Translator

	GoodsSrvClient proto.GoodsClient // 商品服务客户端

	OrderSrvClient proto.OrderClient // 订单服务客户端

	InventorySrvClient proto.InventoryClient // 库存服务客户端
)
