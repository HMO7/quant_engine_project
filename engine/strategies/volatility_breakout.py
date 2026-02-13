import ta
from engine.strategies.strategy_base import StrategyBase


class VolatilityBreakout(StrategyBase):

    def generate_signals(self, df):

        atr_window = self.params["atr_window"]
        multiplier = self.params["multiplier"]

        df = df.copy()

        df["atr"] = ta.volatility.AverageTrueRange(
            df["high"], df["low"], df["close"],
            window=atr_window
        ).average_true_range()

        df["prev_high"] = df["high"].shift(1)
        df["prev_low"] = df["low"].shift(1)

        df["signal"] = 0

        df.loc[
            df["high"] > df["prev_high"] + df["atr"] * multiplier,
            "signal"
        ] = 1

        df.loc[
            df["low"] < df["prev_low"] - df["atr"] * multiplier,
            "signal"
        ] = -1

        return df
