package exchanges

import (
	"github.com/arieroos/crypto-trader/shared"
	"time"
)

type Valr struct{}

func (v Valr) Name() string {
	return "VALR South Africa"
}

func (v Valr) TradesFor(startExc time.Time, endInc time.Time) ([]shared.Trade, error) {
	panic("implement me")
}

func (v Valr) Balance(currency string) (float64, error) {
	panic("implement me")
}

func (v Valr) OrderSummary(orderID string) (shared.OrderSummary, error) {
	panic("implement me")
}

func (v Valr) ListOpenOrders() ([]shared.OrderSummary, error) {
	panic("implement me")
}

func (v Valr) CancelOrder(orderID string) error {
	panic("implement me")
}

func (v Valr) MarketOrder(input shared.OrderInput) (averagePrice float64, err error) {
	panic("implement me")
}

func (v Valr) LimitOrder(input shared.OrderInput) (orderID string, err error) {
	panic("implement me")
}
