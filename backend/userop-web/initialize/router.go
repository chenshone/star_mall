package initialize

import (
	"net/http"
	"star_mall_api/userop-web/middleware"
	"star_mall_api/userop-web/router"

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

	ApiGroup := Router.Group("/uo/v1")

	router.InitAddressRouter(ApiGroup)
	router.InitMessageRouter(ApiGroup)
	router.InitUserFavRouter(ApiGroup)

	return Router
}
