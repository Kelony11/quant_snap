import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl

DATA_DIR = "data"
OUT_DIR = "output"

ETF = "SPY"
STOCK = "AAPL"


def load_price_series(ticker: str):
    """
    Loads one CSV and returns a clean Adj Close price series indexed by Date.
    """
    # Uses the Part 1 CSVs:
    path = os.path.join(DATA_DIR, f"{ticker}.csv")
    df = pd.read_csv(path)

    # Parse Date
    df["Date"] = pd.to_datetime(df["Date"])

    # Make sure Adj Close exists
    if "Adj Close" not in df.columns:
        raise RuntimeError(f"Missing 'Adj Close' in {path}")

    # Convert Adj Close to numeric
    df["Adj Close"] = pd.to_numeric(df["Adj Close"], errors="coerce")

    # Drop bad rows
    df = df.dropna(subset=["Date", "Adj Close"]).sort_values("Date")

    # Use Date as index
    series = df.set_index("Date")["Adj Close"]
    series.name = ticker
    return series


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # load Adj Close series, for both tickers
    etf_price = load_price_series(ETF)
    stock_price = load_price_series(STOCK)

    # Align on the same dates - Only keep overlapping trading dates
    prices = pd.concat([etf_price, stock_price], axis=1).dropna()

    # Compute daily returns
    returns = prices.pct_change().dropna()

    # Rolling volatility (eg. 20 day)
    window = 20
    rolling_vol = returns.rolling(window).std()

    # PLOT 1: ------ PRICE HISTORY -------

    plt.figure()
    plt.plot(prices.index, prices[ETF], label=ETF)
    plt.plot(prices.index, prices[STOCK], label=STOCK)

    pl.title("Price History (Adj Close)")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(OUT_DIR, "price_history.png"), dpi=200)
    plt.close()

    # PLOT 2: ------ ROLLING VOLATILITY COMPARISON -------

    plt.figure()
    plt.plot(rolling_vol.index, rolling_vol[ETF], label=f"{ETF} (20d vol)")
    plt.plot(rolling_vol.index, rolling_vol[STOCK], label=f"{STOCK} (20d vol)")

    pl.title("Rolling Volatility (20-day, Daily)")
    plt.xlabel("Date")
    plt.ylabel("Volatility (daily std dev)")
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(OUT_DIR, "volatility.png"), dpi=200)
    plt.close()

    # Print a quick summary

    print("DONE ✅", "Part 2 complete")
    print("Saved:", os.path.join(OUT_DIR, "price_history.png"))
    print("Saved:", os.path.join(OUT_DIR, "volatility.png"))
    print("\nReturn stats (daily):")
    print(returns.describe())


if __name__ == "__main__":
    main()
