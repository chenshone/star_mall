package global

import (
	"star_mall_api/goods-web/config"
	"star_mall_api/goods-web/proto"

	ut "github.com/go-playground/universal-translator"
)

var (
	NacosConfig *config.NacosConfig = &config.NacosConfig{}

	ServerConfig *config.ServerConfig = &config.ServerConfig{}

	Trans ut.Translator

	GoodsSrvClient proto.GoodsClient // 商品服务客户端
)
