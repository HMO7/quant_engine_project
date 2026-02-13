import numpy as np
import ta


def detect_regime(df, config):

    atr_window = config["atr_window"]
    trend_ma = config["trend_ma"]

    df = df.copy()

    atr = ta.volatility.AverageTrueRange(
        df["high"], df["low"], df["close"],
        window=atr_window
    ).average_true_range()

    df["atr"] = atr
    df["ma"] = df["close"].rolling(trend_ma).mean()

    df.dropna(inplace=True)

    latest_close = df["close"].iloc[-1]
    latest_ma = df["ma"].iloc[-1]
    latest_atr = df["atr"].iloc[-1]

    high_vol = np.percentile(df["atr"], 70)
    low_vol = np.percentile(df["atr"], 30)

    if latest_atr > high_vol:
        return "volatile"

    if latest_atr < low_vol:
        return "low_vol"

    if latest_close > latest_ma:
        return "trend"

    return "range"
