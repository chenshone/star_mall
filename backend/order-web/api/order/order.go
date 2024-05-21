package order

import (
	"context"
	"net/http"
	"star_mall_api/order-web/api"
	"star_mall_api/order-web/form"
	"star_mall_api/order-web/global"
	"star_mall_api/order-web/model"
	"star_mall_api/order-web/proto"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/smartwalle/alipay/v3"
	"go.uber.org/zap"
)

func List(ctx *gin.Context) {
	//订单的列表
	userId, _ := ctx.Get("userId")
	claims, _ := ctx.Get("claims")

	request := proto.OrderFilterRequest{}

	//如果是管理员用户则返回所有的订单
	model := claims.(*model.CustomClaims)
	if model.AuthorityId == 1 { // 普通用户，只返回自己的订单信息
		request.UserId = int32(userId.(uint))
	}

	pages := ctx.DefaultQuery("p", "0")
	pagesInt, _ := strconv.Atoi(pages)
	request.Pages = int32(pagesInt)

	perNums := ctx.DefaultQuery("pnum", "0")
	perNumsInt, _ := strconv.Atoi(perNums)
	request.PagePerNums = int32(perNumsInt)

	request.Pages = int32(pagesInt)
	request.PagePerNums = int32(perNumsInt)

	resp, err := global.OrderSrvClient.OrderList(context.Background(), &request)
	if err != nil {
		zap.S().Errorw("获取订单列表失败")
		api.HandleGrpcError2HTTPStatusCode(err, ctx)
		return
	}

	/*
		{
			"total":100,
			"data":[
				{
					"
				}
			]
		}
	*/
	reMap := gin.H{
		"total": resp.Total,
	}
	orderList := make([]any, 0)

	for _, item := range resp.Data {
		tempMap := map[string]any{}

		tempMap["id"] = item.Id
		tempMap["status"] = item.Status
		tempMap["pay_type"] = item.PayType
		tempMap["user"] = item.UserId
		tempMap["post"] = item.Post
		tempMap["total"] = item.Total
		tempMap["address"] = item.Address
		tempMap["name"] = item.Name
		tempMap["mobile"] = item.Mobile
		tempMap["order_sn"] = item.OrderSn
		tempMap["id"] = item.Id
		tempMap["add_time"] = item.AddTime

		orderList = append(orderList, tempMap)
	}
	reMap["data"] = orderList
	ctx.JSON(http.StatusOK, reMap)
}

func New(ctx *gin.Context) {
	orderForm := form.CreateOrderForm{}
	if err := ctx.ShouldBindJSON(&orderForm); err != nil {
		api.HandleValidatorError(ctx, err)
	}
	userId, _ := ctx.Get("userId")
	rsp, err := global.OrderSrvClient.CreateOrder(context.Background(), &proto.OrderRequest{
		UserId:  int32(userId.(uint)),
		Name:    orderForm.Name,
		Mobile:  orderForm.Mobile,
		Address: orderForm.Address,
		Post:    orderForm.Post,
	})
	if err != nil {
		zap.S().Errorw("新建订单失败")
		api.HandleGrpcError2HTTPStatusCode(err, ctx)
		return
	}

	// 生成支付宝支付url
	client, err := alipay.New(global.ServerConfig.AliPayInfo.AppID, global.ServerConfig.AliPayInfo.PrivateKey, false)
	if err != nil {
		zap.S().Errorw("实例化支付宝失败")
		ctx.JSON(http.StatusInternalServerError, gin.H{
			"msg": err.Error(),
		})
		return
	}
	err = client.LoadAliPayPublicKey((global.ServerConfig.AliPayInfo.AliPublicKey))
	if err != nil {
		zap.S().Errorw("加载支付宝的公钥失败")
		ctx.JSON(http.StatusInternalServerError, gin.H{
			"msg": err.Error(),
		})
		return
	}

	var p = alipay.TradePagePay{}
	p.NotifyURL = global.ServerConfig.AliPayInfo.NotifyURL
	p.ReturnURL = global.ServerConfig.AliPayInfo.ReturnURL
	p.Subject = "斯达商城订单-" + rsp.OrderSn
	p.OutTradeNo = rsp.OrderSn
	p.TotalAmount = strconv.FormatFloat(float64(rsp.Total), 'f', 2, 64)
	p.ProductCode = "FAST_INSTANT_TRADE_PAY"

	url, err := client.TradePagePay(p)
	if err != nil {
		zap.S().Errorw("生成支付url失败")
		ctx.JSON(http.StatusInternalServerError, gin.H{
			"msg": err.Error(),
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"id":         rsp.Id,
		"alipay_url": url.String(),
	})
}
func Detail(ctx *gin.Context) {
	id := ctx.Param("id")
	userId, _ := ctx.Get("userId")
	i, err := strconv.Atoi(id)
	if err != nil {
		ctx.JSON(http.StatusNotFound, gin.H{
			"msg": "url格式出错",
		})
		return
	}

	//如果是管理员用户则返回所有的订单
	request := proto.OrderRequest{
		Id: int32(i),
	}
	claims, _ := ctx.Get("claims")
	model := claims.(*model.CustomClaims)
	if model.AuthorityId == 1 { // 普通用户，只返回自己的订单信息
		request.UserId = int32(userId.(uint))
	}

	resp, err := global.OrderSrvClient.OrderDetail(context.Background(), &request)
	if err != nil {
		zap.S().Errorw("获取订单详情失败")
		api.HandleGrpcError2HTTPStatusCode(err, ctx)
		return
	}
	reMap := gin.H{}
	reMap["id"] = resp.OrderInfo.Id
	reMap["status"] = resp.OrderInfo.Status
	reMap["user"] = resp.OrderInfo.UserId
	reMap["post"] = resp.OrderInfo.Post
	reMap["total"] = resp.OrderInfo.Total
	reMap["address"] = resp.OrderInfo.Address
	reMap["name"] = resp.OrderInfo.Name
	reMap["mobile"] = resp.OrderInfo.Mobile
	reMap["pay_type"] = resp.OrderInfo.PayType
	reMap["order_sn"] = resp.OrderInfo.OrderSn

	goodsList := make([]any, 0)
	for _, item := range resp.Data {
		tmpMap := gin.H{
			"id":    item.GoodsId,
			"name":  item.GoodsName,
			"image": item.GoodsImage,
			"price": item.GoodsPrice,
			"nums":  item.Nums,
		}

		goodsList = append(goodsList, tmpMap)
	}

	reMap["goods"] = goodsList

	// 生成支付宝支付url
	client, err := alipay.New(global.ServerConfig.AliPayInfo.AppID, global.ServerConfig.AliPayInfo.PrivateKey, false)
	if err != nil {
		zap.S().Errorw("实例化支付宝失败")
		ctx.JSON(http.StatusInternalServerError, gin.H{
			"msg": err.Error(),
		})
		return
	}
	err = client.LoadAliPayPublicKey((global.ServerConfig.AliPayInfo.AliPublicKey))
	if err != nil {
		zap.S().Errorw("加载支付宝的公钥失败")
		ctx.JSON(http.StatusInternalServerError, gin.H{
			"msg": err.Error(),
		})
		return
	}

	var p = alipay.TradePagePay{}
	p.NotifyURL = global.ServerConfig.AliPayInfo.NotifyURL
	p.ReturnURL = global.ServerConfig.AliPayInfo.ReturnURL
	p.Subject = "斯达商城订单-" + resp.OrderInfo.OrderSn
	p.OutTradeNo = resp.OrderInfo.OrderSn
	p.TotalAmount = strconv.FormatFloat(float64(resp.OrderInfo.Total), 'f', 2, 64)
	p.ProductCode = "FAST_INSTANT_TRADE_PAY"

	url, err := client.TradePagePay(p)
	if err != nil {
		zap.S().Errorw("生成支付url失败")
		ctx.JSON(http.StatusInternalServerError, gin.H{
			"msg": err.Error(),
		})
		return
	}
	reMap["alipay_url"] = url.String()

	ctx.JSON(http.StatusOK, reMap)
}
