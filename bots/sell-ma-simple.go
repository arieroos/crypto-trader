package bots

import (
	"fmt"
	"github.com/arieroos/crypto-trader/redislib"
	"github.com/arieroos/crypto-trader/shared"
	log "github.com/sirupsen/logrus"
	"time"
)

const hourFormat = "2006-01-02:15"

type SellMASimple struct{}

func (s SellMASimple) Name() string {
	return "Sell MA Simple"
}

func (s SellMASimple) Hourly(exchange shared.ExchangeAPI) error {
	lastPrice, err := exchange.LastTradedPrice("BTCZAR")
	if err != nil {
		return err
	}

	log.Debugf("Last price for BTCZAR is %s", lastPrice)

	err = redislib.SaveValueForBot(s, time.Now().Format(hourFormat), fmt.Sprintf("%f", lastPrice))
	if err != nil {
		return err
	}

	return nil
}
