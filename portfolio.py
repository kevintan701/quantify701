"""
Portfolio management module.
Tracks positions, cash, and overall portfolio performance.
"""

import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import config


class Portfolio:
    """
    Manages portfolio state including cash, positions, and performance tracking.
    """
    
    def __init__(self, initial_capital: float = None):
        """
        Initialize portfolio.
        
        Args:
            initial_capital: Starting cash amount (defaults to config value)
        """
        self.initial_capital = initial_capital or config.INITIAL_CAPITAL
        self.cash = self.initial_capital
        self.positions: Dict[str, Dict] = {}  # symbol -> position data
        self.trade_history: List[Dict] = []
        self.last_rebalance_date: Optional[datetime] = None
    
    def add_position(
        self, 
        symbol: str, 
        shares: int, 
        price: float,
        stock_data: Dict = None
    ) -> bool:
        """
        Add a new position to the portfolio.
        
        Args:
            symbol: Stock ticker symbol
            shares: Number of shares to buy
            price: Price per share
            stock_data: Optional stock data dictionary
        
        Returns:
            True if position added successfully, False otherwise
        """
        cost = shares * price
        
        # Check if we have enough cash
        if cost > self.cash:
            print(f"Insufficient cash to buy {shares} shares of {symbol} at ${price:.2f}")
            return False
        
        # Check if we already have a position
        if symbol in self.positions:
            print(f"Already have a position in {symbol}")
            return False
        
        # Check maximum positions limit
        if len(self.positions) >= config.MAX_POSITIONS:
            print(f"Maximum positions limit ({config.MAX_POSITIONS}) reached")
            return False
        
        # Add position
        self.positions[symbol] = {
            'symbol': symbol,
            'shares': shares,
            'entry_price': price,
            'entry_date': datetime.now(),
            'stock_data': stock_data
        }
        
        # Update cash
        self.cash -= cost
        
        # Record trade
        self.trade_history.append({
            'date': datetime.now(),
            'symbol': symbol,
            'action': 'BUY',
            'shares': shares,
            'price': price,
            'value': cost
        })
        
        print(f"Bought {shares} shares of {symbol} at ${price:.2f} (Total: ${cost:.2f})")
        return True
    
    def remove_position(self, symbol: str, price: float) -> bool:
        """
        Remove a position from the portfolio (sell).
        
        Args:
            symbol: Stock ticker symbol
            price: Current market price per share
        
        Returns:
            True if position removed successfully, False otherwise
        """
        if symbol not in self.positions:
            print(f"No position found for {symbol}")
            return False
        
        position = self.positions[symbol]
        shares = position['shares']
        proceeds = shares * price
        
        # Calculate profit/loss
        entry_price = position['entry_price']
        pnl = proceeds - (shares * entry_price)
        pnl_pct = (price - entry_price) / entry_price * 100
        
        # Update cash
        self.cash += proceeds
        
        # Record trade
        self.trade_history.append({
            'date': datetime.now(),
            'symbol': symbol,
            'action': 'SELL',
            'shares': shares,
            'price': price,
            'value': proceeds,
            'pnl': pnl,
            'pnl_pct': pnl_pct
        })
        
        # Remove position
        del self.positions[symbol]
        
        print(f"Sold {shares} shares of {symbol} at ${price:.2f} (P&L: ${pnl:.2f}, {pnl_pct:.1f}%)")
        return True
    
    def update_position_data(self, symbol: str, stock_data: Dict):
        """
        Update stock data for an existing position.
        
        Args:
            symbol: Stock ticker symbol
            stock_data: Updated stock data dictionary
        """
        if symbol in self.positions:
            self.positions[symbol]['stock_data'] = stock_data
    
    def get_position_value(self, symbol: str, current_price: float) -> float:
        """
        Get current value of a position.
        
        Args:
            symbol: Stock ticker symbol
            current_price: Current market price
        
        Returns:
            Current position value
        """
        if symbol not in self.positions:
            return 0.0
        
        return self.positions[symbol]['shares'] * current_price
    
    def get_total_value(self, current_prices: Dict[str, float]) -> float:
        """
        Get total portfolio value (cash + positions).
        
        Args:
            current_prices: Dictionary mapping symbols to current prices
        
        Returns:
            Total portfolio value
        """
        positions_value = sum(
            self.get_position_value(symbol, price)
            for symbol, price in current_prices.items()
            if symbol in self.positions
        )
        
        return self.cash + positions_value
    
    def get_portfolio_summary(self, current_prices: Dict[str, float]) -> Dict:
        """
        Get summary of portfolio performance.
        
        Args:
            current_prices: Dictionary mapping symbols to current prices
        
        Returns:
            Dictionary with portfolio summary statistics
        """
        total_value = self.get_total_value(current_prices)
        total_return = total_value - self.initial_capital
        total_return_pct = (total_return / self.initial_capital) * 100
        
        # Calculate position values
        positions_summary = []
        for symbol, position in self.positions.items():
            current_price = current_prices.get(symbol, position['entry_price'])
            position_value = self.get_position_value(symbol, current_price)
            entry_value = position['shares'] * position['entry_price']
            pnl = position_value - entry_value
            pnl_pct = (current_price - position['entry_price']) / position['entry_price'] * 100
            
            positions_summary.append({
                'symbol': symbol,
                'shares': position['shares'],
                'entry_price': position['entry_price'],
                'current_price': current_price,
                'value': position_value,
                'pnl': pnl,
                'pnl_pct': pnl_pct
            })
        
        return {
            'cash': self.cash,
            'positions_value': total_value - self.cash,
            'total_value': total_value,
            'initial_capital': self.initial_capital,
            'total_return': total_return,
            'total_return_pct': total_return_pct,
            'num_positions': len(self.positions),
            'positions': positions_summary
        }
    
    def get_trade_history(self) -> pd.DataFrame:
        """
        Get trade history as a DataFrame.
        
        Returns:
            DataFrame with all trades
        """
        if not self.trade_history:
            return pd.DataFrame()
        
        return pd.DataFrame(self.trade_history)

