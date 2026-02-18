import os
import pandas as pd
import matplotlib.pyplot as plt
import json

# Importing PART 2 functions to avoid duplicate code
from part2_analysis import load_price_series

DATA_DIR = "data"
OUT_DIR = "output"

ETF = "SPY"
STOCK = "AAPL"

SHORT_W, LONG_W = 20, 50


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # load prices (Adj Close) using part 2 function
    etf_price = load_price_series(ETF)
    stock_price = load_price_series(STOCK)

    # Strategy on the stock (AAPL)
    prices = pd.concat([stock_price], axis=1).dropna()[STOCK]

    # Daily returns
    returns = prices.pct_change().dropna()

    # Moving averages
    ma_short = prices.rolling(SHORT_W).mean()
    ma_long = prices.rolling(LONG_W).mean()

    # Signal: 1 when short MA > long MA else 0
    signal = (ma_short > ma_long).astype(int)

    # No look-ahead: position uses yesterday's signal
    position = signal.shift(1).fillna(0)

    # Strategy returns
    strategy_returns = position.loc[returns.index] * returns

    # Equity curves (starts at $1)
    equity_strategy = (1 + strategy_returns).cumprod()
    equity_buy_hold = (1 + returns).cumprod()

    # Metrics
    total_return_strategy = equity_strategy.iloc[-1] - 1
    total_return_buy_hold = equity_buy_hold.iloc[-1] - 1

    vol_strategy = strategy_returns.std()
    vol_buy_hold = returns.std()

    invested_percentage = position.mean()

    metrics = {
        "strategy": {
            "name": f"MOVING AVERAGE CROSSOVER: ({SHORT_W} vs {LONG_W}) long-only",
            "ticker": STOCK,
            "start_date": str(equity_strategy.index.min().date()),
            "end_date": str(equity_strategy.index.max().date()),
            "total_return": float(total_return_strategy),
            "daily_volatility": float(vol_strategy),
            "percent_time_in_market": float(invested_percentage),
        },

        "buy_and_hold": {
            "ticker": STOCK,
            "total_return": float(total_return_buy_hold),
            "daily_volatility": float(vol_buy_hold),
        }
    }

    # Save metrics
    json_output = os.path.join(OUT_DIR, 'metrics_part3.json')

    with open(json_output, "w") as file:
        json.dump(metrics, file, indent=2)

    # Plot equity curve
    plt.plot(equity_buy_hold.index, equity_buy_hold.values, label="Buy & Hold (AAPL)")
    plt.plot(equity_strategy.index, equity_strategy.values, label=f"Strategy Moving Average ({SHORT_W}, {LONG_W})")
    plt.title("Strategy Equity Curve (Start = $1.00)")
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.legend()
    plt.tight_layout()

    plot_output = os.path.join(OUT_DIR, "strategy_equity.png")
    plt.savefig(plot_output, dpi=200)
    plt.close()

    print("DONE ✅", "Part 3 Complete")
    print("Saved:", plot_output)
    print("Saved:", json_output)
    print("\nMetrics Preview:")
    print(metrics)


if __name__ == "__main__":
    main()




