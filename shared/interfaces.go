package shared

import "time"

type ExchangeAPI interface {
	Name() string
	TradesFor(startExc time.Time, endInc time.Time) ([]Trade, error)
	Balance(currency string) (float64, error)
	OrderSummary(orderID string) (OrderSummary, error)
	ListOpenOrders() ([]OrderSummary, error)
	CancelOrder(orderID string) error
	// MarketOrder buys or sells the base currency at whatever price is available on the market,
	// using only base or quote amount.
	MarketOrder(input OrderInput) (averagePrice float64, err error)
	// LimitOrder places a order at a certain price point which automatically executes if the market allows for it.
	// Both base and quote amounts need to be specified.
	LimitOrder(input OrderInput) (orderID string, err error)
}

type Bot interface {
	Name() string
}

type DailyBot interface {
	Bot
	Daily(exchange ExchangeAPI) error
}

type HourlyBot interface {
	Bot
	Hourly(exchange ExchangeAPI) error
}

type MinutelyBot interface {
	Bot
	Minutely(exchange ExchangeAPI) error
}
