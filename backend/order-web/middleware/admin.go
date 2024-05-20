package middleware

import (
	"net/http"
	"star_mall_api/order-web/model"

	"github.com/gin-gonic/gin"
)

func IsAdminAuth() gin.HandlerFunc {
	return func(c *gin.Context) {
		claims, _ := c.Get("claims")
		currentUser := claims.(*model.CustomClaims)

		if currentUser.AuthorityId != 2 {
			c.JSON(http.StatusForbidden, gin.H{
				"msg": "权限不足",
			})
			c.Abort()
			return
		}

		c.Next()
	}
}
