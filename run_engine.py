import argparse
import json
import pandas as pd
import importlib
import logging
from engine.regimes.logic import detect_regime

logging.basicConfig(level=logging.INFO)


def load_strategy(logic_id, params):
    module = importlib.import_module(f"engine.strategies.{logic_id}")
    class_name = "".join([x.capitalize() for x in logic_id.split("_")])
    Strategy = getattr(module, class_name)
    return Strategy(params)


def run_engine(config_path):

    with open(config_path, "r") as f:
        config = json.load(f)

    df = pd.read_csv(config["data_file"])
    df["date"] = pd.to_datetime(df["date"])

    regime_cfg = config["regime_classifier"]
    strategies_cfg = config["strategies"]

    trades = []
    position = None

    regime_map = {
        "trend": "trend_following",
        "range": "range_play",
        "volatile": "volatility_breakout",
        "low_vol": "mean_reversion"
    }

    for i in range(60, len(df)-1):

        data_slice = df.iloc[:i+1]

        regime = detect_regime(data_slice, regime_cfg)

        strat_key = regime_map[regime]
        strat_cfg = strategies_cfg[strat_key]

        strategy = load_strategy(
            strat_cfg["logic_id"],
            strat_cfg["params"]
        )

        signal_df = strategy.generate_signals(data_slice)
        signal = signal_df["signal"].iloc[-1]

        next_open = df["open"].iloc[i+1]
        next_date = df["date"].iloc[i+1]

        if position is None and signal == 1:
            position = {
                "entry_dt": next_date,
                "entry_price": next_open,
                "strategy_used": strat_key,
                "regime": regime,
                "index": i+1
            }

        elif position and signal == -1:
            trades.append({
                "entry_dt": position["entry_dt"],
                "entry_price": position["entry_price"],
                "qty": 1,
                "side": "LONG",
                "strategy_used": position["strategy_used"],
                "regime": position["regime"],
                "exit_dt": next_date,
                "exit_price": next_open,
                "pnl": next_open - position["entry_price"],
                "bars_held": (i+1) - position["index"]
            })
            position = None

    trades_df = pd.DataFrame(trades)

    if not trades_df.empty:
        trades_df.sort_values("entry_dt", inplace=True)
        trades_df.to_excel("outputs/orders.xlsx", index=False)
        logging.info("Backtest completed. Orders saved.")

    else:
        logging.info("No trades generated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    run_engine(args.config)
