from engine.strategies.strategy_base import StrategyBase


class TrendFollowing(StrategyBase):

    def generate_signals(self, df):

        fast = self.params["fast_ma"]
        slow = self.params["slow_ma"]

        df = df.copy()

        df["fast_ma"] = df["close"].rolling(fast).mean()
        df["slow_ma"] = df["close"].rolling(slow).mean()

        df["signal"] = 0

        df.loc[
            (df["fast_ma"] > df["slow_ma"]) &
            (df["fast_ma"].shift(1) <= df["slow_ma"].shift(1)),
            "signal"
        ] = 1

        df.loc[
            (df["fast_ma"] < df["slow_ma"]) &
            (df["fast_ma"].shift(1) >= df["slow_ma"].shift(1)),
            "signal"
        ] = -1

        return df
