package router

import (
	"star_mall_api/order-web/api/shop_cart"
	"star_mall_api/order-web/middleware"

	"github.com/gin-gonic/gin"
)

func InitShopCartRouter(Router *gin.RouterGroup) {
	ShopCartRouter := Router.Group("shopcarts").Use(middleware.JwtAuth())
	{
		ShopCartRouter.GET("/", shop_cart.List)         // 购物车列表
		ShopCartRouter.POST("/", shop_cart.New)         // 新建购物车
		ShopCartRouter.PATCH("/:id", shop_cart.Update)  // 更新条目
		ShopCartRouter.DELETE("/:id", shop_cart.Delete) // 删除条目
	}
}
