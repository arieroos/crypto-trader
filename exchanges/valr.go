package exchanges

import "github.com/arieroos/crypto-trader/interfaces"

type Valr struct{}

func (v Valr) Balance(currency string) (float64, error) {
	panic("implement me")
}

func (v Valr) OrderSummary(orderID string) (interfaces.OrderSummary, error) {
	panic("implement me")
}

func (v Valr) ListOpenOrders() ([]interfaces.OrderSummary, error) {
	panic("implement me")
}

func (v Valr) CancelOrder(orderID string) error {
	panic("implement me")
}

func (v Valr) BuyAtMarket(input interfaces.OrderInput) (averagePrice float64, err error) {
	panic("implement me")
}

func (v Valr) SellAtMarket(input interfaces.OrderInput) (averagePrice float64, err error) {
	panic("implement me")
}

func (v Valr) PlaceBuyOrder(input interfaces.OrderInput) (orderID string, err error) {
	panic("implement me")
}

func (v Valr) PlaceSellOrder(input interfaces.OrderInput) (orderID string, err error) {
	panic("implement me")
}

func (v Valr) LastTradedPrice(pair string) (float64, error) {
	panic("implement me")
}
