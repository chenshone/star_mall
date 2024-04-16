package api

import (
	"context"
	"fmt"
	"net/http"
	"star_mall_api/user-web/global/response"
	pb "star_mall_api/user-web/proto"
	"time"

	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/status"
)

func handleGrpcError2HTTPStatusCode(err error, c *gin.Context) {
	if err == nil {
		return
	}

	if e, ok := status.FromError(err); ok {
		switch e.Code() {
		case codes.NotFound:
			c.JSON(http.StatusNotFound, gin.H{
				"msg": e.Message(),
			})
		case codes.Internal:
			c.JSON(http.StatusInternalServerError, gin.H{
				"msg": "内部错误",
			})
		case codes.InvalidArgument:
			c.JSON(http.StatusBadRequest, gin.H{
				"msg": "参数错误",
			})
		default:
			c.JSON(http.StatusInternalServerError, gin.H{
				"msg": "用户服务错误",
			})
		}
	}
}

func GetUserList(ginCtx *gin.Context) {
	ip := "127.0.0.1"
	port := 50051

	conn, err := grpc.Dial(fmt.Sprintf("%s:%d", ip, port), grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		zap.S().Errorw("[GetUserList] 连接 【用户服务失败】", "msg", err.Error())
		return
	}
	defer conn.Close()

	client := pb.NewUserClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)

	defer cancel()

	resp, err := client.GetUserList(ctx, &pb.PageInfo{
		Pn:    0,
		PSize: 0,
	})
	if err != nil {
		zap.S().Errorw("[GetUserList] 查询 【用户列表】 失败", "msg", err.Error())
		handleGrpcError2HTTPStatusCode(err, ginCtx)
		return
	}

	result := make([]interface{}, 0)

	for _, value := range resp.Data {
		user := response.UserResponse{
			Id:       value.Id,
			Nickname: value.Nickname,
			Birthday: response.JsonTime(time.Unix(int64(value.Birthday), 0)),
			Gender:   value.Gender,
			Mobile:   value.Mobile,
		}

		result = append(result, user)
	}

	ginCtx.JSON(http.StatusOK, result)
}
