package main

import (
	"fmt"
	"github.com/arieroos/crypto-trader/bots"
	"github.com/arieroos/crypto-trader/exchanges"
	"github.com/go-co-op/gocron"
	log "github.com/sirupsen/logrus"
	"time"
)

func main() {
	fmt.Println("It is time to go!")

	schedule := gocron.NewScheduler(time.UTC)

	_, err := schedule.Every(1).Hour().Do(func() {
		err := bots.Hourly(exchanges.Valr{})
		if err != nil {
			log.Error(err)
		}
	})
	if err != nil {
		log.Fatal(err)
	}

	schedule.StartBlocking()
}
