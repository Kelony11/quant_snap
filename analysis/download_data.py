import os
import yfinance as yf
import pandas as pd


def download(symbol, start, end):
    return yf.download(symbol, start=start, end=end)


def clean_df(df: pd.DataFrame):
    # If yfinance returns MultiIndex columns (e.g., ('Close','SPY')), flatten them
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Remove any column name labels like "Price" / "Ticker"
    df.columns.name = None

    # Ensure Adj Close exists (some versions omit it)
    if "Adj Close" not in df.columns:
        if "Close" in df.columns:
            df["Adj Close"] = df["Close"]
        else:
            raise RuntimeError("❌ Missing both 'Close' and 'Adj Close' columns.")

    return df


def save_clean_csv(df: pd.DataFrame, path: str):
    # Make Date a real column, not the index, and save a clean 1-row header CSV
    df_out = df.reset_index()  # creates Date column
    df_out.to_csv(path, index=False)


if __name__ == "__main__":
    # Make sure the folder exists
    os.makedirs("data", exist_ok=True)

    # Pick One ETF or/and Individual stock
    ETF = "SPY"
    STOCK = "AAPL"

    # 3+ years of daily data
    start, end = "2020-01-01", "2024-01-01"

    # -------- DOWNLOAD EFT --------------
    df_eft = download(ETF, start, end)
    df_eft = clean_df(df_eft)
    df_eft.to_csv(f"data/{ETF}.csv")
    print("Confirmed ✅", f"Saved data/{ETF}.csv | rows={len(df_eft)} | cols={list(df_eft.columns)}")

    # -------- DOWNLOAD STOCK --------------
    df_stock = download(STOCK, start, end)
    df_stock = clean_df(df_stock)
    df_stock.to_csv(f"data/{STOCK}.csv")
    print("Confirmed ✅", f"Saved data/{STOCK}.csv | rows={len(df_stock)} | cols={list(df_stock.columns)}")
