package api

import (
	"context"
	"fmt"
	"net/http"
	"star_mall_api/user-web/form"
	"star_mall_api/user-web/global"
	"star_mall_api/user-web/global/response"
	"star_mall_api/user-web/middleware"
	"star_mall_api/user-web/model"
	pb "star_mall_api/user-web/proto"
	"strconv"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
	"github.com/golang-jwt/jwt/v5"
	"github.com/redis/go-redis/v9"

	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/status"
)

func removeTopStruct(fileds map[string]string) map[string]string {
	resp := map[string]string{}
	for field, err := range fileds {
		resp[field[strings.Index(field, ".")+1:]] = err
	}
	return resp
}

func HandleGrpcError2HTTPStatusCode(err error, c *gin.Context) {
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
		case codes.AlreadyExists:
			c.JSON(http.StatusBadRequest, gin.H{
				"msg": "手机号已注册",
			})
		default:
			c.JSON(http.StatusInternalServerError, gin.H{
				"msg": "用户服务错误",
			})
		}
	}
}

func HandleValidatorError(c *gin.Context, err error) {
	errs, ok := err.(validator.ValidationErrors)
	if !ok {
		c.JSON(http.StatusOK, gin.H{
			"msg": err.Error(),
		})
		return
	}
	c.JSON(http.StatusBadRequest, gin.H{
		"error": removeTopStruct(errs.Translate(global.Trans)),
	})
}

func GetUserList(ginCtx *gin.Context) {
	conn, err := grpc.Dial(fmt.Sprintf("%s:%d", global.ServerConfig.UserSrvInfo.Host, global.ServerConfig.UserSrvInfo.Port), grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		zap.S().Errorw("[GetUserList] 连接 【用户服务失败】", "msg", err.Error())
		return
	}
	defer conn.Close()

	claims, _ := ginCtx.Get("claims")

	zap.S().Infof("访问用户: %d", claims.(*model.CustomClaims).ID)

	client := pb.NewUserClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)

	defer cancel()

	pn, _ := strconv.Atoi(ginCtx.DefaultQuery("pn", "0"))
	pSize, _ := strconv.Atoi(ginCtx.DefaultQuery("psize", "10"))

	resp, err := client.GetUserList(ctx, &pb.PageInfo{
		Pn:    uint32(pn),
		PSize: uint32(pSize),
	})
	if err != nil {
		zap.S().Errorw("[GetUserList] 查询 【用户列表】 失败", "msg", err.Error())
		HandleGrpcError2HTTPStatusCode(err, ginCtx)
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

func PasswordLogin(ginCtx *gin.Context) {
	// 表单验证
	passwordLoginForm := form.PasswordLoginForm{}
	if err := ginCtx.ShouldBind(&passwordLoginForm); err != nil {
		HandleValidatorError(ginCtx, err)
		return
	}

	if !store.Verify(passwordLoginForm.CaptchaId, passwordLoginForm.Captcha, true) {
		ginCtx.JSON(http.StatusBadRequest, gin.H{
			"captcha": "验证码错误",
		})
		return
	}

	conn, err := grpc.Dial(fmt.Sprintf("%s:%d", global.ServerConfig.UserSrvInfo.Host, global.ServerConfig.UserSrvInfo.Port), grpc.WithTransportCredentials(insecure.NewCredentials()))

	if err != nil {
		zap.S().Errorw("[PasswordLogin] 连接 【用户服务失败】", "msg", err.Error())
		return
	}
	defer conn.Close()

	client := pb.NewUserClient(conn)

	if resp, err := client.GetUserByMobile(context.Background(), &pb.MobileRequest{
		Mobile: passwordLoginForm.Mobile,
	}); err != nil {
		if e, ok := status.FromError(err); ok {
			switch e.Code() {
			case codes.NotFound:
				ginCtx.JSON(http.StatusNotFound, map[string]string{
					"mobile": "用户不存在",
				})
				return
			default:
				ginCtx.JSON(http.StatusInternalServerError, map[string]string{
					"mobile": "登录失败",
				})
			}
			return
		}
	} else {
		if checkPasswordResp, checkPasswordErr := client.CheckPassword(context.Background(), &pb.PasswordCheckInfo{
			Password:          passwordLoginForm.Password,
			EncryptedPassword: resp.Password,
		}); checkPasswordErr != nil {
			ginCtx.JSON(http.StatusInternalServerError, map[string]string{
				"password": "登录失败",
			})
		} else {
			if checkPasswordResp.Success {
				// 生成token
				j := middleware.NewJwt()

				claim := model.CustomClaims{
					ID:          uint(resp.Id),
					Nickname:    resp.Nickname,
					AuthorityId: uint(resp.Role),
					RegisteredClaims: jwt.RegisteredClaims{
						NotBefore: jwt.NewNumericDate(time.Now()),
						ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Hour * 24 * 30)),
						Issuer:    "star_mall",
					}}

				token, err := j.CreateToken(claim)
				if err != nil {
					ginCtx.JSON(http.StatusInternalServerError, gin.H{
						"msg": "生成token失败",
					})
					return
				}

				ginCtx.JSON(http.StatusOK, gin.H{
					"id":         resp.Id,
					"nick_name":  resp.Nickname,
					"token":      token,
					"expires_at": (time.Now().Unix() + 60*60*24*30) * 1000,
				})
			} else {
				ginCtx.JSON(http.StatusBadRequest, map[string]string{
					"password": "登录失败",
				})
			}
		}
	}
}

func Register(ginCtx *gin.Context) {
	registerForm := form.RegisterForm{}

	if err := ginCtx.ShouldBind(&registerForm); err != nil {
		HandleValidatorError(ginCtx, err)
		return
	}

	rdb := redis.NewClient(&redis.Options{
		Addr: fmt.Sprintf("%s:%d", global.ServerConfig.RedisInfo.Host, global.ServerConfig.RedisInfo.Port),
		DB:   global.ServerConfig.RedisInfo.DB,
	})

	if value, err := rdb.Get(context.Background(), registerForm.Mobile).Result(); err == redis.Nil {
		ginCtx.JSON(http.StatusBadRequest, gin.H{
			"code": "验证码错误",
		})
		return
	} else if value != registerForm.Code {
		ginCtx.JSON(http.StatusBadRequest, gin.H{
			"code": "验证码错误",
		})
		return
	}

	conn, err := grpc.Dial(fmt.Sprintf("%s:%d", global.ServerConfig.UserSrvInfo.Host, global.ServerConfig.UserSrvInfo.Port), grpc.WithTransportCredentials(insecure.NewCredentials()))

	if err != nil {
		zap.S().Errorw("[PasswordLogin] 连接 【用户服务失败】", "msg", err.Error())
		return
	}
	defer conn.Close()

	client := pb.NewUserClient(conn)

	user, err := client.CreateUser(context.Background(), &pb.CreateUserInfo{
		Mobile:   registerForm.Mobile,
		Password: registerForm.Password,
		Nickname: registerForm.Mobile,
	})

	if err != nil {
		zap.S().Errorw("[Register] 创建用户失败", "msg", err.Error())
		HandleGrpcError2HTTPStatusCode(err, ginCtx)
		return
	}

	j := middleware.NewJwt()

	claim := model.CustomClaims{
		ID:          uint(user.Id),
		Nickname:    user.Nickname,
		AuthorityId: uint(user.Role),
		RegisteredClaims: jwt.RegisteredClaims{
			NotBefore: jwt.NewNumericDate(time.Now()),
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Hour * 24 * 30)),
			Issuer:    "star_mall",
		},
	}

	token, err := j.CreateToken(claim)
	if err != nil {
		ginCtx.JSON(http.StatusInternalServerError, gin.H{
			"msg": "生成token失败",
		})
		return
	}

	ginCtx.JSON(http.StatusOK, gin.H{
		"id":         user.Id,
		"nick_name":  user.Nickname,
		"token":      token,
		"expires_at": (time.Now().Unix() + 60*60*24*30) * 1000,
	})

}
