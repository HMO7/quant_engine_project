import ta
from engine.strategies.strategy_base import StrategyBase


class MeanReversion(StrategyBase):

    def generate_signals(self, df):

        window = self.params["rsi_window"]
        buy = self.params["rsi_buy"]
        sell = self.params["rsi_sell"]

        df = df.copy()

        df["rsi"] = ta.momentum.RSIIndicator(
            df["close"], window
        ).rsi()

        df["signal"] = 0

        df.loc[df["rsi"] < buy, "signal"] = 1
        df.loc[df["rsi"] > sell, "signal"] = -1

        return df
