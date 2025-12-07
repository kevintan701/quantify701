# Quantify 701 - AI-Powered Quantitative Investment Platform

**Quantify 701** is an AI-powered quantitative investment platform by **The Studio 701 LLC** that uses free data sources to select and analyze stocks based on technical analysis, quantitative filters, and artificial intelligence.

🌐 **Live App**: [https://quantify701.streamlit.app/](https://quantify701.streamlit.app/)  
📦 **GitHub**: [https://github.com/kevintan701/quantify701](https://github.com/kevintan701/quantify701)

## Features

### Core Features
- **🤖 AI-Powered Insights**: Comprehensive, supportive analysis with clear explanations beyond technical data
- **💰 Suggested Buy Price**: AI-calculated entry prices based on support levels, strategy, and technical indicators
- **📊 Time Range Filters**: Analyze stocks with customizable periods (1mo to 10y) and intervals (Daily, Weekly, Monthly, Quarterly)
- **🕯️ Candlestick Charts**: Professional OHLC price visualization with technical indicators overlay
- **Free Data Access**: Uses Yahoo Finance (yfinance) for real-time and historical stock data

### Stock Selection & Analysis
- **Quantitative Stock Selection**: Filters stocks based on multiple criteria:
  - Market capitalization
  - Trading volume
  - Technical indicators (RSI, MACD, Moving Averages, Bollinger Bands)
  - Momentum and volatility
- **Automated Trading Signals**: Generates buy/sell signals based on technical analysis
- **Composite Scoring System**: 8-factor scoring algorithm (0-100) for ranking stocks
- **Support Level Analysis**: Identifies key support levels (SMA 20/50, Bollinger Bands, recent lows)

### AI & Recommendations
- **Enhanced AI Recommendations**: Actionable recommendations with:
  - Multi-factor confidence scoring
  - Detailed reasoning beyond technical indicators
  - Risk level assessment with explanations
  - Time horizon recommendations
  - Supportive, clear explanations
- **Market Sentiment Analysis**: AI-powered overall market analysis
- **Portfolio Insights**: High-level analysis of selected stocks
- **Score Explanations**: Detailed breakdown of why stocks received their scores

### User Interface
- **Interactive Web UI**: Modern, responsive interface with smooth animations
- **Real-time Charts**: Interactive Plotly charts with technical indicators
- **Flexible Strategy Presets**: Multiple investment strategies:
  - Default (balanced approach)
  - Conservative (large-cap, low volatility)
  - Aggressive (higher risk/reward)
  - Momentum (trend-following)
  - Value (established companies)
  - Dividend Focus (income investing)
- **Customizable Filters**: Adjustable criteria for personalized analysis
- **Export Functionality**: Download results as CSV

## Installation

**🚀 Quick Start (No Docker Required!):**

**Option 1: Automated Setup (Easiest)**
```bash
./setup_local.sh
```

**Option 2: Manual Setup**
1. Create a virtual environment:
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

**💡 Docker is Optional:** The `Dockerfile` in this repo is only for deployment to cloud platforms. For local development, just use the virtual environment method above. See [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md) for details.

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

### Option 1: Interactive Web UI (Recommended) 🚀

**Quick Start:**
```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Run the app
streamlit run app.py
```

**Or use the convenience script:**
```bash
./run_app.sh
```

The app will automatically open in your browser at **`http://localhost:8501`**

**The web UI provides:**
- 📊 **Stock Rankings**: Interactive table with scores, signals, and key metrics
- 📈 **Top Recommendations**: BUY signals with suggested entry prices and AI insights
- 🔍 **Stock Details**: Comprehensive analysis with technical indicators and charts
- 🤖 **AI Insights**: Enhanced analysis with market context, sector trends, and risk assessment
- 💰 **Suggested Buy Prices**: AI-calculated entry prices based on support levels and strategy
- 🕯️ **Candlestick Charts**: Professional OHLC visualization (toggle between candlestick and line charts)
- ⏱️ **Time Range Controls**: Customize analysis period and data interval
- ⚙️ **Customizable Filters**: Strategy presets and adjustable criteria
- 📥 **Export Data**: Download results as CSV

**📖 See [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md) for detailed local setup instructions.**

**💡 Note:** You don't need Docker for local development! Just use a virtual environment (see above). Docker is only for deployment to certain cloud platforms.

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
- **Interactive web UI**: Modern Streamlit interface with smooth animations
- **Real-time charts**: Interactive Plotly charts with technical indicators
  - Candlestick charts (OHLC visualization)
  - Line charts (closing prices)
  - Technical indicators overlay (RSI, MACD, Moving Averages)
- **Time range controls**: Customizable period and interval selectors
- **Strategy presets**: Pre-configured investment strategies
- **Custom filters**: Adjustable quantitative criteria
- **Suggested buy prices**: Display AI-calculated entry prices
- **Enhanced AI insights**: Comprehensive analysis integration
- **Export functionality**: CSV download capability

### `ai_insights.py` ⭐
- **AI-powered stock analysis**: Comprehensive, supportive insights with clear explanations
- **Suggested buy price calculation**: Calculates entry prices based on:
  - Support levels (SMA 20/50, Bollinger Bands, recent lows)
  - Strategy-based adjustments (Conservative, Aggressive, etc.)
  - RSI-based timing recommendations
  - Price range calculations based on volatility
- **Enhanced recommendations**: Multi-factor confidence scoring with detailed reasoning
- **Market sentiment analysis**: Overall market conditions assessment
- **Portfolio-level insights**: High-level analysis of selected stocks
- **Score explanations**: Detailed breakdown of quantitative scores
- **Market context**: Sector analysis, market cap considerations, risk factors

### `data_fetcher.py`
- Fetches stock data from Yahoo Finance with customizable periods and intervals
- Calculates technical indicators:
  - Moving Averages (SMA 20, 50, 200)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - Volume indicators
  - Momentum and volatility
- Provides intelligent caching to minimize API calls
- Supports multiple time ranges (1mo to 10y) and intervals (Daily, Weekly, Monthly, Quarterly)

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

## Key Features in Detail

### Suggested Buy Price Calculation
The AI calculates suggested entry prices based on:
- **Support Levels**: Identifies key support from SMA 20/50, Bollinger Lower Band, and recent lows
- **Strategy Adjustments**: Applies strategy-specific multipliers (Conservative = 98%, Aggressive = 102%, etc.)
- **RSI Timing**: Adjusts for oversold/overbought conditions
- **Volatility-Based Range**: Calculates price range based on historical volatility
- **Current Price Comparison**: Shows discount/premium percentage

### Enhanced AI Insights
Provides comprehensive analysis including:
- **Technical Analysis**: Clear explanations of RSI, momentum, volume with context
- **Market Context**: Sector-specific insights, market cap considerations
- **Risk Assessment**: Volatility analysis with actionable recommendations
- **Non-Technical Factors**: Sector trends, economic considerations, risk factors
- **Supportive Tone**: Clear, actionable explanations that go beyond technical data

### Time Range Flexibility
- **Period Options**: 1 Month, 3 Months, 6 Months, 1 Year, 2 Years, 5 Years, 10 Years, Year to Date, Maximum Available
- **Interval Options**: Daily (most detailed), Weekly, Monthly, Quarterly (smoothed)
- **Use Cases**: 
  - Short-term: 1-3 months with daily intervals
  - Medium-term: 6 months-1 year with daily/weekly
  - Long-term: 2-10 years with weekly/monthly
  - Trend analysis: Longer periods with weekly/monthly intervals

### Chart Visualization
- **Candlestick Charts**: Professional OHLC visualization showing open, high, low, close
- **Line Charts**: Simple closing price visualization
- **Technical Overlays**: Moving averages, RSI, MACD indicators
- **Interactive Features**: Hover tooltips, zoom, pan capabilities

## Future Enhancements

- Backtesting functionality
- More sophisticated strategies (mean reversion, momentum, etc.)
- Portfolio optimization
- Real-time alerts
- Integration with broker APIs for live trading
- News sentiment analysis
- Predictive price forecasting
- Natural language queries about stocks

## License

This project is for educational purposes. Use at your own risk.

