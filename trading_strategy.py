"""
Trading strategy module.
Implements buy/sell signals based on technical analysis and risk management.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import config


class TradingStrategy:
    """
    Implements trading signals and decision logic.
    Determines when to buy, sell, or hold positions.
    """
    
    def __init__(self):
        """Initialize the trading strategy."""
        pass
    
    def generate_buy_signal(self, stock_data: Dict) -> Tuple[bool, str]:
        """
        Generate buy signal for a stock.
        
        Args:
            stock_data: Dictionary with stock data including technical indicators
        
        Returns:
            Tuple of (should_buy: bool, reason: str)
        """
        data = stock_data.get('data')
        if data is None or data.empty:
            return False, "No data available"
        
        latest = data.iloc[-1]
        reasons = []
        
        # Check multiple conditions for buy signal
        buy_score = 0
        
        # RSI condition (oversold or neutral)
        rsi = latest['RSI']
        if not pd.isna(rsi):
            if 30 <= rsi <= 50:  # Oversold to neutral
                buy_score += 1
                reasons.append(f"RSI at {rsi:.1f} (oversold/neutral)")
        
        # Moving average condition
        current_price = float(latest['Close'])
        sma_20 = latest['SMA_20']
        sma_50 = latest['SMA_50']
        
        if not pd.isna(sma_20) and not pd.isna(sma_50):
            if current_price > sma_20 > sma_50:
                buy_score += 1
                reasons.append("Price above moving averages (uptrend)")
            elif current_price > sma_20:
                buy_score += 1
                reasons.append("Price above 20-day MA")
        
        # MACD condition
        macd = latest['MACD']
        macd_signal = latest['MACD_Signal']
        if not pd.isna(macd) and not pd.isna(macd_signal):
            if macd > macd_signal:
                buy_score += 1
                reasons.append("MACD bullish crossover")
        
        # Momentum condition
        momentum = latest['Momentum']
        if not pd.isna(momentum) and momentum > 0:
            buy_score += 1
            reasons.append(f"Positive momentum ({momentum*100:.1f}%)")
        
        # Volume condition
        volume_ratio = latest['Volume_Ratio']
        if not pd.isna(volume_ratio) and volume_ratio >= 1.0:
            buy_score += 1
            reasons.append("Above-average volume")
        
        # Need at least 3 positive signals
        should_buy = buy_score >= 3
        reason = "; ".join(reasons) if reasons else "Insufficient buy signals"
        
        return should_buy, reason
    
    def generate_sell_signal(
        self, 
        position: Dict, 
        current_price: float
    ) -> Tuple[bool, str]:
        """
        Generate sell signal for an existing position.
        
        Args:
            position: Dictionary with position data (entry_price, entry_date, etc.)
            current_price: Current market price of the stock
        
        Returns:
            Tuple of (should_sell: bool, reason: str)
        """
        entry_price = position.get('entry_price', 0)
        entry_date = position.get('entry_date')
        
        if entry_price == 0:
            return False, "Invalid position data"
        
        # Calculate return
        return_pct = (current_price - entry_price) / entry_price
        
        reasons = []
        should_sell = False
        
        # Stop loss check
        if return_pct <= -config.STOP_LOSS_PCT:
            should_sell = True
            reasons.append(f"Stop loss triggered ({return_pct*100:.1f}%)")
        
        # Take profit check
        elif return_pct >= config.TAKE_PROFIT_PCT:
            should_sell = True
            reasons.append(f"Take profit target reached ({return_pct*100:.1f}%)")
        
        # Minimum holding period check
        if entry_date:
            holding_days = (datetime.now() - entry_date).days
            if holding_days < config.MIN_HOLDING_PERIOD_DAYS:
                # Don't sell if we haven't held long enough (unless stop loss)
                if return_pct > -config.STOP_LOSS_PCT:
                    return False, f"Minimum holding period not met ({holding_days} days)"
        
        # Check for reversal signals (if we have stock data)
        stock_data = position.get('stock_data')
        if stock_data is not None:
            data = stock_data.get('data')
            if data is not None and not data.empty:
                latest = data.iloc[-1]
                
                # RSI overbought
                rsi = latest['RSI']
                if not pd.isna(rsi) and rsi > 70:
                    should_sell = True
                    reasons.append(f"RSI overbought ({rsi:.1f})")
                
                # Price below moving averages (downtrend)
                current_price_check = float(latest['Close'])
                sma_20 = latest['SMA_20']
                if not pd.isna(sma_20) and current_price_check < sma_20:
                    should_sell = True
                    reasons.append("Price below 20-day MA (downtrend)")
        
        reason = "; ".join(reasons) if reasons else "No sell signal"
        return should_sell, reason
    
    def calculate_position_size(
        self, 
        stock_score: float, 
        portfolio_value: float,
        current_price: float
    ) -> float:
        """
        Calculate optimal position size based on stock score and risk.
        
        Args:
            stock_score: Stock selection score (0-100)
            portfolio_value: Total portfolio value
            current_price: Current stock price
        
        Returns:
            Number of shares to buy
        """
        # Base position size on score (higher score = larger position)
        # Normalize score to position size percentage
        score_pct = stock_score / 100.0
        
        # Calculate position size as percentage of portfolio
        # Scale between min and max position sizes
        position_pct = (
            config.MIN_POSITION_SIZE + 
            (config.MAX_POSITION_SIZE - config.MIN_POSITION_SIZE) * score_pct
        )
        
        # Calculate dollar amount
        position_value = portfolio_value * position_pct
        
        # Calculate number of shares (round down)
        num_shares = int(position_value / current_price)
        
        return max(num_shares, 0)  # Ensure non-negative
    
    def should_rebalance(self, last_rebalance_date: Optional[datetime]) -> bool:
        """
        Check if portfolio should be rebalanced.
        
        Args:
            last_rebalance_date: Date of last rebalancing
        
        Returns:
            True if rebalancing is needed
        """
        if last_rebalance_date is None:
            return True
        
        days_since = (datetime.now() - last_rebalance_date).days
        return days_since >= config.REBALANCE_FREQUENCY_DAYS

