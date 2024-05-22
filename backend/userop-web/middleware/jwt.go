package middleware

import (
	"errors"
	"net/http"
	"star_mall_api/userop-web/global"
	"star_mall_api/userop-web/model"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

func JwtAuth() gin.HandlerFunc {
	return func(c *gin.Context) {
		token := c.Request.Header.Get("x-token")

		if token == "" {
			c.JSON(http.StatusUnauthorized, gin.H{"msg": "请登录"})
			c.Abort()
			return
		}

		j := NewJwt()

		claims, err := j.ParseToken(token)
		if err != nil {
			if err == ErrTokenExpired {
				c.JSON(http.StatusUnauthorized, gin.H{"msg": "授权已过期"})
				c.Abort()
				return
			}

			c.JSON(http.StatusUnauthorized, gin.H{"msg": "未登录"})
			c.Abort()
			return
		}
		c.Set("claims", claims)
		c.Set("userId", claims.ID)
		c.Next()
	}
}

type Jwt struct {
	SigningKey []byte
}

var (
	ErrTokenExpired = errors.New("token is expired")
	ErrTokenInvalid = errors.New("couldn't handle this token")
)

func NewJwt() *Jwt {
	return &Jwt{
		[]byte(global.ServerConfig.JwtInfo.SigningKey),
	}
}

func (j *Jwt) CreateToken(claims model.CustomClaims) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(j.SigningKey)
}

func (j *Jwt) ParseToken(tokenString string) (*model.CustomClaims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &model.CustomClaims{}, func(token *jwt.Token) (i interface{}, e error) {
		return j.SigningKey, nil
	})
	if err != nil {
		return nil, err
	}

	if token != nil {
		if claims, ok := token.Claims.(*model.CustomClaims); ok && token.Valid {
			return claims, nil
		}
		return nil, ErrTokenInvalid
	} else {
		return nil, ErrTokenInvalid
	}
}

func (j *Jwt) RefreshToken(tokenString string) (string, error) {
	token, err := jwt.ParseWithClaims(tokenString, &model.CustomClaims{}, func(token *jwt.Token) (interface{}, error) {
		return j.SigningKey, nil
	})
	if err != nil {
		return "", err
	}

	if claims, ok := token.Claims.(*model.CustomClaims); ok && token.Valid {
		claims.RegisteredClaims.ExpiresAt = jwt.NewNumericDate(time.Now().Add(1 * time.Hour))
		return j.CreateToken(*claims)
	}
	return "", ErrTokenInvalid
}
