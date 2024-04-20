package initialize

import (
	"fmt"
	"star_mall_api/user-web/global"

	"github.com/fsnotify/fsnotify"
	"github.com/spf13/viper"
	"go.uber.org/zap"
)

// func getEnvInfo(env string) bool {
// 	viper.AutomaticEnv()
// 	return viper.GetBool(env)
// }

func InitConfig() {
	// 读取配置文件
	// debug := getEnvInfo("MALL_DEBUG")
	debug := true
	configFilePrefix := "config"
	configFileName := fmt.Sprintf("%s-pro.yaml", configFilePrefix)

	if debug {
		configFileName = fmt.Sprintf("%s-debug.yaml", configFilePrefix)
	}

	v := viper.New()

	v.SetConfigFile(configFileName)
	if err := v.ReadInConfig(); err != nil {
		panic(err)
	}

	if err := v.Unmarshal(global.ServerConfig); err != nil {
		panic(err)
	}

	zap.S().Infof("配置信息:%v", global.ServerConfig)

	v.WatchConfig()
	v.OnConfigChange(func(e fsnotify.Event) {
		zap.S().Infof("配置文件产生变化: %s", e.Name)
		_ = v.ReadInConfig()
		_ = v.Unmarshal(global.ServerConfig)
		zap.S().Infof("配置信息:%v", global.ServerConfig)
	})
}
