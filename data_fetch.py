import yfinance as yf
import pandas as pd

df = yf.download("BTC-USD", period="6mo", interval="1d")

# fix multi index issue
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df.reset_index(inplace=True)
df.columns = [c.lower() for c in df.columns]

df.to_csv("data/ohlc_clean.csv", index=False)

print("Data downloaded successfully!")
