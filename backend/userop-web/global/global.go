package global

import (
	"star_mall_api/userop-web/config"
	"star_mall_api/userop-web/proto"

	ut "github.com/go-playground/universal-translator"
)

var (
	NacosConfig *config.NacosConfig = &config.NacosConfig{}

	ServerConfig *config.ServerConfig = &config.ServerConfig{}

	Trans ut.Translator

	GoodsClient proto.GoodsClient // 商品服务客户端

	AddressClient proto.AddressClient // 地址服务客户端
	MessageClient proto.MessageClient // 留言服务客户端
	UserFavClient proto.UserFavClient // 用户收藏服务客户端
)
