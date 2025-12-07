# Quantify - AI-Powered Quantitative Investment Platform

**Quantify** is an AI-powered quantitative investment platform by **The Studio 701 LLC** that uses free data sources to select and analyze stocks based on technical analysis, quantitative filters, and artificial intelligence.

## Features

- **🤖 AI-Powered Insights**: Intelligent analysis, recommendations, and market sentiment
- **Free Data Access**: Uses Yahoo Finance (yfinance) for real-time and historical stock data
- **Quantitative Stock Selection**: Filters stocks based on multiple criteria:
  - Market capitalization
  - Trading volume
  - Technical indicators (RSI, MACD, Moving Averages)
  - Momentum and volatility
- **Automated Trading Signals**: Generates buy/sell signals based on technical analysis
- **AI Recommendations**: Actionable recommendations with confidence levels and risk assessment
- **Market Sentiment Analysis**: AI-powered overall market analysis
- **Interactive Web UI**: Modern, responsive interface with real-time charts
- **Flexible Strategy Presets**: Multiple investment strategies (Conservative, Aggressive, Momentum, Value, Dividend)
- **Customizable Filters**: Adjustable criteria for personalized analysis

## Installation

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

**Note**: If you're using Python 3.14+ on macOS, you may need to use a virtual environment due to externally-managed environment restrictions.

## Configuration

Edit `config.py` to customize:
- Stock universe (list of stocks to analyze)
- Selection criteria (market cap, volume, price filters)
- Trading parameters (position sizes, stop-loss, take-profit)
- Risk management settings

## Usage

**Important**: Make sure your virtual environment is activated before running:
```bash
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### Option 1: Interactive Web UI (Recommended)

Run the Streamlit web application for an interactive, user-friendly interface:

```bash
streamlit run app.py
```

Or use the convenience script:
```bash
./run_app.sh
```

The web UI provides:
- 📊 Interactive stock rankings table
- 📈 Real-time charts with technical indicators
- 🔍 Detailed stock analysis
- ⚙️ Customizable filters and settings
- 📥 Export data to CSV

The app will open in your default web browser at `http://localhost:8501`

### Option 2: Deploy as Public Web App 🌐

**The app is already web-based!** To make it publicly accessible on the internet, see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

**Quick Deploy (Streamlit Cloud - Free):**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy with one click!

Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

### Option 3: Command Line Interface

Run the main script for terminal output:
```bash
python main.py
```

The system will:
1. Fetch data for all stocks in the universe
2. Filter and rank stocks based on quantitative criteria
3. Generate buy signals for qualified stocks
4. Display detailed analysis and recommendations

## System Components

### `app.py` ⭐
- Interactive web UI built with Streamlit
- Real-time charts and visualizations
- Interactive filtering and analysis
- User-friendly dashboard interface
- AI insights integration

### `ai_insights.py` ⭐ NEW
- AI-powered stock analysis and insights
- Market sentiment analysis
- Intelligent recommendations with confidence levels
- Score explanations and risk assessment
- Portfolio-level insights

### `data_fetcher.py`
- Fetches stock data from Yahoo Finance
- Calculates technical indicators (RSI, MACD, Bollinger Bands, etc.)
- Provides caching to minimize API calls

### `stock_selector.py`
- Applies quantitative filters to stock universe
- Ranks stocks based on composite scoring system
- Filters by market cap, volume, price, and technical indicators

### `trading_strategy.py`
- Generates buy/sell signals based on technical analysis
- Calculates optimal position sizes
- Implements risk management rules

### `main.py`
- Command-line interface for stock selection
- Runs analysis cycles
- Displays results in terminal

## Example Output

```
============================================================
Quantitative Trading System - Analysis Cycle
Date: 2024-01-15 10:30:00
============================================================

[Step 1] Filtering and ranking stocks...
Evaluating 36 stocks...
Found 15 qualified stocks

Top 10 Stock Candidates:
------------------------------------------------------------
1. AAPL   | Score:  85.0 | Price: $185.50 | RSI:  45.2 | Momentum:  3.2%
2. MSFT   | Score:  82.5 | Price: $380.20 | RSI:  48.1 | Momentum:  2.8%
...

[Step 2] Generating buy signals...
BUY signal: AAPL - RSI at 45.2 (oversold/neutral); Price above moving averages (uptrend); MACD bullish crossover

[Step 3] Executing buy orders...
Bought 50 shares of AAPL at $185.50 (Total: $9,275.00)

[Step 4] Checking existing positions for sell signals...

[Step 5] Portfolio Summary
============================================================
Cash: $90,725.00
Positions Value: $9,275.00
Total Portfolio Value: $100,000.00
Initial Capital: $100,000.00
Total Return: $0.00 (0.00%)
Number of Positions: 1
```

## Customization

### Adding More Stocks
Edit `config.py` and add symbols to `STOCK_UNIVERSE`:
```python
STOCK_UNIVERSE = [
    "AAPL", "MSFT", "GOOGL", 
    # Add your stocks here
]
```

### Adjusting Selection Criteria
Modify filters in `config.py`:
```python
MIN_MARKET_CAP = 10_000_000_000  # Minimum market cap
MIN_VOLUME = 1_000_000  # Minimum daily volume
MIN_RSI = 30  # Minimum RSI threshold
MAX_RSI = 70  # Maximum RSI threshold
```

### Changing Trading Parameters
Update risk management settings:
```python
STOP_LOSS_PCT = 0.05  # 5% stop loss
TAKE_PROFIT_PCT = 0.15  # 15% take profit
MAX_POSITION_SIZE = 0.10  # Max 10% per position
```

## Notes

- This is a **paper trading** system - it does not execute real trades
- Always test strategies thoroughly before using real money
- Market conditions change - regularly review and adjust parameters
- Free data sources may have rate limits or delays
- Past performance does not guarantee future results

## Future Enhancements

- Backtesting functionality
- More sophisticated strategies (mean reversion, momentum, etc.)
- Portfolio optimization
- Real-time alerts
- Integration with broker APIs for live trading

## License

This project is for educational purposes. Use at your own risk.

