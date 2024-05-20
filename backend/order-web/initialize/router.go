package initialize

import (
	"net/http"
	"star_mall_api/order-web/middleware"
	"star_mall_api/order-web/router"

	"github.com/gin-gonic/gin"
)

func Routers() *gin.Engine {
	Router := gin.Default()

	Router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"code":    http.StatusOK,
			"success": true,
		})
	})

	Router.Use(middleware.Cors())

	ApiGroup := Router.Group("/o/v1")

	router.InitOrderRouter(ApiGroup)
	router.InitShopCartRouter(ApiGroup)

	return Router
}
