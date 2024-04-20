package api

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/mojocn/base64Captcha"
	"go.uber.org/zap"
)

var store = base64Captcha.DefaultMemStore

func GetCaptcha(c *gin.Context) {
	driver := base64Captcha.NewDriverDigit(80, 240, 5, 0.7, 80)
	cp := base64Captcha.NewCaptcha(driver, store)

	id, b64s, _, err := cp.Generate()

	if err != nil {
		zap.S().Errorf("验证码生成失败", err.Error())
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg": "验证码生成失败",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"captchaId": id,
		"picPath":   b64s,
	})

}
