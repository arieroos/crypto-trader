package bots

import (
	"github.com/arieroos/crypto-trader/interfaces"
	log "github.com/sirupsen/logrus"
)

func Hourly(api interfaces.ExchangeAPI) error {
	lastPrice, err := api.LastTradedPrice("BTCZAR")
	if err != nil {
		return err
	}

	log.Debugf("Last price for BTCZAR is %s", lastPrice)
	return nil
}
