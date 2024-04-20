package global

import (
	"star_mall_api/user-web/config"

	ut "github.com/go-playground/universal-translator"
)

var (
	ServerConfig *config.ServerConfig = &config.ServerConfig{}

	Trans ut.Translator
)
