import statistics

import redis_lib
import valr

UNKNOWN_TREND = "unknown"
DOWN_TREND = "down"
UP_TREND = "up"

if __name__ == "__main__":
    price = valr.market_summary()["lastTradedPrice"]

    redis_lib.save_price(price)

    long_periods, short_periods = 20, 5
    long_prices, short_prices = redis_lib.last_prices(20), redis_lib.last_prices(5)
    if len(long_prices) != long_periods:
        print("incomplete data, not trading")
        redis_lib.save_trend(UNKNOWN_TREND)
        exit()

    long_mean, short_mean = statistics.mean(long_prices), statistics.mean(short_prices)

    last_trend = redis_lib.last_trend() or UNKNOWN_TREND
    if short_mean < long_mean:
        trend = DOWN_TREND
    elif short_mean > long_mean:
        trend = UP_TREND
    else:
        trend = last_trend
    redis_lib.save_trend(trend)

    if trend == last_trend or last_trend == UNKNOWN_TREND:
        print("No change in trend: not trading")
        exit()
    if trend == UP_TREND:
        print("BUY SIGNAL")
    elif trend == DOWN_TREND:
        print("SELL SIGNAL")
