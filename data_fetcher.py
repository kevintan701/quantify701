"""
Data fetching module for stock market data.
Uses yfinance (Yahoo Finance) for free data access.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import config
from utils import retry_on_failure, rate_limit, setup_logging

# Set up logging
logger = setup_logging()


class DataFetcher:
    """
    Handles fetching and processing stock market data from free sources.
    Provides methods to get price data, technical indicators, and fundamentals.
    """
    
    def __init__(self):
        """Initialize the data fetcher."""
        self.cache = {}  # Simple cache to avoid redundant API calls
        self.cache_timeout = timedelta(hours=config.UPDATE_INTERVAL_HOURS)
    
    @retry_on_failure(max_attempts=3, delay=1.0, backoff=2.0)
    @rate_limit(max_calls_per_minute=60)
    def get_stock_data(
        self, 
        symbol: str, 
        period: str = "1y",
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data for a given symbol with retry logic and rate limiting.
        
        Args:
            symbol: Stock ticker symbol (e.g., "AAPL")
            period: Time period ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
            interval: Data interval ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo")
        
        Returns:
            DataFrame with OHLCV data, or None if fetch fails
        """
        try:
            # Check cache first
            cache_key = f"{symbol}_{period}_{interval}"
            if cache_key in self.cache:
                cached_data, cached_time = self.cache[cache_key]
                if datetime.now() - cached_time < self.cache_timeout:
                    logger.debug(f"Cache hit for {symbol}")
                    return cached_data.copy()
            
            # Fetch data from yfinance
            logger.debug(f"Fetching data for {symbol} ({period}, {interval})")
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                logger.warning(f"No data returned for {symbol}")
                return None
            
            # Store in cache
            self.cache[cache_key] = (data.copy(), datetime.now())
            logger.debug(f"Successfully fetched and cached data for {symbol}")
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}", exc_info=True)
            return None
    
    def get_multiple_stocks(
        self, 
        symbols: List[str], 
        period: str = "1y"
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple stocks efficiently.
        
        Args:
            symbols: List of stock ticker symbols
            period: Time period for historical data
        
        Returns:
            Dictionary mapping symbols to their DataFrames
        """
        results = {}
        
        for symbol in symbols:
            data = self.get_stock_data(symbol, period=period)
            if data is not None:
                results[symbol] = data
        
        return results
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate common technical indicators for trading signals.
        
        Args:
            data: DataFrame with OHLCV data
        
        Returns:
            DataFrame with added technical indicator columns
        """
        df = data.copy()
        
        # Simple Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        # Exponential Moving Averages
        df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
        
        # MACD (Moving Average Convergence Divergence)
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        # RSI (Relative Strength Index)
        df['RSI'] = self._calculate_rsi(df['Close'], period=14)
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # Volume indicators
        df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_SMA']
        
        # Price momentum (rate of change)
        df['Momentum'] = df['Close'].pct_change(periods=config.MIN_MOMENTUM_DAYS)
        
        # Volatility (standard deviation of returns)
        df['Volatility'] = df['Close'].pct_change().rolling(window=20).std()
        
        return df
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI).
        
        Args:
            prices: Series of closing prices
            period: RSI period (default 14)
        
        Returns:
            Series with RSI values
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @retry_on_failure(max_attempts=3, delay=1.0, backoff=2.0)
    @rate_limit(max_calls_per_minute=60)
    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """
        Get fundamental information about a stock with retry logic and rate limiting.
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Dictionary with stock info (market cap, sector, etc.) or None
        """
        try:
            logger.debug(f"Fetching info for {symbol}")
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract relevant information
            stock_info = {
                'symbol': symbol,
                'market_cap': info.get('marketCap', 0),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'current_price': info.get('currentPrice', 0),
                'volume': info.get('volume', 0),
                'avg_volume': info.get('averageVolume', 0),
                'pe_ratio': info.get('trailingPE', None),
                'dividend_yield': info.get('dividendYield', 0),
            }
            
            logger.debug(f"Successfully fetched info for {symbol}")
            return stock_info
            
        except Exception as e:
            logger.error(f"Error fetching info for {symbol}: {str(e)}", exc_info=True)
            return None
    
    def get_latest_price(self, symbol: str) -> Optional[float]:
        """
        Get the latest closing price for a symbol.
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Latest closing price or None
        """
        data = self.get_stock_data(symbol, period="5d")
        if data is not None and not data.empty:
            return float(data['Close'].iloc[-1])
        return None

