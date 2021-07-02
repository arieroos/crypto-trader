package redislib

import (
	"context"
	"github.com/go-redis/redis/v8"
	"sync"
)

var connection *redis.Client
var redisSetup sync.Once
var defaultCtx = context.Background()

func setupRedis() {
	connection = redis.NewClient(&redis.Options{
		Addr: ":6379",
	})
}

func Client() *redis.Client {
	redisSetup.Do(setupRedis)
	return connection
}
