package shared

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
	Side Side
	Pair string
	// The base amount to apply to the order.
	// If the order only needs one amount, and the base amount is not 0, it will be preferred over the quote amount.
	BaseAmount float64
	// The quote  amount to apply to the order.
	// If the order only needs one amount, the quote amount will only be used if the base amount is exactly 0.
	QuoteAmount float64
}
