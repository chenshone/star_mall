package initialize_test

import (
	"star_mall_api/order-web/initialize"
	"testing"
)

func TestGetEnvInfo(t *testing.T) {
	// 测试GetEnvInfo函数
	debug := initialize.GetEnvInfo("MALL_DEBUG")

	t.Logf("MALL_DEBUG: %v", debug)
}
