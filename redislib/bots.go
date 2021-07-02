package redislib

import (
	"fmt"
	"github.com/arieroos/crypto-trader/shared"
)

func botKey(bot string, key string) string {
	return fmt.Sprintf("cb:%s:%s", bot, key)
}

func SaveValueForBot(bot shared.Bot, key string, value string) error {
	_, err := Client().Set(defaultCtx, botKey(bot.Name(), key), value, 0).Result()
	return err
}

func GetValueForBot(bot shared.Bot, key string) (string, error) {
	return Client().Get(defaultCtx, botKey(bot.Name(), key)).Result()
}
