package main

import (
	"fmt"
	"star_mall_api/user-web/global"
	"star_mall_api/user-web/initialize"
	"star_mall_api/user-web/util"
	vd "star_mall_api/user-web/validator"

	"github.com/gin-gonic/gin/binding"
	ut "github.com/go-playground/universal-translator"
	"github.com/go-playground/validator/v10"
	"go.uber.org/zap"
)

func main() {
	// init logger
	initialize.InitLogger()

	// init config
	initialize.InitConfig()

	// init routers
	Router := initialize.Routers()

	// init translator
	if err := initialize.InitTrans("zh"); err != nil {
		panic(err)
	}

	// 初始化srv连接
	initialize.InitSrvConn()

	// 本地开发环境端口号固定，线上环境随机端口号
	if debug := initialize.GetEnvInfo("MALL_DEBUG"); !debug {
		port, err := util.GetFreePort()
		if err == nil {
			global.ServerConfig.Port = port
		}
	}

	// 注册验证器
	if v, ok := binding.Validator.Engine().(*validator.Validate); ok {
		v.RegisterValidation("mobile", vd.ValidateMobile)
		v.RegisterTranslation("mobile", global.Trans, func(ut ut.Translator) error {
			return ut.Add("mobile", "{0} 非法的手机号码!", true)
		}, func(ut ut.Translator, fe validator.FieldError) string {
			t, _ := ut.T("mobile", fe.Field())
			return t
		})
	}

	// start server
	zap.S().Debugf("start http server listening %d", global.ServerConfig.Port)

	if err := Router.Run(fmt.Sprintf(":%d", global.ServerConfig.Port)); err != nil {
		zap.S().Panic("start http server failed", err.Error())
	}
}
