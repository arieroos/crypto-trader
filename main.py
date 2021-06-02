import statistics

import redis_lib
import valr

price = valr.market_summary()["lastTradedPrice"]

redis_lib.save_price(price)

long_periods, short_periods = 20, 5
long_prices, short_prices = redis_lib.last_prices(20), redis_lib.last_prices(5)
long_mean, short_mean = statistics.mean(long_prices), statistics.mean(short_prices)
