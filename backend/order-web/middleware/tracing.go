package middleware

import (
	"fmt"
	"star_mall_api/order-web/global"

	"github.com/gin-gonic/gin"
	"github.com/opentracing/opentracing-go"
	"github.com/uber/jaeger-client-go"
	jaegercfg "github.com/uber/jaeger-client-go/config"
)

func Trace() gin.HandlerFunc {
	return func(c *gin.Context) {
		// 添加一些追踪逻辑
		cfg := jaegercfg.Configuration{
			Sampler: &jaegercfg.SamplerConfig{
				Type:  jaeger.SamplerTypeConst,
				Param: 1,
			},
			Reporter: &jaegercfg.ReporterConfig{
				// 设置日志输出
				LogSpans: true,
				// 设置追踪数据发送到Jaeger的地址
				LocalAgentHostPort: fmt.Sprintf("%s:%d", global.ServerConfig.JaegerInfo.Host, global.ServerConfig.JaegerInfo.Port),
			},
			ServiceName: global.ServerConfig.JaegerInfo.Name,
		}

		// 创建Jaeger追踪器
		tracer, closer, err := cfg.NewTracer(jaegercfg.Logger(jaeger.StdLogger))
		if err != nil {
			panic(err)
		}
		defer closer.Close()

		startSpan := opentracing.StartSpan(c.Request.URL.Path)
		defer startSpan.Finish()

		// 将追踪器绑定到Gin的上下文中
		c.Set("tracer", tracer)
		c.Set("parentSpan", startSpan)

		// 继续处理请求
		c.Next()
	}
}
