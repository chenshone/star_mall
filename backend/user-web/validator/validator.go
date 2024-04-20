package validator

import (
	"regexp"

	"github.com/go-playground/validator/v10"
)

func ValidateMobile(fl validator.FieldLevel) bool {
	// 获取手机号
	mobile := fl.Field().String()
	// 校验手机号
	ok, _ := regexp.MatchString(`^1[3-9]\d{9}$`, mobile)

	return ok
}
