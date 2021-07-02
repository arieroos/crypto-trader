package bots

import (
	"github.com/arieroos/crypto-trader/shared"
	log "github.com/sirupsen/logrus"
)

func Hourly(api shared.ExchangeAPI) error {
	lastPrice, err := api.LastTradedPrice("BTCZAR")
	if err != nil {
		return err
	}

	log.Debugf("Last price for BTCZAR is %s", lastPrice)
	return nil
}
