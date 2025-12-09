# 📈 Quantify 701 - AI-Powered Quantitative Investment Platform

<div align="center">

**A comprehensive quantitative stock analysis platform that combines technical analysis, AI-powered insights, and interactive data visualization to help investors make informed decisions.**

[![Live App](https://img.shields.io/badge/Live%20App-Streamlit%20Cloud-blue?style=for-the-badge&logo=streamlit)](https://quantify701.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/kevintan701/quantify701)
[![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-yellow?style=for-the-badge)](LICENSE)

🌐 **Live Demo**: [https://quantify701.streamlit.app/](https://quantify701.streamlit.app/)  
📦 **Repository**: [https://github.com/kevintan701/quantify701](https://github.com/kevintan701/quantify701)

</div>

---

## 🎯 Project Overview

**Quantify 701** is a full-stack quantitative investment analysis platform that empowers investors with AI-driven stock selection, technical analysis, and actionable insights. Built with Python and Streamlit, the platform provides a modern, interactive web interface for analyzing stocks using quantitative filters, technical indicators, and intelligent recommendations.

### Key Highlights

- 🤖 **AI-Powered Analysis**: Intelligent stock recommendations with multi-factor confidence scoring
- 📊 **Advanced Technical Analysis**: 8-factor composite scoring system with 10+ technical indicators
- 💰 **Smart Entry Pricing**: AI-calculated suggested buy prices based on support levels and strategy
- 🕯️ **Professional Visualizations**: Interactive candlestick charts with technical indicator overlays
- ⚡ **Flexible Time Ranges**: Support for intraday (1m-1h) to long-term (10y) analysis periods
- 🎨 **Modern UI/UX**: Responsive web interface with smooth animations and intuitive design
- 🔄 **Adaptive Filtering**: Intelligent data point requirements that adjust based on time range
- 📈 **Multiple Strategies**: Pre-configured investment strategies (Conservative, Aggressive, Momentum, Value, Dividend)

## 🚀 Features

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

## 🛠️ Technologies Used

### Backend & Data Processing
- **Python 3.8+**: Core programming language
- **yfinance**: Free stock market data from Yahoo Finance
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations

### Frontend & Visualization
- **Streamlit**: Interactive web application framework
- **Plotly**: Interactive charts and visualizations
- **Custom CSS**: Modern, responsive UI design

### Technical Analysis
- **RSI (Relative Strength Index)**: Momentum oscillator
- **MACD**: Moving Average Convergence Divergence
- **Moving Averages**: SMA 20, 50, 200
- **Bollinger Bands**: Volatility indicators
- **Volume Analysis**: Volume ratios and confirmation
- **Momentum Indicators**: Price momentum and trend strength

### AI & Machine Learning
- **Rule-based AI System**: Intelligent recommendation engine
- **Multi-factor Scoring**: Composite 0-100 scoring algorithm
- **Risk Assessment**: Automated risk level calculation
- **Market Sentiment Analysis**: Overall market condition evaluation

## 📋 Installation

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

## ⚙️ Configuration

Edit `config.py` to customize:
- Stock universe (list of stocks to analyze)
- Selection criteria (market cap, volume, price filters)
- Trading parameters (position sizes, stop-loss, take-profit)
- Risk management settings

## 💻 Usage

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

## 🏗️ Architecture & System Components

The platform follows a modular architecture with clear separation of concerns:

### Core Modules

### `app.py` ⭐ **Main Application**
- **Interactive web UI**: Modern Streamlit interface with smooth animations and responsive design
- **Real-time charts**: Interactive Plotly charts with technical indicators
  - Candlestick charts (OHLC visualization)
  - Line charts (closing prices)
  - Technical indicators overlay (RSI, MACD, Moving Averages)
- **Time range controls**: Customizable period and interval selectors with adaptive data point calculation
- **Strategy presets**: Pre-configured investment strategies (6 different strategies)
- **Custom filters**: Adjustable quantitative criteria with real-time updates
- **Suggested buy prices**: Display AI-calculated entry prices with support level analysis
- **Enhanced AI insights**: Comprehensive analysis integration with market context
- **Export functionality**: CSV download capability for further analysis
- **Caching system**: Intelligent data caching to minimize API calls and improve performance

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

### `data_fetcher.py` **Data Management**
- **Data fetching**: Retrieves stock data from Yahoo Finance with customizable periods and intervals
- **Technical indicators calculation**:
  - Moving Averages (SMA 20, 50, 200)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands (Upper, Middle, Lower)
  - Volume indicators (Volume Ratio, Volume SMA)
  - Momentum and volatility metrics
- **Intelligent caching**: Reduces API calls with configurable cache timeout (default: 1 hour)
- **Multi-interval support**: Handles intraday (1m-1h) to long-term (10y) data ranges
- **Error handling**: Robust error handling for network issues and data availability

### `stock_selector.py` **Stock Filtering & Ranking**
- **Quantitative filtering**: Applies multiple criteria to filter stock universe
- **Composite scoring system**: 8-factor algorithm (0-100) that evaluates:
  1. Momentum (0-25 points)
  2. RSI positioning (0-20 points)
  3. Moving average trends (0-20 points)
  4. MACD signals (0-15 points)
  5. Volume confirmation (0-12 points)
  6. Volatility assessment (0-8 points)
  7. Momentum consistency (0-8 points)
  8. Bollinger Bands position (0-7 points)
- **Multi-criteria filtering**: Market cap, volume, price, RSI, volatility, volume ratio
- **Adaptive data requirements**: Adjusts minimum data points based on period/interval
- **Ranking system**: Sorts stocks by composite score for easy identification of top opportunities

### `trading_strategy.py` **Signal Generation**
- **Buy/sell signals**: Generates trading signals based on technical analysis
- **Position sizing**: Calculates optimal position sizes based on risk parameters
- **Risk management**: Implements stop-loss, take-profit, and portfolio risk rules
- **Signal confidence**: Provides confidence levels for each trading signal

### `ai_insights.py` ⭐ **AI Analysis Engine**
- **Stock insights**: Comprehensive analysis with market context and sector trends
- **Recommendations**: Multi-factor confidence scoring with detailed reasoning
- **Buy price calculation**: AI-calculated entry prices using support levels and strategy
- **Market sentiment**: Overall market condition assessment
- **Risk assessment**: Automated risk level calculation with explanations
- **Score explanations**: Detailed breakdown of quantitative scores

### `main.py` **CLI Interface**
- **Command-line interface**: Terminal-based stock selection and analysis
- **Batch processing**: Runs analysis cycles for multiple stocks
- **Formatted output**: Displays results in readable terminal format
- **Useful for**: Automated scripts, cron jobs, and server-side processing

## 📊 Project Structure

```
quantify701/
├── app.py                 # Main Streamlit web application
├── ai_insights.py         # AI-powered analysis and recommendations
├── data_fetcher.py        # Data fetching and technical indicators
├── stock_selector.py      # Stock filtering and scoring system
├── trading_strategy.py    # Trading signal generation
├── portfolio.py          # Portfolio management (optional)
├── main.py               # CLI interface
├── config.py             # Configuration parameters
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── DEPLOYMENT.md         # Deployment instructions
└── .streamlit/           # Streamlit configuration
    └── config.toml
```

## 📸 Example Output

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

## 🎨 Customization

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

## ⚠️ Important Notes & Disclaimers

- **Paper Trading System**: This platform does not execute real trades - it's for analysis and educational purposes only
- **Not Financial Advice**: All recommendations and insights are generated by algorithms and should not be considered as financial advice
- **Data Limitations**: Free data sources may have rate limits, delays, or occasional unavailability
- **Market Conditions**: Market conditions change constantly - regularly review and adjust parameters
- **Past Performance**: Past performance does not guarantee future results
- **Risk Warning**: Always test strategies thoroughly before using real money. Investing involves risk of loss.

## 🔍 Key Features in Detail


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
- **Interval Options**: 
  - **Intraday**: 1 Minute, 2 Minutes, 5 Minutes, 15 Minutes, 30 Minutes, 60 Minutes, 90 Minutes, Hourly
  - **Daily/Weekly**: Daily, Weekly, Monthly, Quarterly
- **Adaptive Data Point Requirements**: The system automatically adjusts minimum data point requirements based on the selected period and interval, ensuring stocks aren't filtered out unnecessarily
- **Use Cases**: 
  - **Intraday Trading**: 1-3 months with hourly/15-minute intervals (note: intraday data typically available up to 60 days)
  - **Short-term**: 1-3 months with daily intervals
  - **Medium-term**: 6 months-1 year with daily/weekly
  - **Long-term**: 2-10 years with weekly/monthly
  - **Trend analysis**: Longer periods with weekly/monthly intervals
- **Important Note**: Intraday intervals (1m-1h) are typically only available for periods up to 60 days. For longer periods, use Daily or Weekly intervals.

### Chart Visualization
- **Candlestick Charts**: Professional OHLC visualization showing open, high, low, close
- **Line Charts**: Simple closing price visualization
- **Technical Overlays**: Moving averages, RSI, MACD indicators
- **Interactive Features**: Hover tooltips, zoom, pan capabilities

## 🚀 Future Enhancements

### Planned Features
- **Backtesting Engine**: Historical strategy performance testing
- **Advanced Strategies**: Mean reversion, pairs trading, statistical arbitrage
- **Portfolio Optimization**: Modern portfolio theory and risk-return optimization
- **Real-time Alerts**: Email/SMS notifications for trading signals
- **Broker Integration**: API connections for live trading (Alpaca, Interactive Brokers, etc.)
- **News Sentiment Analysis**: NLP-based sentiment scoring from financial news
- **Predictive Models**: Machine learning price forecasting
- **Natural Language Queries**: Chat interface for stock queries
- **Multi-asset Support**: Extend to ETFs, options, cryptocurrencies
- **Social Features**: Share strategies and insights with community

### Technical Improvements
- **Database Integration**: Persistent storage for historical analysis
- **API Development**: RESTful API for programmatic access
- **Performance Optimization**: Parallel processing for faster analysis
- **Enhanced Caching**: Redis-based distributed caching
- **Monitoring & Logging**: Comprehensive logging and performance monitoring

## 📚 Learning Outcomes

This project demonstrates:

- **Full-Stack Development**: End-to-end application development from data processing to UI
- **Financial Engineering**: Implementation of quantitative trading strategies and technical analysis
- **Data Science**: Data fetching, processing, and visualization
- **AI/ML Concepts**: Rule-based AI systems and multi-factor scoring
- **Web Development**: Modern web UI with Streamlit and interactive visualizations
- **Software Architecture**: Modular design with separation of concerns
- **API Integration**: Working with external APIs (Yahoo Finance)
- **Performance Optimization**: Caching strategies and efficient data processing

## 🤝 Contributing

This is a portfolio project, but suggestions and feedback are welcome! If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is for **educational purposes only**. Use at your own risk.

**Disclaimer**: This software is provided "as is" without warranty of any kind. The authors and contributors are not responsible for any financial losses or damages resulting from the use of this software.

---

<div align="center">

**Built with ❤️ by [The Studio 701 LLC](https://github.com/kevintan701)**

[⬆ Back to Top](#-quantify-701---ai-powered-quantitative-investment-platform)

</div>

