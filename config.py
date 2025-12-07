"""
Configuration file for the quantitative trading system.
Contains all adjustable parameters for data fetching, stock selection, and trading.
"""

# Data fetching settings
DATA_SOURCE = "yfinance"  # Using Yahoo Finance (free)
LOOKBACK_PERIOD_DAYS = 252  # 1 year of trading days for analysis
UPDATE_INTERVAL_HOURS = 1  # How often to refresh data

# Stock universe settings
# Start with S&P 500 stocks (can be expanded)
STOCK_UNIVERSE = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B",
    "V", "JNJ", "WMT", "JPM", "MA", "PG", "UNH", "HD", "DIS", "BAC",
    "ADBE", "NFLX", "PYPL", "CMCSA", "KO", "NKE", "MRK", "PFE", "T",
    "INTC", "VZ", "CSCO", "XOM", "CVX", "ABT", "COST", "AVGO", "TMO"
]

# Stock selection criteria (quantitative filters)
MIN_MARKET_CAP = 10_000_000_000  # Minimum $10B market cap
MIN_VOLUME = 1_000_000  # Minimum daily volume
MIN_PRICE = 5.0  # Minimum stock price ($)
MAX_PRICE = 1000.0  # Maximum stock price ($)

# Technical indicators thresholds
MIN_RSI = 25  # Minimum RSI (allows more oversold stocks)
MAX_RSI = 75  # Maximum RSI (allows slightly overbought)
MIN_MOMENTUM_DAYS = 20  # Days for momentum calculation

# Additional selection criteria
MIN_VOLUME_RATIO = 0.5  # Minimum volume ratio (vs 20-day average)
MIN_DATA_POINTS = 200  # Minimum historical data points required
MAX_VOLATILITY = 0.05  # Maximum daily volatility (5%)
MIN_TREND_STRENGTH = 0.02  # Minimum price trend strength (2% above MA)

# Trading strategy parameters
INITIAL_CAPITAL = 100_000  # Starting capital in USD
MAX_POSITION_SIZE = 0.10  # Maximum 10% of portfolio per stock
MIN_POSITION_SIZE = 0.02  # Minimum 2% of portfolio per stock
MAX_POSITIONS = 10  # Maximum number of concurrent positions

# Risk management
STOP_LOSS_PCT = 0.05  # 5% stop loss
TAKE_PROFIT_PCT = 0.15  # 15% take profit
MAX_PORTFOLIO_RISK = 0.20  # Maximum 20% portfolio risk

# Rebalancing settings
REBALANCE_FREQUENCY_DAYS = 30  # Rebalance every 30 days
MIN_HOLDING_PERIOD_DAYS = 5  # Minimum days to hold a position

