"""
Stock selection module using quantitative filters.
Applies various criteria to filter and rank stocks for trading.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from data_fetcher import DataFetcher
import config


class StockSelector:
    """
    Implements quantitative stock selection criteria.
    Filters stocks based on technical indicators, fundamentals, and momentum.
    """
    
    def __init__(self, data_fetcher: DataFetcher):
        """
        Initialize the stock selector.
        
        Args:
            data_fetcher: DataFetcher instance for getting stock data
        """
        self.data_fetcher = data_fetcher
        # Default filter parameters (can be overridden)
        self.filter_params = {
            'min_market_cap': config.MIN_MARKET_CAP,
            'min_volume': config.MIN_VOLUME,
            'min_price': config.MIN_PRICE,
            'max_price': config.MAX_PRICE,
            'min_rsi': config.MIN_RSI,
            'max_rsi': config.MAX_RSI,
            'min_volume_ratio': config.MIN_VOLUME_RATIO,
            'min_data_points': config.MIN_DATA_POINTS,
            'max_volatility': config.MAX_VOLATILITY
        }
    
    def set_filter_params(self, **kwargs):
        """
        Update filter parameters.
        
        Args:
            **kwargs: Filter parameters to update
        """
        self.filter_params.update(kwargs)
    
    def filter_stocks(
        self, 
        symbols: List[str], 
        custom_filters: Optional[Dict] = None,
        period: str = "1y",
        interval: str = "1d"
    ) -> List[Dict]:
        """
        Filter stocks based on quantitative criteria.
        
        Args:
            symbols: List of stock symbols to evaluate
            custom_filters: Optional dictionary of custom filter parameters
            period: Time period for data ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
            interval: Data interval ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo")
        
        Returns:
            List of dictionaries with stock data and scores
        """
        # Use custom filters if provided, otherwise use instance filters
        filters = custom_filters if custom_filters else self.filter_params
        
        qualified_stocks = []
        
        # Only print if not in Streamlit environment
        import sys
        if 'streamlit' not in sys.modules:
            print(f"Evaluating {len(symbols)} stocks...")
        
        for symbol in symbols:
            try:
                # Get stock data with specified period and interval
                data = self.data_fetcher.get_stock_data(symbol, period=period, interval=interval)
                if data is None or data.empty:
                    continue
                
                # Calculate technical indicators
                data = self.data_fetcher.calculate_technical_indicators(data)
                
                # Get fundamental info
                info = self.data_fetcher.get_stock_info(symbol)
                if info is None:
                    continue
                
                # Apply filters
                if not self._passes_filters(data, info, filters):
                    continue
                
                # Calculate score
                score = self._calculate_score(data, info)
                
                # Store qualified stock
                stock_data = {
                    'symbol': symbol,
                    'score': score,
                    'current_price': float(data['Close'].iloc[-1]),
                    'rsi': float(data['RSI'].iloc[-1]) if not pd.isna(data['RSI'].iloc[-1]) else None,
                    'momentum': float(data['Momentum'].iloc[-1]) if not pd.isna(data['Momentum'].iloc[-1]) else None,
                    'volume_ratio': float(data['Volume_Ratio'].iloc[-1]) if not pd.isna(data['Volume_Ratio'].iloc[-1]) else None,
                    'market_cap': info.get('market_cap', 0),
                    'sector': info.get('sector', 'Unknown'),
                    'data': data  # Store full data for strategy use
                }
                
                qualified_stocks.append(stock_data)
                
            except Exception as e:
                # Only print if not in Streamlit environment
                import sys
                if 'streamlit' not in sys.modules:
                    print(f"Error processing {symbol}: {str(e)}")
                continue
        
        # Sort by score (highest first)
        qualified_stocks.sort(key=lambda x: x['score'], reverse=True)
        
        # Only print if not in Streamlit environment
        import sys
        if 'streamlit' not in sys.modules:
            print(f"Found {len(qualified_stocks)} qualified stocks")
        
        return qualified_stocks
    
    def _passes_filters(self, data: pd.DataFrame, info: Dict, filters: Optional[Dict] = None) -> bool:
        """
        Check if a stock passes all quantitative filters.
        
        Args:
            data: DataFrame with price and technical indicator data
            info: Dictionary with fundamental stock information
            filters: Optional dictionary of filter parameters (uses instance filters if None)
        
        Returns:
            True if stock passes all filters, False otherwise
        """
        if data.empty:
            return False
        
        # Use provided filters or instance filters
        f = filters if filters else self.filter_params
        
        latest = data.iloc[-1]
        
        # Price filter
        current_price = float(latest['Close'])
        if current_price < f['min_price'] or current_price > f['max_price']:
            return False
        
        # Market cap filter
        market_cap = info.get('market_cap', 0)
        if market_cap < f['min_market_cap']:
            return False
        
        # Volume filter
        volume = float(latest['Volume'])
        if volume < f['min_volume']:
            return False
        
        # RSI filter (avoid extreme overbought/oversold)
        rsi = latest['RSI']
        if not pd.isna(rsi):
            if rsi < f['min_rsi'] or rsi > f['max_rsi']:
                return False
        
        # Ensure we have enough data points
        if len(data) < f['min_data_points']:
            return False
        
        # Check for sufficient liquidity (volume ratio)
        volume_ratio = latest['Volume_Ratio']
        if not pd.isna(volume_ratio) and volume_ratio < f['min_volume_ratio']:
            return False
        
        # Volatility filter (avoid extremely volatile stocks)
        volatility = latest.get('Volatility', None)
        if not pd.isna(volatility) and volatility > f['max_volatility']:
            return False
        
        # Trend strength filter (prefer stocks with clear trends)
        sma_20 = latest.get('SMA_20', None)
        if pd.notna(sma_20):
            price_vs_sma20 = (current_price - sma_20) / sma_20
            # Allow stocks that are at least not significantly below SMA20
            if price_vs_sma20 < -0.10:  # More than 10% below SMA20
                return False
        
        return True
    
    def _calculate_score(self, data: pd.DataFrame, info: Dict) -> float:
        """
        Calculate a composite score for stock ranking using multiple factors.
        Higher scores indicate better investment opportunities.
        
        Args:
            data: DataFrame with price and technical indicator data
            info: Dictionary with fundamental stock information
        
        Returns:
            Composite score (0-100)
        """
        if data.empty:
            return 0.0
        
        latest = data.iloc[-1]
        score = 0.0
        current_price = float(latest['Close'])
        
        # 1. Momentum score (0-25 points)
        # Strong positive momentum is highly valued
        momentum = latest['Momentum']
        if not pd.isna(momentum):
            if 0.03 <= momentum <= 0.12:  # 3-12% momentum (sweet spot)
                score += 25
            elif 0.015 <= momentum < 0.03 or 0.12 < momentum <= 0.20:
                score += 18
            elif 0.005 <= momentum < 0.015 or 0.20 < momentum <= 0.30:
                score += 12
            elif momentum > 0:
                score += 6
        
        # 2. RSI score (0-20 points)
        # Prefer RSI in optimal range (40-65 for bullish momentum)
        rsi = latest['RSI']
        if not pd.isna(rsi):
            if 45 <= rsi <= 65:  # Optimal bullish range
                score += 20
            elif 35 <= rsi < 45 or 65 < rsi <= 70:
                score += 15
            elif 30 <= rsi < 35 or 70 < rsi <= 75:
                score += 10
            elif 25 <= rsi < 30 or 75 < rsi <= 80:
                score += 5
        
        # 3. Moving average trend strength (0-20 points)
        # Strong uptrend is highly valued
        sma_20 = latest['SMA_20']
        sma_50 = latest['SMA_50']
        sma_200 = latest.get('SMA_200', None)
        
        if not pd.isna(sma_20) and not pd.isna(sma_50):
            # Perfect uptrend: price > SMA20 > SMA50
            if current_price > sma_20 > sma_50:
                # Calculate how strong the trend is
                price_above_sma20 = (current_price - sma_20) / sma_20
                sma20_above_sma50 = (sma_20 - sma_50) / sma_50
                
                if price_above_sma20 >= 0.05 and sma20_above_sma50 >= 0.02:  # Strong trend
                    score += 20
                elif price_above_sma20 >= 0.02 and sma20_above_sma50 >= 0.01:  # Good trend
                    score += 15
                else:  # Weak but positive trend
                    score += 10
            elif current_price > sma_20:  # Price above short-term MA
                score += 8
            elif current_price > sma_50:  # Price above long-term MA
                score += 4
        
        # Bonus for SMA200 alignment (if available)
        if pd.notna(sma_200) and pd.notna(sma_50):
            if sma_50 > sma_200:
                score += 3  # Long-term uptrend confirmed
        
        # 4. MACD signal strength (0-15 points)
        # Strong bullish MACD is valuable
        macd = latest['MACD']
        macd_signal = latest['MACD_Signal']
        macd_hist = latest.get('MACD_Histogram', None)
        
        if not pd.isna(macd) and not pd.isna(macd_signal):
            if macd > macd_signal:
                # Calculate MACD strength
                macd_strength = (macd - macd_signal) / abs(macd_signal) if macd_signal != 0 else 0
                
                if macd > 0 and macd_strength > 0.2:  # Strong bullish
                    score += 15
                elif macd > 0:  # Moderate bullish
                    score += 12
                else:  # Weak bullish (above zero line)
                    score += 8
            elif macd > 0:  # MACD positive but below signal
                score += 5
        
        # Bonus for increasing MACD histogram
        if pd.notna(macd_hist) and macd_hist > 0:
            score += 2
        
        # 5. Volume confirmation (0-12 points)
        # Strong volume confirms price movements
        volume_ratio = latest['Volume_Ratio']
        if not pd.isna(volume_ratio):
            if volume_ratio >= 1.5:  # Very high volume
                score += 12
            elif volume_ratio >= 1.2:  # High volume
                score += 10
            elif volume_ratio >= 1.0:  # Above average
                score += 8
            elif volume_ratio >= 0.8:  # Near average
                score += 5
        
        # 6. Volatility score (0-8 points)
        # Moderate volatility is preferred
        volatility = latest['Volatility']
        if not pd.isna(volatility):
            if 0.015 <= volatility <= 0.025:  # 1.5-2.5% daily volatility (ideal)
                score += 8
            elif 0.01 <= volatility < 0.015 or 0.025 < volatility <= 0.035:
                score += 6
            elif 0.005 <= volatility < 0.01 or 0.035 < volatility <= 0.045:
                score += 4
        
        # 7. Price momentum consistency (0-8 points)
        # Check if momentum is consistent over multiple periods
        if len(data) >= 60:
            recent_momentum_5d = data['Close'].iloc[-1] / data['Close'].iloc[-5] - 1
            recent_momentum_10d = data['Close'].iloc[-1] / data['Close'].iloc[-10] - 1
            
            if recent_momentum_5d > 0 and recent_momentum_10d > 0:
                if abs(recent_momentum_5d - recent_momentum_10d) < 0.02:  # Consistent
                    score += 8
                else:
                    score += 5
        
        # 8. Bollinger Bands position (0-7 points)
        # Price near lower band can indicate good entry, but not too oversold
        bb_upper = latest.get('BB_Upper', None)
        bb_lower = latest.get('BB_Lower', None)
        bb_middle = latest.get('BB_Middle', None)
        
        if pd.notna(bb_upper) and pd.notna(bb_lower) and pd.notna(bb_middle):
            bb_position = (current_price - bb_lower) / (bb_upper - bb_lower)
            
            if 0.3 <= bb_position <= 0.7:  # Middle to upper-middle (good)
                score += 7
            elif 0.2 <= bb_position < 0.3 or 0.7 < bb_position <= 0.8:
                score += 5
            elif 0.1 <= bb_position < 0.2 or 0.8 < bb_position <= 0.9:
                score += 3
        
        return min(score, 100.0)  # Cap at 100

