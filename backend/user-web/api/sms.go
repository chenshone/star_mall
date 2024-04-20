package api

import (
	"context"
	"fmt"
	"math/rand"
	"net/http"
	"star_mall_api/user-web/form"
	"star_mall_api/user-web/global"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
)

func generateSmsCode(width int) string {
	numeric := [10]byte{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
	r := len(numeric)

	var sb strings.Builder

	for i := 0; i < width; i++ {
		sb.WriteByte(numeric[rand.Intn(r)])
	}

	return sb.String()
}

func SendSms(c *gin.Context) {
	sendSmsForm := form.SendSmsForm{}

	if err := c.ShouldBind(&sendSmsForm); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": err.Error(),
		})
		return
	}

	rdb := redis.NewClient(&redis.Options{
		Addr: fmt.Sprintf("%s:%d", global.ServerConfig.RedisInfo.Host, global.ServerConfig.RedisInfo.Port),
		DB:   global.ServerConfig.RedisInfo.DB,
	})

	rdb.Set(context.Background(), sendSmsForm.Mobile, generateSmsCode(global.ServerConfig.SmsInfo.Len), time.Duration(global.ServerConfig.SmsInfo.Expire)*time.Second)

	c.JSON(http.StatusOK, gin.H{
		"msg": "发送成功",
	})
}
