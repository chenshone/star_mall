package global

import (
	"star_mall_api/user-web/config"
	"star_mall_api/user-web/proto"

	ut "github.com/go-playground/universal-translator"
)

var (
	ServerConfig *config.ServerConfig = &config.ServerConfig{}

	Trans ut.Translator

	UserSrvClient proto.UserClient
)
