"""
AI Insights Module for Quantify App.
Provides AI-powered analysis, insights, and recommendations.
Designed to be flexible for future expansion beyond stock selection.
"""

from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime


class AIInsights:
    """
    AI-powered insights generator for stock analysis.
    Provides intelligent analysis, recommendations, and explanations.
    """
    
    def __init__(self):
        """Initialize the AI insights generator."""
        pass
    
    def generate_stock_insight(self, stock: Dict) -> str:
        """
        Generate AI-powered insight for a single stock.
        
        Args:
            stock: Stock data dictionary with all metrics
        
        Returns:
            AI-generated insight text
        """
        symbol = stock['symbol']
        score = stock['score']
        rsi = stock.get('rsi')
        momentum = stock.get('momentum')
        volume_ratio = stock.get('volume_ratio', 0)
        sector = stock.get('sector', 'Unknown')
        current_price = stock['current_price']
        
        # Build insight based on multiple factors
        insights = []
        
        # Score-based insight
        if score >= 90:
            insights.append(f"**Exceptional Opportunity**: {symbol} shows outstanding quantitative metrics with a score of {score:.1f}/100. This stock demonstrates strong technical indicators across multiple dimensions.")
        elif score >= 80:
            insights.append(f"**Strong Candidate**: {symbol} presents a compelling investment opportunity with a score of {score:.1f}/100, indicating robust technical fundamentals.")
        elif score >= 70:
            insights.append(f"**Solid Choice**: {symbol} shows promising characteristics with a score of {score:.1f}/100, worth monitoring for entry opportunities.")
        else:
            insights.append(f"**Moderate Potential**: {symbol} has a score of {score:.1f}/100. While not exceptional, it may present value opportunities in specific market conditions.")
        
        # RSI analysis
        if rsi is not None:
            if rsi < 30:
                insights.append(f"The RSI of {rsi:.1f} indicates the stock is significantly oversold, potentially presenting a buying opportunity for contrarian investors.")
            elif rsi < 40:
                insights.append(f"With an RSI of {rsi:.1f}, the stock is approaching oversold territory, suggesting potential upward momentum ahead.")
            elif 40 <= rsi <= 60:
                insights.append(f"The RSI of {rsi:.1f} is in a neutral range, indicating balanced market sentiment without extreme overbought or oversold conditions.")
            elif rsi > 70:
                insights.append(f"An RSI of {rsi:.1f} suggests the stock may be overbought. Consider waiting for a pullback before entering.")
            else:
                insights.append(f"The RSI of {rsi:.1f} shows moderate bullish momentum.")
        
        # Momentum analysis
        if momentum is not None:
            momentum_pct = momentum * 100
            if momentum_pct > 10:
                insights.append(f"Strong positive momentum of {momentum_pct:.2f}% over the past 20 days indicates sustained buying pressure and potential continuation of the uptrend.")
            elif momentum_pct > 5:
                insights.append(f"Positive momentum of {momentum_pct:.2f}% suggests the stock is gaining traction, which could signal the beginning of a favorable trend.")
            elif momentum_pct > 0:
                insights.append(f"Modest positive momentum of {momentum_pct:.2f}% indicates slight upward pressure, though the trend may need confirmation.")
            else:
                insights.append(f"Negative momentum of {momentum_pct:.2f}% suggests caution. The stock may need to stabilize before considering entry.")
        
        # Volume analysis
        if volume_ratio:
            if volume_ratio >= 1.5:
                insights.append(f"Exceptional trading volume ({volume_ratio:.2f}x average) indicates strong institutional interest and confirms the current price movement.")
            elif volume_ratio >= 1.2:
                insights.append(f"Above-average volume ({volume_ratio:.2f}x) suggests increased market attention and validates recent price action.")
            elif volume_ratio < 0.8:
                insights.append(f"Below-average volume ({volume_ratio:.2f}x) may indicate lack of conviction. Monitor for volume confirmation before committing.")
        
        # Sector context
        insights.append(f"Operating in the {sector} sector, {symbol} should be evaluated within the context of sector-specific trends and macroeconomic factors affecting this industry.")
        
        # Price context
        if current_price < 50:
            insights.append(f"At ${current_price:.2f}, this stock offers accessibility for smaller portfolios while maintaining liquidity.")
        elif current_price > 200:
            insights.append(f"With a price of ${current_price:.2f}, this stock represents a premium investment that may appeal to institutional investors.")
        
        return " ".join(insights)
    
    def generate_portfolio_insight(self, stocks: List[Dict]) -> str:
        """
        Generate AI insight for the overall portfolio/selection.
        
        Args:
            stocks: List of stock dictionaries
        
        Returns:
            AI-generated portfolio insight
        """
        if not stocks:
            return "No stocks available for analysis."
        
        total_stocks = len(stocks)
        avg_score = sum(s['score'] for s in stocks) / total_stocks
        buy_signals = sum(1 for s in stocks if s.get('buy_signal', False))
        
        # Sector distribution
        sectors = {}
        for stock in stocks:
            sector = stock.get('sector', 'Unknown')
            sectors[sector] = sectors.get(sector, 0) + 1
        
        top_sector = max(sectors.items(), key=lambda x: x[1])[0] if sectors else "N/A"
        
        insights = []
        
        insights.append(f"**Portfolio Analysis**: The current selection includes {total_stocks} qualified stocks with an average score of {avg_score:.1f}/100.")
        
        if avg_score >= 80:
            insights.append("The overall quality is exceptional, indicating a strong market environment with numerous high-quality opportunities.")
        elif avg_score >= 70:
            insights.append("The selection shows solid quality, suggesting favorable market conditions for quantitative strategies.")
        else:
            insights.append("The current selection reflects moderate opportunities. Consider tightening filters or waiting for better market conditions.")
        
        if buy_signals > 0:
            buy_pct = (buy_signals / total_stocks) * 100
            insights.append(f"**Trading Signals**: {buy_signals} stocks ({buy_pct:.1f}%) show BUY signals, indicating active opportunities in the current market.")
        
        insights.append(f"**Sector Focus**: The {top_sector} sector dominates the selection with {sectors.get(top_sector, 0)} stocks, suggesting sector-specific strength or opportunities.")
        
        # Risk assessment
        high_volatility_count = sum(1 for s in stocks if s.get('data') is not None and 
                                   not s['data'].empty and 
                                   s['data'].iloc[-1].get('Volatility', 0) > 0.04)
        
        if high_volatility_count > total_stocks * 0.3:
            insights.append("**Risk Note**: A significant portion of selected stocks show elevated volatility. Consider position sizing and risk management strategies.")
        else:
            insights.append("**Risk Assessment**: The selection shows generally moderate volatility levels, suitable for most risk profiles.")
        
        return " ".join(insights)
    
    def generate_recommendation(self, stock: Dict) -> Dict:
        """
        Generate AI-powered recommendation for a stock.
        
        Args:
            stock: Stock data dictionary
        
        Returns:
            Dictionary with recommendation details
        """
        symbol = stock['symbol']
        score = stock['score']
        buy_signal = stock.get('buy_signal', False)
        
        recommendation = {
            'symbol': symbol,
            'action': 'BUY' if buy_signal else 'HOLD',
            'confidence': 'High' if score >= 80 else 'Medium' if score >= 60 else 'Low',
            'reasoning': [],
            'risk_level': 'Low',
            'time_horizon': 'Short-term'
        }
        
        # Determine risk level
        volatility = None
        if stock.get('data') is not None and not stock['data'].empty:
            volatility = stock['data'].iloc[-1].get('Volatility', None)
        
        if volatility:
            if volatility > 0.04:
                recommendation['risk_level'] = 'High'
            elif volatility > 0.025:
                recommendation['risk_level'] = 'Medium'
            else:
                recommendation['risk_level'] = 'Low'
        
        # Determine time horizon based on momentum and trends
        momentum = stock.get('momentum')
        if momentum and momentum > 0.05:
            recommendation['time_horizon'] = 'Short to Medium-term'
        elif momentum and momentum > 0:
            recommendation['time_horizon'] = 'Medium-term'
        else:
            recommendation['time_horizon'] = 'Long-term'
        
        # Build reasoning
        if buy_signal:
            recommendation['reasoning'].append("Strong BUY signal detected based on technical analysis")
        if score >= 80:
            recommendation['reasoning'].append("Exceptional quantitative score indicates high-quality opportunity")
        if stock.get('rsi') and 30 <= stock['rsi'] <= 50:
            recommendation['reasoning'].append("RSI suggests favorable entry point")
        if momentum and momentum > 0.03:
            recommendation['reasoning'].append("Strong positive momentum supports bullish outlook")
        
        recommendation['summary'] = f"AI Recommendation: {recommendation['action']} {symbol} with {recommendation['confidence'].lower()} confidence. "
        recommendation['summary'] += f"Risk level: {recommendation['risk_level']}. "
        recommendation['summary'] += f"Time horizon: {recommendation['time_horizon']}."
        
        return recommendation
    
    def explain_score(self, stock: Dict) -> str:
        """
        AI explanation of why a stock received its score.
        
        Args:
            stock: Stock data dictionary
        
        Returns:
            Explanation text
        """
        symbol = stock['symbol']
        score = stock['score']
        
        explanation = f"**Score Explanation for {symbol} ({score:.1f}/100)**:\n\n"
        
        # Analyze contributing factors
        factors = []
        
        data = stock.get('data')
        if data is not None and not data.empty:
            latest = data.iloc[-1]
            
            # Momentum contribution
            momentum = latest.get('Momentum')
            if momentum and 0.03 <= momentum <= 0.12:
                factors.append("Strong momentum (3-12%) contributes significantly to the score")
            elif momentum and momentum > 0:
                factors.append("Positive momentum provides moderate score contribution")
            
            # RSI contribution
            rsi = latest.get('RSI')
            if rsi and 45 <= rsi <= 65:
                factors.append("Optimal RSI range (45-65) indicates balanced market sentiment")
            elif rsi:
                factors.append(f"RSI of {rsi:.1f} affects the score based on overbought/oversold conditions")
            
            # Moving average trend
            sma_20 = latest.get('SMA_20')
            sma_50 = latest.get('SMA_50')
            current_price = stock['current_price']
            
            if pd.notna(sma_20) and pd.notna(sma_50):
                if current_price > sma_20 > sma_50:
                    factors.append("Strong uptrend (price > SMA20 > SMA50) significantly boosts the score")
                elif current_price > sma_20:
                    factors.append("Price above short-term moving average supports the score")
            
            # MACD
            macd = latest.get('MACD')
            macd_signal = latest.get('MACD_Signal')
            if pd.notna(macd) and pd.notna(macd_signal) and macd > macd_signal:
                factors.append("Bullish MACD crossover adds to the score")
            
            # Volume
            volume_ratio = latest.get('Volume_Ratio')
            if pd.notna(volume_ratio) and volume_ratio >= 1.0:
                factors.append("Above-average volume confirms price movements and enhances score")
        
        if factors:
            explanation += "Key contributing factors:\n"
            for i, factor in enumerate(factors, 1):
                explanation += f"{i}. {factor}\n"
        else:
            explanation += "Score is based on a composite of technical indicators, momentum, and market factors."
        
        return explanation
    
    def generate_market_sentiment(self, stocks: List[Dict]) -> str:
        """
        Generate overall market sentiment based on stock selection.
        
        Args:
            stocks: List of stock dictionaries
        
        Returns:
            Market sentiment analysis
        """
        if not stocks:
            return "Insufficient data for sentiment analysis."
        
        total = len(stocks)
        high_scores = sum(1 for s in stocks if s['score'] >= 80)
        buy_signals = sum(1 for s in stocks if s.get('buy_signal', False))
        avg_score = sum(s['score'] for s in stocks) / total
        
        sentiment = []
        
        sentiment.append("**Market Sentiment Analysis**:\n\n")
        
        # Overall sentiment
        if avg_score >= 80 and buy_signals > total * 0.5:
            sentiment.append("🟢 **Bullish**: Market conditions are highly favorable. Strong quantitative scores and numerous BUY signals suggest a robust market environment with multiple high-quality opportunities.")
        elif avg_score >= 70 and buy_signals > total * 0.3:
            sentiment.append("🟡 **Moderately Bullish**: Market shows positive characteristics with solid opportunities. While not exceptional, there are worthwhile investments available.")
        elif avg_score >= 60:
            sentiment.append("⚪ **Neutral**: Market conditions are mixed. Exercise caution and be selective in stock choices.")
        else:
            sentiment.append("🔴 **Cautious**: Market conditions are challenging. Consider waiting for better opportunities or tightening selection criteria.")
        
        sentiment.append(f"\n**Key Metrics**:\n")
        sentiment.append(f"- {high_scores}/{total} stocks ({high_scores/total*100:.1f}%) show exceptional scores (≥80)\n")
        sentiment.append(f"- {buy_signals}/{total} stocks ({buy_signals/total*100:.1f}%) have BUY signals\n")
        sentiment.append(f"- Average score: {avg_score:.1f}/100\n")
        
        return " ".join(sentiment)

