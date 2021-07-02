package exchanges

import "github.com/arieroos/crypto-trader/shared"

type Valr struct{}

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

func (v Valr) BuyAtMarket(input shared.OrderInput) (averagePrice float64, err error) {
	panic("implement me")
}

func (v Valr) SellAtMarket(input shared.OrderInput) (averagePrice float64, err error) {
	panic("implement me")
}

func (v Valr) PlaceBuyOrder(input shared.OrderInput) (orderID string, err error) {
	panic("implement me")
}

func (v Valr) PlaceSellOrder(input shared.OrderInput) (orderID string, err error) {
	panic("implement me")
}

func (v Valr) LastTradedPrice(pair string) (float64, error) {
	panic("implement me")
}
