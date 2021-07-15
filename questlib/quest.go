package questlib

import (
	"github.com/arieroos/crypto-trader/shared"
	"github.com/jackc/pgx"
	"github.com/pkg/errors"
	"github.com/sirupsen/logrus"
	"regexp"
	"strings"
	"sync"
)

var conn *pgx.ConnPool
var setupOnce sync.Once

func setupPool() {
	setupOnce.Do(func() {
		var err error
		conn, err = pgx.NewConnPool(pgx.ConnPoolConfig{
			ConnConfig: pgx.ConnConfig{
				Host: "127.0.0.1",
				Port: 8812,
			},
		})
		if err != nil {
			logrus.Fatal(err)
		}
	})
}

func tableName(exchangeName string) string {
	space := regexp.MustCompile(`\s+`)
	s := space.ReplaceAllString(exchangeName, "_")
	return strings.ToLower(s)
}

func ensureTable(tableName string) error {
	stmt := `
		CREATE TABLE IF NOT EXISTS $1
		(traded_at timestamp, pair string, price float)
		timestamp(traded_at) PARTITION BY DAY;
	`
	_, err := conn.Exec(stmt, tableName)
	return errors.Wrapf(err, "Could not create table %s", tableName)
}

func SaveTrades(trades []shared.Trade, exchangeName string) error {
	setupPool()
	tn := tableName(exchangeName)
	err := ensureTable(tn)
	if err != nil {
		return err
	}

	stmt := "INSERT INTO $1 (traded_at, pair, price) VALUES ($2, $3, $4)"
	for _, trade := range trades {
		_, err = conn.Exec(stmt, tn, trade.TradedAt, trade.Price)
		if err != nil {
			return errors.Wrap(err, "Could not insert trade row")
		}
	}
	return nil
}
