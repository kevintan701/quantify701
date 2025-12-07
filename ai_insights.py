"""
AI Insights Module for Quantify App.
Provides AI-powered analysis, insights, and recommendations.
Designed to be flexible for future expansion beyond stock selection.
"""

from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime


class AIInsights:
    """
    AI-powered insights generator for stock analysis.
    Provides intelligent analysis, recommendations, and explanations.
    """
    
    def __init__(self):
        """Initialize the AI insights generator."""
        pass
    
    def calculate_suggested_buy_price(
        self, 
        stock: Dict, 
        strategy: str = "Default",
        period: str = "1y"
    ) -> Dict:
        """
        Calculate suggested buy price or price range based on technical analysis and strategy.
        
        Args:
            stock: Stock data dictionary
            strategy: Selected strategy (Default, Conservative, Aggressive, etc.)
            period: Time period for analysis
            
        Returns:
            Dictionary with suggested buy price, price range, and reasoning
        """
        current_price = stock['current_price']
        data = stock.get('data')
        
        if data is None or data.empty:
            return {
                'suggested_price': current_price,
                'price_range_low': current_price * 0.95,
                'price_range_high': current_price * 1.05,
                'reasoning': 'Insufficient data for price calculation'
            }
        
        latest = data.iloc[-1]
        
        # Calculate support levels
        support_levels = []
        
        # 1. Moving averages as support
        sma_20 = latest.get('SMA_20')
        sma_50 = latest.get('SMA_50')
        if pd.notna(sma_20):
            support_levels.append(('SMA 20', sma_20))
        if pd.notna(sma_50):
            support_levels.append(('SMA 50', sma_50))
        
        # 2. Bollinger Lower Band as support
        bb_lower = latest.get('BB_Lower')
        if pd.notna(bb_lower):
            support_levels.append(('Bollinger Lower', bb_lower))
        
        # 3. Recent low (last 20 days)
        recent_low = data['Low'].tail(20).min()
        if pd.notna(recent_low):
            support_levels.append(('Recent Low', recent_low))
        
        # 4. RSI-based adjustment
        rsi = stock.get('rsi')
        rsi_adjustment = 0
        if rsi is not None:
            if rsi < 30:  # Oversold - suggest buying below current
                rsi_adjustment = -0.03  # 3% below
            elif rsi < 40:
                rsi_adjustment = -0.015  # 1.5% below
            elif rsi > 70:  # Overbought - wait for pullback
                rsi_adjustment = -0.05  # 5% below
        
        # Strategy-based adjustments
        strategy_multipliers = {
            'Conservative': 0.98,  # More conservative, buy slightly below
            'Default': 1.0,
            'Aggressive': 1.02,  # More aggressive, can buy at or slightly above
            'Momentum': 1.01,  # Momentum strategy, slight premium OK
            'Value': 0.97,  # Value strategy, wait for discount
            'Dividend Focus': 0.99  # Slight discount preferred
        }
        strategy_mult = strategy_multipliers.get(strategy, 1.0)
        
        # Calculate suggested price
        if support_levels:
            # Use the highest support level (closest to current price but below)
            valid_supports = [s[1] for s in support_levels if s[1] < current_price]
            if valid_supports:
                base_support = max(valid_supports)
                suggested_price = base_support * strategy_mult * (1 + rsi_adjustment)
            else:
                # All supports above current, use current with adjustment
                suggested_price = current_price * strategy_mult * (1 + rsi_adjustment)
        else:
            # No support levels, use current price with adjustments
            suggested_price = current_price * strategy_mult * (1 + rsi_adjustment)
        
        # Ensure suggested price is reasonable (within 10% of current)
        suggested_price = max(
            current_price * 0.90,
            min(suggested_price, current_price * 1.10)
        )
        
        # Calculate price range (±2-5% depending on volatility)
        volatility = latest.get('Volatility', 0.02)
        if pd.notna(volatility):
            range_pct = min(max(volatility * 2, 0.02), 0.05)  # 2-5% range
        else:
            range_pct = 0.03  # Default 3%
        
        price_range_low = suggested_price * (1 - range_pct)
        price_range_high = suggested_price * (1 + range_pct)
        
        # Build reasoning
        reasoning_parts = []
        if support_levels:
            closest_support = min(support_levels, key=lambda x: abs(x[1] - suggested_price))
            reasoning_parts.append(f"Based on {closest_support[0]} support level")
        if rsi_adjustment < 0:
            reasoning_parts.append(f"RSI suggests waiting for {abs(rsi_adjustment)*100:.1f}% pullback")
        reasoning_parts.append(f"{strategy} strategy adjustment applied")
        
        reasoning = ". ".join(reasoning_parts) if reasoning_parts else "Based on technical analysis"
        
        return {
            'suggested_price': round(suggested_price, 2),
            'price_range_low': round(price_range_low, 2),
            'price_range_high': round(price_range_high, 2),
            'current_price': round(current_price, 2),
            'discount_pct': round(((current_price - suggested_price) / current_price) * 100, 2),
            'reasoning': reasoning,
            'support_levels': support_levels
        }
    
    def generate_stock_insight(self, stock: Dict) -> str:
        """
        Generate AI-powered insight for a single stock with supportive, clear explanations.
        
        Args:
            stock: Stock data dictionary with all metrics
        
        Returns:
            AI-generated insight text with comprehensive analysis
        """
        symbol = stock['symbol']
        score = stock['score']
        rsi = stock.get('rsi')
        momentum = stock.get('momentum')
        volume_ratio = stock.get('volume_ratio', 0)
        sector = stock.get('sector', 'Unknown')
        current_price = stock['current_price']
        market_cap = stock.get('market_cap', 0)
        volatility = None
        data = stock.get('data')
        
        if data is not None and not data.empty:
            latest = data.iloc[-1]
            volatility = latest.get('Volatility', None)
        
        # Build comprehensive insight with supportive tone
        insights = []
        
        # Opening statement - supportive and clear
        if score >= 90:
            insights.append(f"**🎯 Excellent Opportunity**: {symbol} demonstrates exceptional quantitative strength with a score of **{score:.1f}/100**. This indicates strong technical fundamentals across multiple indicators, making it a compelling candidate for consideration.")
        elif score >= 80:
            insights.append(f"**✅ Strong Candidate**: {symbol} presents a solid investment opportunity with a score of **{score:.1f}/100**. The technical analysis suggests robust fundamentals that align well with quantitative selection criteria.")
        elif score >= 70:
            insights.append(f"**📊 Solid Choice**: {symbol} shows promising characteristics with a score of **{score:.1f}/100**. While not exceptional, it demonstrates enough positive signals to warrant monitoring for potential entry points.")
        else:
            insights.append(f"**⚠️ Moderate Potential**: {symbol} has a score of **{score:.1f}/100**. This suggests the stock may require more careful evaluation or waiting for improved market conditions before considering an investment.")
        
        # Technical Analysis Section
        insights.append("\n**📈 Technical Analysis:**")
        
        # RSI analysis with clear explanations
        if rsi is not None:
            if rsi < 30:
                insights.append(f"• **RSI ({rsi:.1f})**: The stock is significantly oversold, which historically presents buying opportunities. However, ensure this isn't due to fundamental issues. Consider this a potential entry point for contrarian investors.")
            elif rsi < 40:
                insights.append(f"• **RSI ({rsi:.1f})**: Approaching oversold territory, suggesting the stock may be undervalued relative to recent momentum. This could indicate a favorable entry opportunity.")
            elif 40 <= rsi <= 60:
                insights.append(f"• **RSI ({rsi:.1f})**: In a healthy neutral range, indicating balanced market sentiment. This suggests the stock isn't overextended in either direction, providing a stable foundation for investment.")
            elif 60 < rsi <= 70:
                insights.append(f"• **RSI ({rsi:.1f})**: Showing moderate bullish momentum. While positive, be cautious of potential overbought conditions. Consider waiting for a slight pullback for better entry prices.")
            else:
                insights.append(f"• **RSI ({rsi:.1f})**: The stock appears overbought, suggesting recent gains may be unsustainable short-term. **Recommendation**: Wait for a pullback to more reasonable levels before entering.")
        
        # Momentum analysis with context
        if momentum is not None:
            momentum_pct = momentum * 100
            if momentum_pct > 10:
                insights.append(f"• **Momentum (+{momentum_pct:.2f}%)**: Strong positive momentum over the past 20 days indicates sustained buying interest. This suggests institutional confidence and potential trend continuation, though be mindful of potential exhaustion at these levels.")
            elif momentum_pct > 5:
                insights.append(f"• **Momentum (+{momentum_pct:.2f}%)**: Healthy positive momentum suggests the stock is gaining traction. This could signal the early stages of a favorable trend, making it worth monitoring closely.")
            elif momentum_pct > 0:
                insights.append(f"• **Momentum (+{momentum_pct:.2f}%)**: Modest positive momentum indicates slight upward pressure. While encouraging, the trend may need additional confirmation through volume and price action before committing.")
            else:
                insights.append(f"• **Momentum ({momentum_pct:.2f}%)**: Negative momentum suggests the stock may need time to stabilize. **Recommendation**: Exercise patience and wait for clear reversal signals before considering entry.")
        
        # Volume analysis with market context
        if volume_ratio:
            if volume_ratio >= 1.5:
                insights.append(f"• **Volume ({volume_ratio:.2f}x average)**: Exceptional trading volume indicates strong institutional interest and validates recent price movements. This high volume provides confidence that the current trend is supported by real buying pressure.")
            elif volume_ratio >= 1.2:
                insights.append(f"• **Volume ({volume_ratio:.2f}x average)**: Above-average volume suggests increased market attention and confirms recent price action. This is a positive sign that the stock is attracting investor interest.")
            elif volume_ratio >= 0.8:
                insights.append(f"• **Volume ({volume_ratio:.2f}x average)**: Normal trading volume indicates steady market participation. While not exceptional, this level of activity provides adequate liquidity for most investors.")
            else:
                insights.append(f"• **Volume ({volume_ratio:.2f}x average)**: Below-average volume may indicate lack of strong conviction in recent price movements. **Recommendation**: Wait for volume confirmation to validate any potential entry signals.")
        
        # Market Context Section
        insights.append("\n**🌐 Market Context:**")
        
        # Sector analysis
        sector_insights = {
            'Technology': 'Technology stocks are sensitive to innovation cycles and market sentiment. Consider broader tech sector trends and regulatory environment.',
            'Healthcare': 'Healthcare stocks often provide defensive characteristics but can be volatile around regulatory news and clinical trial results.',
            'Financial Services': 'Financial stocks are closely tied to interest rates and economic conditions. Monitor macroeconomic indicators.',
            'Consumer Cyclical': 'Consumer stocks reflect economic health and consumer confidence. Consider economic cycles and spending trends.',
            'Consumer Defensive': 'Defensive stocks typically provide stability during market uncertainty but may have slower growth.',
            'Energy': 'Energy stocks are highly correlated with commodity prices and geopolitical factors. Monitor oil prices and supply dynamics.',
            'Communication Services': 'Communication stocks benefit from digital transformation trends but face regulatory scrutiny.'
        }
        sector_advice = sector_insights.get(sector, f'The {sector} sector has unique characteristics that should be considered in your investment decision.')
        insights.append(f"• **Sector ({sector})**: {sector_advice}")
        
        # Market cap context
        if market_cap > 200_000_000_000:  # > $200B
            insights.append(f"• **Market Cap (${market_cap/1e9:.1f}B)**: Large-cap stock providing stability and liquidity. Typically less volatile but may have slower growth potential.")
        elif market_cap > 10_000_000_000:  # > $10B
            insights.append(f"• **Market Cap (${market_cap/1e9:.1f}B)**: Mid to large-cap stock offering a balance between growth potential and stability.")
        else:
            insights.append(f"• **Market Cap (${market_cap/1e9:.1f}B)**: Smaller market cap may offer higher growth potential but with increased volatility and risk.")
        
        # Risk Assessment
        insights.append("\n**⚠️ Risk Considerations:**")
        if volatility:
            vol_pct = volatility * 100
            if vol_pct > 4:
                insights.append(f"• **Volatility ({vol_pct:.2f}%)**: High volatility indicates significant price swings. This requires a higher risk tolerance and proper position sizing. Consider using stop-loss orders to manage risk.")
            elif vol_pct > 2.5:
                insights.append(f"• **Volatility ({vol_pct:.2f}%)**: Moderate volatility suggests reasonable price stability. This level is manageable for most investors with standard risk management practices.")
            else:
                insights.append(f"• **Volatility ({vol_pct:.2f}%)**: Low volatility indicates stable price action, suitable for conservative investors seeking lower-risk opportunities.")
        else:
            insights.append("• **Volatility**: Unable to assess volatility from available data. Consider this in your risk evaluation.")
        
        # Price accessibility
        if current_price < 50:
            insights.append(f"• **Price (${current_price:.2f})**: Accessible price point suitable for smaller portfolios while maintaining good liquidity.")
        elif current_price > 200:
            insights.append(f"• **Price (${current_price:.2f})**: Premium price point typically associated with established companies. May appeal to institutional investors but requires larger capital allocation.")
        else:
            insights.append(f"• **Price (${current_price:.2f})**: Moderate price point providing flexibility for various portfolio sizes.")
        
        # Closing supportive statement
        if score >= 80:
            insights.append(f"\n**💡 Bottom Line**: {symbol} presents a strong quantitative case with multiple positive technical indicators. However, always complement this analysis with fundamental research, consider your risk tolerance, and ensure it aligns with your overall investment strategy.")
        else:
            insights.append(f"\n**💡 Bottom Line**: While {symbol} shows some positive signals, consider waiting for stronger confirmation or exploring other opportunities. Remember, quantitative analysis is one tool—combine it with fundamental analysis and your investment goals.")
        
        return "\n".join(insights)
    
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
        Generate AI-powered recommendation for a stock with clear, supportive reasoning.
        
        Args:
            stock: Stock data dictionary
        
        Returns:
            Dictionary with recommendation details and comprehensive reasoning
        """
        symbol = stock['symbol']
        score = stock['score']
        buy_signal = stock.get('buy_signal', False)
        rsi = stock.get('rsi')
        momentum = stock.get('momentum')
        volume_ratio = stock.get('volume_ratio', 0)
        
        # Determine confidence level
        confidence_score = 0
        if score >= 80:
            confidence_score += 3
        elif score >= 60:
            confidence_score += 2
        else:
            confidence_score += 1
        
        if buy_signal:
            confidence_score += 2
        
        if rsi and 30 <= rsi <= 50:
            confidence_score += 1
        
        if momentum and momentum > 0.03:
            confidence_score += 1
        
        if volume_ratio and volume_ratio >= 1.2:
            confidence_score += 1
        
        if confidence_score >= 6:
            confidence = 'High'
        elif confidence_score >= 4:
            confidence = 'Medium'
        else:
            confidence = 'Low'
        
        recommendation = {
            'symbol': symbol,
            'action': 'BUY' if buy_signal else 'HOLD',
            'confidence': confidence,
            'reasoning': [],
            'risk_level': 'Low',
            'time_horizon': 'Short-term',
            'detailed_reasoning': []
        }
        
        # Determine risk level with context
        volatility = None
        if stock.get('data') is not None and not stock['data'].empty:
            volatility = stock['data'].iloc[-1].get('Volatility', None)
        
        if volatility:
            if volatility > 0.04:
                recommendation['risk_level'] = 'High'
                recommendation['detailed_reasoning'].append(f"High volatility ({volatility*100:.2f}%) indicates significant price swings. This requires careful risk management and position sizing.")
            elif volatility > 0.025:
                recommendation['risk_level'] = 'Medium'
                recommendation['detailed_reasoning'].append(f"Moderate volatility ({volatility*100:.2f}%) suggests manageable risk with standard risk management practices.")
            else:
                recommendation['risk_level'] = 'Low'
                recommendation['detailed_reasoning'].append(f"Low volatility ({volatility*100:.2f}%) indicates stable price action, suitable for risk-averse investors.")
        
        # Determine time horizon with explanation
        if momentum and momentum > 0.05:
            recommendation['time_horizon'] = 'Short to Medium-term (1-6 months)'
            recommendation['detailed_reasoning'].append("Strong momentum suggests potential for near-term gains, making this suitable for shorter holding periods.")
        elif momentum and momentum > 0:
            recommendation['time_horizon'] = 'Medium-term (3-12 months)'
            recommendation['detailed_reasoning'].append("Moderate momentum indicates steady growth potential over the medium term.")
        else:
            recommendation['time_horizon'] = 'Long-term (1+ years)'
            recommendation['detailed_reasoning'].append("Lower momentum suggests this may be better suited for long-term value appreciation rather than quick gains.")
        
        # Build comprehensive reasoning
        if buy_signal:
            recommendation['reasoning'].append("✅ Strong BUY signal from technical analysis")
            recommendation['detailed_reasoning'].append("Multiple technical indicators align to suggest a favorable entry point. The combination of RSI, moving averages, MACD, and momentum creates a compelling technical case.")
        else:
            recommendation['reasoning'].append("⏸️ HOLD - Waiting for stronger signals")
            recommendation['detailed_reasoning'].append("While the stock shows some positive characteristics, the technical indicators haven't aligned strongly enough to generate a clear BUY signal. Consider monitoring for improved entry conditions.")
        
        if score >= 80:
            recommendation['reasoning'].append(f"⭐ Exceptional quantitative score ({score:.1f}/100)")
            recommendation['detailed_reasoning'].append(f"The high score of {score:.1f}/100 indicates strong performance across multiple quantitative factors including momentum, RSI, moving averages, MACD, and volume. This suggests a high-quality opportunity.")
        elif score >= 60:
            recommendation['reasoning'].append(f"📊 Solid quantitative score ({score:.1f}/100)")
            recommendation['detailed_reasoning'].append(f"The score of {score:.1f}/100 shows decent technical fundamentals, though not exceptional. This suggests moderate opportunity with room for improvement.")
        else:
            recommendation['reasoning'].append(f"⚠️ Lower quantitative score ({score:.1f}/100)")
            recommendation['detailed_reasoning'].append(f"The score of {score:.1f}/100 indicates weaker technical signals. Consider waiting for improved conditions or exploring other opportunities.")
        
        if rsi and 30 <= rsi <= 50:
            recommendation['reasoning'].append(f"📈 RSI ({rsi:.1f}) suggests favorable entry")
            recommendation['detailed_reasoning'].append(f"RSI of {rsi:.1f} is in the optimal range for entry, indicating the stock is not overbought and may have room for upward movement.")
        elif rsi and rsi > 70:
            recommendation['reasoning'].append(f"⚠️ RSI ({rsi:.1f}) indicates overbought conditions")
            recommendation['detailed_reasoning'].append(f"RSI of {rsi:.1f} suggests the stock may be overextended. Consider waiting for a pullback to more reasonable levels.")
        
        if momentum and momentum > 0.03:
            recommendation['reasoning'].append(f"🚀 Strong momentum ({momentum*100:.2f}%)")
            recommendation['detailed_reasoning'].append(f"Positive momentum of {momentum*100:.2f}% indicates sustained buying interest and potential trend continuation.")
        elif momentum and momentum <= 0:
            recommendation['reasoning'].append(f"📉 Negative momentum ({momentum*100:.2f}%)")
            recommendation['detailed_reasoning'].append(f"Negative momentum suggests the stock may need time to stabilize. Exercise patience and wait for reversal signals.")
        
        if volume_ratio and volume_ratio >= 1.2:
            recommendation['reasoning'].append(f"📊 High volume ({volume_ratio:.2f}x) confirms interest")
            recommendation['detailed_reasoning'].append(f"Above-average volume ({volume_ratio:.2f}x) validates recent price movements and indicates strong market participation.")
        
        # Build summary with supportive tone
        action_emoji = "✅" if buy_signal else "⏸️"
        confidence_emoji = "🟢" if confidence == 'High' else "🟡" if confidence == 'Medium' else "🔴"
        
        recommendation['summary'] = f"{action_emoji} **{recommendation['action']}** {symbol} with {confidence_emoji} **{confidence} confidence**"
        recommendation['summary'] += f"\n\n**Risk Level**: {recommendation['risk_level']}"
        recommendation['summary'] += f"\n**Time Horizon**: {recommendation['time_horizon']}"
        
        if recommendation['detailed_reasoning']:
            recommendation['summary'] += "\n\n**Why this recommendation?**\n"
            for i, reason in enumerate(recommendation['detailed_reasoning'], 1):
                recommendation['summary'] += f"{i}. {reason}\n"
        
        recommendation['summary'] += "\n**💡 Remember**: This is quantitative analysis based on technical indicators. Always complement with fundamental research, consider your risk tolerance, and ensure alignment with your investment goals."
        
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

