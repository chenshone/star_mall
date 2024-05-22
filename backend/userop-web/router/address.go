package router

import (
	"star_mall_api/userop-web/api/address"
	"star_mall_api/userop-web/middleware"

	"github.com/gin-gonic/gin"
)

func InitAddressRouter(Router *gin.RouterGroup) {
	AddressRouter := Router.Group("address")
	{
		AddressRouter.GET("", middleware.JwtAuth(), address.List)
		AddressRouter.DELETE("/:id", middleware.JwtAuth(), address.Delete)
		AddressRouter.POST("", middleware.JwtAuth(), address.New)
		AddressRouter.PUT("/:id", middleware.JwtAuth(), address.Update)
	}
}
