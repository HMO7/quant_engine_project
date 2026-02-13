from engine.strategies.strategy_base import StrategyBase


class RangePlay(StrategyBase):

    def generate_signals(self, df):

        lookback = self.params["lookback"]

        df = df.copy()

        df["range_high"] = df["high"].rolling(lookback).max()
        df["range_low"] = df["low"].rolling(lookback).min()

        df["signal"] = 0

        df.loc[df["close"] <= df["range_low"], "signal"] = 1
        df.loc[df["close"] >= df["range_high"], "signal"] = -1

        return df
