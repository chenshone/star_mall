package util_test

import (
	"star_mall_api/userop-web/util"
	"testing"
)

func TestGetFreePort(t *testing.T) {
	if port, err := util.GetFreePort(); err != nil {
		t.Fatal(err)
	} else {
		// 打印随机端口
		t.Logf("随机端口：%d", port)
	}
}
