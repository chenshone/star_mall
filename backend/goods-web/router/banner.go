package router

import (
	"star_mall_api/goods-web/api/banners"
	"star_mall_api/goods-web/middleware"

	"github.com/gin-gonic/gin"
)

func InitBannerRouter(Router *gin.RouterGroup) {
	BannerRouter := Router.Group("banners").Use(middleware.Trace())
	{
		BannerRouter.GET("", banners.List)                                                          // 轮播图列表页
		BannerRouter.DELETE("/:id", middleware.JwtAuth(), middleware.IsAdminAuth(), banners.Delete) // 删除轮播图
		BannerRouter.POST("", middleware.JwtAuth(), middleware.IsAdminAuth(), banners.New)          //新建轮播图
		BannerRouter.PUT("/:id", middleware.JwtAuth(), middleware.IsAdminAuth(), banners.Update)    //修改轮播图信息
	}
}
