import math
import statistics
import sys
import time
from datetime import datetime

import error_handler
import redis_lib
import valr

UNKNOWN_TREND = "unknown"
DOWN_TREND = "down"
UP_TREND = "up"


def open_short_position():
    sell_price = valr.sell_at_market()
    print(f"Sold at {sell_price}")
    buy_price = int(math.ceil(0.985 * sell_price))
    while True:
        print(f"Attempting to buy at {buy_price}")
        oid = valr.buy_order(buy_price)
        if valr.order_placed(oid):
            print(f"Buy order successfully placed: {oid}")
            break
        else:
            if valr.lowest_ask() <= buy_price or redis_lib.last_trend() == UP_TREND:
                try:
                    actual_buy_price = valr.buy_at_market()
                    print(f"Bought at {actual_buy_price}")
                except Exception as err:
                    print(f"{type(err)}: {err}")
                break
            else:
                sec_wait = 5
                print(f"Unfavourable market, trying again in {sec_wait} seconds")
                time.sleep(sec_wait)


def close_short_positions():
    valr.close_open_buys()
    try:
        bp = valr.buy_at_market()
        print(f"Bought at {bp}")
    except Exception as err:
        print(f"{type(err)}: {err}")


if __name__ == "__main__":
    sys.excepthook = error_handler.excepthook

    print(datetime.now())

    market_summary = valr.market_summary()
    price = market_summary["lastTradedPrice"]
    redis_lib.save_price(price)

    long_periods, short_periods = 20, 5  # TODO: config
    long_prices, short_prices = redis_lib.last_prices(long_periods), redis_lib.last_prices(short_periods)
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
        print("BUY SIGNAL: closing short positions")
        close_short_positions()
    elif trend == DOWN_TREND:
        print("SELL SIGNAL: opening short position")
        open_short_position()
