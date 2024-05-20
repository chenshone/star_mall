package router

import (
	"star_mall_api/order-web/api/order"
	"star_mall_api/order-web/middleware"

	"github.com/gin-gonic/gin"
)

func InitOrderRouter(Router *gin.RouterGroup) {
	OrderRouter := Router.Group("orders").Use(middleware.JwtAuth())
	{
		OrderRouter.GET("/", order.List)      // 订单列表
		OrderRouter.POST("/", order.New)      // 新建订单
		OrderRouter.GET("/:id", order.Detail) // 获取订单
	}
}
