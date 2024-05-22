package main

import (
	"fmt"
	"os"
	"os/signal"
	"star_mall_api/userop-web/global"
	"star_mall_api/userop-web/initialize"
	"star_mall_api/userop-web/util"
	"star_mall_api/userop-web/util/register/consul"
	vd "star_mall_api/userop-web/validator"
	"syscall"

	"github.com/gin-gonic/gin/binding"
	ut "github.com/go-playground/universal-translator"
	"github.com/go-playground/validator/v10"
	uuid "github.com/satori/go.uuid"
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

	registerClient := consul.NewRegistryClient(global.ServerConfig.ConsulInfo.Host, global.ServerConfig.ConsulInfo.Port)

	// register server
	serviceId := uuid.NewV4().String()
	if err := registerClient.Register(global.ServerConfig.Host, global.ServerConfig.Port, global.ServerConfig.Name, global.ServerConfig.Tags, serviceId); err != nil {
		zap.S().Panic("[userop-web] 服务注册失败: ", err.Error())
	}

	// start server
	zap.S().Debugf("start http server listening %d", global.ServerConfig.Port)

	go func() {
		if err := Router.Run(fmt.Sprintf(":%d", global.ServerConfig.Port)); err != nil {
			zap.S().Panic("start http server failed", err.Error())
		}
	}()

	// 接收终止信号
	quit := make(chan os.Signal)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	// 注销服务
	if err := registerClient.DeRegister(serviceId); err != nil {
		zap.S().Info("注销服务 [userop-web] 失败: ", err.Error())
	} else {
		zap.S().Info("注销服务 [userop-web] 成功")
	}
}
