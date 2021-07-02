package shared

type ExchangeAPI interface {
	LastTradedPrice(pair string) (float64, error)
	Balance(currency string) (float64, error)
	OrderSummary(orderID string) (OrderSummary, error)
	ListOpenOrders() ([]OrderSummary, error)
	CancelOrder(orderID string) error
	// BuyAtMarket buys the base currency at whatever price is available on the market,
	// using the base amount if it is not 0 or quote amount if base amount is 0.
	BuyAtMarket(input OrderInput) (averagePrice float64, err error)
	// SellAtMarket sells the base currency at whatever price is available on the market,
	// using the base amount if it is not 0 or quote amount if base amount is 0.
	SellAtMarket(input OrderInput) (averagePrice float64, err error)
	PlaceBuyOrder(input OrderInput) (orderID string, err error)
	PlaceSellOrder(input OrderInput) (orderID string, err error)
}

type Side string

const (
	SideBuy  Side = "buy"
	SideSell Side = "sell"
)

type OrderSummary struct {
	OrderID       string
	Side          Side
	Success       bool
	FailureReason string
}

type OrderInput struct {
	Pair        string
	BaseAmount  float64
	QuoteAmount float64
}
