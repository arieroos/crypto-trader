package interfaces

type ExchangeAPI interface {
	LastTradedPrice(pair string) (float64, error)
}
