package router

import (
	"star_mall_api/goods-web/api/category"

	"github.com/gin-gonic/gin"
)

func InitCategoryRouter(Router *gin.RouterGroup) {
	// 分类管理
	CategoryRouter := Router.Group("categorys")
	{
		CategoryRouter.GET("/", category.List)
		CategoryRouter.DELETE("/:id", category.Delete)
		CategoryRouter.GET("/:id", category.Detail)
		CategoryRouter.POST("/", category.New)
		CategoryRouter.PUT("/:id", category.Update)
	}
}
