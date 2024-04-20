package config

type UserSrvConfig struct {
	Host string `mapstructure:"host"`
	Port int    `mapstructure:"port"`
}

type JwtConfig struct {
	SigningKey string `mapstructure:"key"`
}

type ServerConfig struct {
	Name        string        `mapstructure:"name"`
	Port        int           `mapstructure:"port"`
	UserSrvInfo UserSrvConfig `mapstructure:"user_srv"`
	JwtInfo     JwtConfig     `mapstructure:"jwt"`
	RedisInfo   RedisConfig   `mapstructure:"redis"`
	SmsInfo     SmsConfig     `mapstructure:"sms"`
}

type RedisConfig struct {
	Host string `mapstructure:"host"`
	Port int    `mapstructure:"port"`
	DB   int    `mapstructure:"db"`
}

type SmsConfig struct {
	Len    int `mapstructure:"len"`
	Expire int `mapstructure:"expire"`
}
