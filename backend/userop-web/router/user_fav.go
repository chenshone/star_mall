package router

import (
	"star_mall_api/userop-web/api/user_fav"
	"star_mall_api/userop-web/middleware"

	"github.com/gin-gonic/gin"
)

func InitUserFavRouter(Router *gin.RouterGroup) {
	UserFavRouter := Router.Group("userfavs")
	{
		UserFavRouter.DELETE("/:id", middleware.JwtAuth(), user_fav.Delete) // 删除收藏记录
		UserFavRouter.GET("/:id", middleware.JwtAuth(), user_fav.Detail)    // 获取收藏记录
		UserFavRouter.POST("", middleware.JwtAuth(), user_fav.New)          //新建收藏记录
		UserFavRouter.GET("", middleware.JwtAuth(), user_fav.List)          //获取当前用户的收藏
	}
}
