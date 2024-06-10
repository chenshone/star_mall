package router

import (
	"star_mall_api/goods-web/api/goods"
	"star_mall_api/goods-web/middleware"

	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

func InitGoodsRouter(Router *gin.RouterGroup) {
	// 商品服务相关路由
	GoodsRouter := Router.Group("/goods").Use(middleware.Trace())
	zap.S().Info("配置商品服务相关路由")
	{
		GoodsRouter.GET("/", goods.List) // 商品列表
		GoodsRouter.POST("/", middleware.JwtAuth(), middleware.IsAdminAuth(), goods.New)
		GoodsRouter.GET("/:id", goods.Detail) // 商品详情
		GoodsRouter.DELETE("/:id", middleware.JwtAuth(), middleware.IsAdminAuth(), goods.Delete)
		GoodsRouter.GET("/:id/stocks", goods.Stocks) // 获取商品库存
		GoodsRouter.PATCH("/:id", middleware.JwtAuth(), middleware.IsAdminAuth(), goods.UpdateStatus)
		GoodsRouter.PUT("/:id", middleware.JwtAuth(), middleware.IsAdminAuth(), goods.Update)
	}

}
