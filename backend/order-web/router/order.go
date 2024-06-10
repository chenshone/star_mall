package router

import (
	"star_mall_api/order-web/api/order"
	"star_mall_api/order-web/api/pay"
	"star_mall_api/order-web/middleware"

	"github.com/gin-gonic/gin"
)

func InitOrderRouter(Router *gin.RouterGroup) {
	OrderRouter := Router.Group("orders").Use(middleware.JwtAuth()).Use(middleware.Trace())
	{
		OrderRouter.GET("/", order.List)      // 订单列表
		OrderRouter.POST("/", order.New)      // 新建订单
		OrderRouter.GET("/:id", order.Detail) // 获取订单
	}

	PayRouter := Router.Group("pay")
	{
		PayRouter.POST("/alipay/notify", pay.Notify) // 支付宝支付回调订单
	}
}
