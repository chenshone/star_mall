package router

import (
	"star_mall_api/user-web/api"
	"star_mall_api/user-web/middleware"

	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

func InitUserRouter(Router *gin.RouterGroup) {
	UserRouter := Router.Group("/user")
	zap.S().Info("配置用户相关路由")
	{
		UserRouter.GET("/list", middleware.JwtAuth(), middleware.IsAdminAuth(), api.GetUserList)
		UserRouter.POST("/pwd_login", api.PasswordLogin)
		UserRouter.POST("/register", api.Register)
	}

}
