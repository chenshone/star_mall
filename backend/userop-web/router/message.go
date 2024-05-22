package router

import (
	"star_mall_api/userop-web/api/message"
	"star_mall_api/userop-web/middleware"

	"github.com/gin-gonic/gin"
)

func InitMessageRouter(Router *gin.RouterGroup) {
	MessageRouter := Router.Group("message").Use(middleware.JwtAuth())
	{
		MessageRouter.GET("", message.List)
		MessageRouter.POST("", message.New)
	}
}
