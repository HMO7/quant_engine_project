# Quant Regime-Based Strategy Engine

## Overview

This project implements a **modular quantitative backtesting engine** that dynamically selects trading strategies based on detected market regimes.

At the start of each trading day, the engine:

1. Detects the current market regime (Trend / Range / Volatile / Low Volatility)
2. Automatically selects the correct strategy
3. Generates signals without look-ahead bias
4. Executes trades at next-day open
5. Logs all trades into an Excel file

The system is designed to simulate a **mini hedge-fund style trading engine** with scalable architecture.

---

## Features

* Modular strategy architecture (plug-and-play)
* Regime-based dynamic strategy switching
* JSON-driven configuration
* No hardcoded parameters
* No look-ahead bias
* Next-day open trade execution
* Excel trade log output
* Clean object-oriented structure

---

## Project Structure

```
project/
│
├── data/
│   └── ohlc_clean.csv
│
├── configs/
│   └── engine.json
│
├── engine/
│   ├── regimes/
│   │   └── logic.py
│   │
│   └── strategies/
│       ├── strategy_base.py
│       ├── trend_following.py
│       ├── mean_reversion.py
│       ├── volatility_breakout.py
│       └── range_play.py
│
├── outputs/
│   └── orders.xlsx
│
├── docs/
│   └── research_notes.md
│
├── data_fetch.py
├── run_engine.py
└── README.md
```

---

## Market Data

* Instrument: **BTC-USD**
* Timeframe: **1 Day**
* Period: **Last 6 Months**
* Source: Yahoo Finance (`yfinance`)

---

## Regime Classification

Market regimes are detected using:

* ATR (Average True Range) → volatility measurement
* Moving Average → trend detection

### Possible regimes:

* `trend`
* `range`
* `volatile`
* `low_vol`

### Regime → Strategy Mapping

| Regime   | Strategy            |
| -------- | ------------------- |
| trend    | trend_following     |
| range    | range_play          |
| volatile | volatility_breakout |
| low_vol  | mean_reversion      |

---

## Strategies Implemented

### Trend Following (MA Crossover)

* Buy when fast MA crosses above slow MA
* Sell when fast MA crosses below slow MA

### Mean Reversion (RSI)

* Buy when RSI is low
* Exit when RSI is high

### Volatility Breakout

* ATR-based breakout strategy

### Range Play

* Buy near range low
* Sell near range high

---

## Configuration (JSON Driven)

All parameters are controlled via:

```
configs/engine.json
```

This allows:

* Easy tuning
* Strategy modification without editing engine code
* Scalability for adding STRAT_5, STRAT_6, etc.

---

## How To Run

### 1. Install dependencies

```bash
pip install pandas numpy ta yfinance openpyxl
```

---

### 2. Download Market Data

```bash
python data_fetch.py
```

---

### 3. Run Engine

```bash
python run_engine.py --config configs/engine.json
```

---

## Output

After execution:

```
outputs/orders.xlsx
```

### Output Columns

* entry_dt
* entry_price
* qty
* side
* strategy_used
* regime
* exit_dt
* exit_price
* pnl
* bars_held

---

## Engineering Highlights

* Object-Oriented Design
* Dynamic strategy loading
* Config-driven architecture
* Clean separation of concerns
* Scalable framework

---

## Backtesting Assumptions

* Trades executed at next-day open
* Quantity = 1
* No look-ahead bias
* Indicator calculations use historical data only

---

## Future Improvements

* Transaction cost & slippage modeling
* Position sizing & risk management
* Sharpe ratio / drawdown metrics
* Multi-asset support
* Regime smoothing filters

---

## Author

Quant Developer Assignment Project
Built as a modular regime-based trading engine.
