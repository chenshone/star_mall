package config

type ServerConfig struct {
	Name             string       `mapstructure:"name" json:"name"`
	Host             string       `mapstructure:"host" json:"host"`
	Port             int          `mapstructure:"port" json:"port"`
	Tags             []string     `mapstructure:"tags" json:"tags"`
	GoodsSrvInfo     SrvConfig    `mapstructure:"goods_srv" json:"goods_srv"`
	OrderSrvInfo     SrvConfig    `mapstructure:"order_srv" json:"order_srv"`
	InventorySrvInfo SrvConfig    `mapstructure:"inventory_srv" json:"inventory_srv"`
	JwtInfo          JwtConfig    `mapstructure:"jwt" json:"jwt"`
	ConsulInfo       ConsulConfig `mapstructure:"consul" json:"consul"`
}

type SrvConfig struct {
	Name string `mapstructure:"name" json:"name"`
}

type JwtConfig struct {
	SigningKey string `mapstructure:"key" json:"key"`
}

type ConsulConfig struct {
	Host string `mapstructure:"host" json:"host"`
	Port int    `mapstructure:"port" json:"port"`
}

type NacosConfig struct {
	Host      string `mapstructure:"host"`
	Port      uint64 `mapstructure:"port"`
	Namespace string `mapstructure:"namespace"`
	DataId    string `mapstructure:"data_id"`
	Group     string `mapstructure:"group"`
}
