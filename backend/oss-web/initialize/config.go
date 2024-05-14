package initialize

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	"github.com/nacos-group/nacos-sdk-go/v2/clients"
	"github.com/nacos-group/nacos-sdk-go/v2/common/constant"
	"github.com/nacos-group/nacos-sdk-go/v2/vo"
	"github.com/spf13/viper"
	"go.uber.org/zap"

	"star_mall_api/oss-web/global"
)

func GetEnvInfo(env string) bool {
	viper.AutomaticEnv()
	return viper.GetBool(env)
	//刚才设置的环境变量 想要生效 我们必须得重启goland
}

func InitConfig() {
	debug := GetEnvInfo("MALL_DEBUG")
	configFilePrefix := "config"
	configFileName := fmt.Sprintf("%s-pro.yaml", configFilePrefix)
	if debug {
		configFileName = fmt.Sprintf("%s-debug.yaml", configFilePrefix)
	}

	v := viper.New()
	//文件的路径如何设置
	v.SetConfigFile(configFileName)
	if err := v.ReadInConfig(); err != nil {
		panic(err)
	}
	//这个对象如何在其他文件中使用 - 全局变量
	if err := v.Unmarshal(global.NacosConfig); err != nil {
		panic(err)
	}
	zap.S().Infof("Nacos配置信息:%v", global.NacosConfig)

	//从nacos中读取配置信息
	sc := []constant.ServerConfig{
		*constant.NewServerConfig(global.NacosConfig.Host, global.NacosConfig.Port, constant.WithContextPath("/nacos")),
	}

	currentDir, _ := os.Getwd()

	// 获取上一个目录（根目录）
	basePath := filepath.Dir(currentDir)

	cc := *constant.NewClientConfig(
		constant.WithNamespaceId(global.NacosConfig.Namespace),
		constant.WithTimeoutMs(5000),
		constant.WithNotLoadCacheAtStart(true),
		constant.WithLogDir(basePath+"/temp/nacos/log"),
		constant.WithCacheDir(basePath+"/temp/nacos/cache"),
		constant.WithLogLevel("debug"),
	)

	configClient, err := clients.NewConfigClient(
		vo.NacosClientParam{
			ClientConfig:  &cc,
			ServerConfigs: sc,
		},
	)
	if err != nil {
		panic(err)
	}

	content, err := configClient.GetConfig(vo.ConfigParam{
		DataId: global.NacosConfig.DataId,
		Group:  global.NacosConfig.Group})

	if err != nil {
		panic(err)
	}
	//fmt.Println(content) //字符串 - yaml
	//想要将一个json字符串转换成struct，需要去设置这个struct的tag
	err = json.Unmarshal([]byte(content), &global.ServerConfig)
	if err != nil {
		zap.S().Fatalf("读取nacos配置失败: %v", err.Error())
	}
	err = configClient.ListenConfig(vo.ConfigParam{
		DataId: global.NacosConfig.DataId,
		Group:  global.NacosConfig.Group,
		OnChange: func(namespace, group, dataId, data string) {
			err = json.Unmarshal([]byte(data), &global.ServerConfig)
			if err != nil {
				zap.S().Fatalf("更新nacos配置失败: %v", err.Error())
			} else {
				zap.S().Infof("更新nacos配置成功")
			}
		},
	})

	if err != nil {
		zap.S().Fatalf("监听nacos配置失败: %v", err.Error())
	}

}
