import math
import statistics
import time
from datetime import datetime

import redis_lib
import valr

UNKNOWN_TREND = "unknown"
DOWN_TREND = "down"
UP_TREND = "up"


def open_sell_position():
    sell_price = valr.sell_at_market()
    print(f"Sold at {sell_price}")
    buy_price = int(math.ceil(0.98 * sell_price))
    while True:
        print(f"Attempting to buy at {buy_price}")
        oid = valr.buy_order(buy_price)
        if valr.order_placed(oid):
            print(f"Buy order successfully placed: {oid}")
            break
        else:
            # if any sell order at or below my price
            #        buy
            #        break loop
            #    elif trend is up
            #        buy at market
            #        break loop
            #    else
            #        wait 4 seconds
            time.sleep(4)
    pass


def close_sell_position():
    # close any unfilled buy orders
    # buy at market
    pass


if __name__ == "__main__":
    print(datetime.now())

    market_summary = valr.market_summary()
    price = market_summary["lastTradedPrice"]
    redis_lib.save_price(price)

    long_periods, short_periods = 20, 5
    long_prices, short_prices = redis_lib.last_prices(20), redis_lib.last_prices(5)
    if len(long_prices) != long_periods:
        print("incomplete data, not trading")
        redis_lib.save_trend(UNKNOWN_TREND)
        exit()
    print(f"long prices: {long_prices}")

    long_mean, short_mean = statistics.mean(long_prices), statistics.mean(short_prices)

    last_trend = redis_lib.last_trend() or UNKNOWN_TREND
    if short_mean < long_mean:
        trend = DOWN_TREND
    elif short_mean > long_mean:
        trend = UP_TREND
    else:
        trend = last_trend
    redis_lib.save_trend(trend)
    print(f"Last trend: {last_trend}")
    print(f"Current trend: {trend}")

    if trend == last_trend or last_trend == UNKNOWN_TREND:
        print("No change in trend: not trading")
        exit()
    if trend == UP_TREND:
        close_sell_position()
    elif trend == DOWN_TREND:
        open_sell_position()
