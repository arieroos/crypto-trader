import redis_lib
import valr

price = valr.market_summary()["lastTradedPrice"]

redis_lib.save_price(price)

print(redis_lib.last_prices(6))
