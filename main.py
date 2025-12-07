"""
Quantitative Stock Selection System.
Focuses on identifying and ranking the best stocks based on quantitative criteria.
"""

from data_fetcher import DataFetcher
from stock_selector import StockSelector
from trading_strategy import TradingStrategy
import config
from datetime import datetime
from typing import Dict
import pandas as pd


class StockSelectionSystem:
    """
    Main stock selection system that identifies and ranks stocks.
    """
    
    def __init__(self):
        """Initialize the stock selection system."""
        self.data_fetcher = DataFetcher()
        self.stock_selector = StockSelector(self.data_fetcher)
        self.strategy = TradingStrategy()
    
    def run_analysis(self, show_all: bool = False, top_n: int = 20):
        """
        Focus on stock selection and analysis.
        Displays detailed information about qualified stocks.
        
        Args:
            show_all: If True, show all qualified stocks. If False, show top 20.
        """
        print("=" * 80)
        print("QUANTITATIVE STOCK SELECTION ANALYSIS")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Step 1: Filter and rank stocks
        print("\n[Step 1] Filtering and ranking stocks...")
        qualified_stocks = self.stock_selector.filter_stocks(config.STOCK_UNIVERSE)
        
        if not qualified_stocks:
            print("No qualified stocks found. Exiting.")
            return
        
        # Display detailed analysis
        num_to_show = len(qualified_stocks) if show_all else min(top_n, len(qualified_stocks))
        print(f"\n{'='*80}")
        print(f"TOP {num_to_show} STOCK SELECTIONS (Ranked by Score)")
        print(f"{'='*80}")
        
        for i, stock in enumerate(qualified_stocks[:num_to_show], 1):
            self._display_stock_details(stock, i)
        
        # Step 2: Generate buy signals for top candidates
        print(f"\n{'='*80}")
        print("TRADING SIGNAL ANALYSIS")
        print(f"{'='*80}")
        
        buy_candidates = []
        hold_candidates = []
        
        for stock in qualified_stocks[:num_to_show]:
            should_buy, reason = self.strategy.generate_buy_signal(stock)
            if should_buy:
                buy_candidates.append((stock, reason))
                print(f"✓ {stock['symbol']:6s} | BUY SIGNAL | Score: {stock['score']:5.1f}")
                print(f"  Reason: {reason}")
            else:
                hold_candidates.append((stock, reason))
        
        # Summary statistics
        print(f"\n{'='*80}")
        print("SELECTION SUMMARY")
        print(f"{'='*80}")
        print(f"Total stocks analyzed: {len(config.STOCK_UNIVERSE)}")
        print(f"Qualified stocks: {len(qualified_stocks)}")
        print(f"Stocks with BUY signals: {len(buy_candidates)}")
        print(f"Stocks to monitor: {len(hold_candidates)}")
        print(f"Qualification rate: {len(qualified_stocks)/len(config.STOCK_UNIVERSE)*100:.1f}%")
        
        if buy_candidates:
            print(f"\n{'='*80}")
            print("TOP BUY RECOMMENDATIONS")
            print(f"{'='*80}")
            for i, (stock, reason) in enumerate(buy_candidates[:10], 1):
                rsi_str = f"{stock['rsi']:5.1f}" if stock['rsi'] is not None else "  N/A"
                print(f"{i:2d}. {stock['symbol']:6s} | Score: {stock['score']:5.1f} | "
                      f"Price: ${stock['current_price']:7.2f} | "
                      f"RSI: {rsi_str:>5}")
                print(f"    {reason}")
        
        print(f"\n{'='*80}")
    
    def _display_stock_details(self, stock: Dict, rank: int):
        """
        Display detailed information about a stock.
        
        Args:
            stock: Stock data dictionary
            rank: Ranking number
        """
        data = stock.get('data')
        if data is None or data.empty:
            return
        
        latest = data.iloc[-1]
        
        # Format values
        rsi_str = f"{stock['rsi']:5.1f}" if stock['rsi'] is not None else "  N/A"
        momentum_val = stock['momentum'] * 100 if stock['momentum'] is not None else 0.0
        volume_ratio = stock.get('volume_ratio', 0)
        volume_ratio_str = f"{volume_ratio:.2f}x" if volume_ratio else "N/A"
        
        # Moving averages
        sma_20 = latest.get('SMA_20', None)
        sma_50 = latest.get('SMA_50', None)
        sma_20_str = f"${sma_20:.2f}" if pd.notna(sma_20) else "N/A"
        sma_50_str = f"${sma_50:.2f}" if pd.notna(sma_50) else "N/A"
        
        # MACD
        macd = latest.get('MACD', None)
        macd_signal = latest.get('MACD_Signal', None)
        macd_str = f"{macd:.2f}" if pd.notna(macd) else "N/A"
        macd_signal_str = f"{macd_signal:.2f}" if pd.notna(macd_signal) else "N/A"
        macd_bullish = "✓" if (pd.notna(macd) and pd.notna(macd_signal) and macd > macd_signal) else "✗"
        
        # Price vs moving averages
        current_price = stock['current_price']
        price_vs_sma20 = ((current_price - sma_20) / sma_20 * 100) if pd.notna(sma_20) else None
        price_vs_sma20_str = f"{price_vs_sma20:+.1f}%" if price_vs_sma20 is not None else "N/A"
        
        # Volatility
        volatility = latest.get('Volatility', None)
        volatility_str = f"{volatility*100:.2f}%" if pd.notna(volatility) else "N/A"
        
        print(f"\n#{rank:2d}. {stock['symbol']:6s} | Score: {stock['score']:5.1f}/100")
        print(f"     Price: ${stock['current_price']:7.2f} | Market Cap: ${stock['market_cap']/1e9:.1f}B | Sector: {stock['sector']}")
        print(f"     RSI: {rsi_str:>5} | Momentum ({config.MIN_MOMENTUM_DAYS}d): {momentum_val:6.2f}% | Volatility: {volatility_str:>6}")
        print(f"     SMA 20: {sma_20_str:>8} | SMA 50: {sma_50_str:>8} | Price vs SMA20: {price_vs_sma20_str:>6}")
        print(f"     MACD: {macd_str:>6} | Signal: {macd_signal_str:>6} | Bullish: {macd_bullish} | Volume Ratio: {volume_ratio_str:>5}")
    


def main():
    """Main entry point."""
    # Create and run the stock selection system
    system = StockSelectionSystem()
    
    # Run stock selection analysis
    # Set show_all=True to see all qualified stocks
    # Set top_n to change number of stocks displayed
    system.run_analysis(show_all=False, top_n=20)


if __name__ == "__main__":
    main()

