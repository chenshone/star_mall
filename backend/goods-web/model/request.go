package model

import "github.com/golang-jwt/jwt/v5"

type CustomClaims struct {
	ID          uint
	Nickname    string
	AuthorityId uint
	jwt.RegisteredClaims
}
