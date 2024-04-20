package initialize

import (
	"star_mall_api/user-web/middleware"
	"star_mall_api/user-web/router"

	"github.com/gin-gonic/gin"
)

func Routers() *gin.Engine {
	Router := gin.Default()
	Router.Use(middleware.Cors())

	ApiGroup := Router.Group("/u/v1")

	router.InitUserRouter(ApiGroup)

	router.InitBaseRouter(ApiGroup)

	return Router
}
