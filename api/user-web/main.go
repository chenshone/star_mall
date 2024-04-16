package main

import (
	"fmt"
	"star_mall_api/user-web/initialize"

	"go.uber.org/zap"
)

func main() {
	port := 8021

	// init logger
	initialize.InitLogger()

	// init routers
	Router := initialize.Routers()

	// start server
	zap.S().Debugf("start http server listening %d", port)

	if err := Router.Run(fmt.Sprintf(":%d", port)); err != nil {
		zap.S().Panic("start http server failed", err.Error())
	}
}
