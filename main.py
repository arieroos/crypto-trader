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


def log(msg: str):
    print(f"[{datetime.now()}] {msg}", flush=True)


def open_short_position():
    lowest_market_price = None
    short = False
    trailing_stop = 0
    percentage = 1.0 / 100.0
    buy_adjustment = 1 - percentage
    stop_adjustment = 1 + percentage

    while redis_lib.last_trend() == DOWN_TREND:
        market_price = float(valr.market_summary()["lastTradedPrice"])
        if not lowest_market_price:
            lowest_market_price = market_price

        if not short and market_price <= lowest_market_price:
            sell_price = valr.sell_at_market()
            log(f"Sold at {sell_price}")
            short = True
            buy_price = sell_price * buy_adjustment
            log(f"Placing buy order at {buy_price}")
            valr.buy_order(buy_price)
            log("Buy order placed")

            trailing_stop = sell_price * stop_adjustment
            log(f"New trailing stop at {trailing_stop}")
            lowest_market_price = sell_price
        elif short:
            if market_price >= trailing_stop:
                close_short_positions()
                short = False
            elif len(valr.get_open_orders()) == 0:
                short = False
            elif market_price <= lowest_market_price:
                lowest_market_price = market_price
                trailing_stop = int(math.ceil(market_price * stop_adjustment))
                log(f"New trailing stop at {trailing_stop}")

        time.sleep(60)

    log("Trend is up again")


def close_short_positions():
    valr.close_open_buys()
    try:
        bp = valr.buy_at_market()
        log(f"Bought at {bp}")
    except Exception as err:
        error_handler.handle_exception(err)


if __name__ == "__main__":
    sys.excepthook = error_handler.excepthook

    market_summary = valr.market_summary()
    price = market_summary["lastTradedPrice"]
    redis_lib.save_price(price)

    long_periods, short_periods = 24, 6  # TODO: config
    long_prices, short_prices = redis_lib.last_prices(long_periods), redis_lib.last_prices(short_periods)
    if len(long_prices) != long_periods:
        log("incomplete data, not trading")
        redis_lib.save_trend(UNKNOWN_TREND)
        exit()
    log(f"Long prices: {long_prices}")

    long_mean, short_mean = statistics.mean(long_prices), statistics.mean(short_prices)

    last_trend = redis_lib.last_trend() or UNKNOWN_TREND
    if short_mean < long_mean:
        trend = DOWN_TREND
    elif short_mean > long_mean:
        trend = UP_TREND
    else:
        trend = last_trend
    redis_lib.save_trend(trend)
    log(f"Last trend: {last_trend}")
    log(f"Current trend: {trend}")

    if trend == last_trend or last_trend == UNKNOWN_TREND:
        log("No change in trend: not trading")
        exit()
    if trend == UP_TREND:
        log("BUY SIGNAL: closing short positions")
        close_short_positions()
    elif trend == DOWN_TREND:
        log("SELL SIGNAL: opening short position")
        open_short_position()
