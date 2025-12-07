"""
Interactive Web UI for Quantitative Stock Selection System.
Built with Streamlit for a modern, interactive experience.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import DataFetcher
from stock_selector import StockSelector
from trading_strategy import TradingStrategy
from ai_insights import AIInsights
import config


# Page configuration
APP_NAME = "Quantify 701"
APP_BRAND = "The Studio 701 LLC"
APP_TAGLINE = "Quantify Your Investment Decisions"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/kevintan701/quantify701',
        'Report a bug': 'https://github.com/kevintan701/quantify701/issues',
        'About': f"{APP_NAME} - {APP_TAGLINE}\n\nPowered by {APP_BRAND}"
    }
)

# Enhanced CSS for modern, professional styling
st.markdown("""
    <style>
    /* Main Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    /* Success/Info boxes */
    .stSuccess {
        border-left: 4px solid #10b981;
        border-radius: 8px;
    }
    
    .stInfo {
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #667eea;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    
    /* Score badges */
    .score-high {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
    }
    
    .score-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
    }
    
    .score-low {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)


def get_strategy_presets():
    """Define strategy presets with different filter configurations."""
    return {
        "Default": {
            'min_market_cap': 10_000_000_000,
            'min_volume': 1_000_000,
            'min_price': 5.0,
            'max_price': 1000.0,
            'min_rsi': 25,
            'max_rsi': 75,
            'min_volume_ratio': 0.5,
            'min_data_points': 200,
            'max_volatility': 0.05
        },
        "Conservative": {
            'min_market_cap': 50_000_000_000,  # Larger companies
            'min_volume': 2_000_000,  # Higher liquidity
            'min_price': 10.0,
            'max_price': 500.0,
            'min_rsi': 30,
            'max_rsi': 70,  # Avoid extremes
            'min_volume_ratio': 0.8,  # Higher volume requirement
            'min_data_points': 200,
            'max_volatility': 0.03  # Lower volatility
        },
        "Aggressive": {
            'min_market_cap': 5_000_000_000,  # Smaller companies OK
            'min_volume': 500_000,  # Lower volume requirement
            'min_price': 5.0,
            'max_price': 1000.0,
            'min_rsi': 20,  # Allow more oversold
            'max_rsi': 80,  # Allow more overbought
            'min_volume_ratio': 0.3,  # Lower volume ratio
            'min_data_points': 200,
            'max_volatility': 0.08  # Higher volatility allowed
        },
        "Momentum": {
            'min_market_cap': 10_000_000_000,
            'min_volume': 1_500_000,  # Higher volume for momentum
            'min_price': 5.0,
            'max_price': 1000.0,
            'min_rsi': 40,  # Prefer not oversold
            'max_rsi': 70,
            'min_volume_ratio': 1.0,  # Above average volume
            'min_data_points': 200,
            'max_volatility': 0.06
        },
        "Value": {
            'min_market_cap': 20_000_000_000,  # Established companies
            'min_volume': 1_000_000,
            'min_price': 5.0,
            'max_price': 200.0,  # Lower price range
            'min_rsi': 25,  # Allow oversold (value opportunities)
            'max_rsi': 65,  # Avoid overbought
            'min_volume_ratio': 0.5,
            'min_data_points': 200,
            'max_volatility': 0.04  # Lower volatility
        },
        "Dividend Focus": {
            'min_market_cap': 30_000_000_000,  # Large, stable companies
            'min_volume': 1_000_000,
            'min_price': 10.0,
            'max_price': 300.0,
            'min_rsi': 30,
            'max_rsi': 70,
            'min_volume_ratio': 0.6,
            'min_data_points': 200,
            'max_volatility': 0.035  # Low volatility for income
        }
    }


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_stock_data(custom_filters=None):
    """Fetch and analyze stocks with caching."""
    data_fetcher = DataFetcher()
    stock_selector = StockSelector(data_fetcher)
    
    with st.spinner("Analyzing stocks... This may take a minute."):
        qualified_stocks = stock_selector.filter_stocks(config.STOCK_UNIVERSE, custom_filters=custom_filters)
    
    return qualified_stocks, data_fetcher


def create_stocks_dataframe(stocks):
    """Convert stock list to DataFrame for display with enhanced formatting."""
    data = []
    for idx, stock in enumerate(stocks):
        # Determine score color category
        score = stock['score']
        if score >= 80:
            score_display = f"🟢 {score:.1f}"
        elif score >= 60:
            score_display = f"🟡 {score:.1f}"
        else:
            score_display = f"🔴 {score:.1f}"
        
        # Format buy signal
        buy_signal = "✅ BUY" if stock.get('buy_signal') else "⏸️ HOLD"
        
        data.append({
            'Rank': idx + 1,
            'Symbol': stock['symbol'],
            'Score': score_display,
            'Signal': buy_signal,
            'Price': f"${stock['current_price']:.2f}",
            'RSI': f"{stock['rsi']:.1f}" if stock['rsi'] else "N/A",
            'Momentum': f"{stock['momentum']*100:+.2f}%" if stock['momentum'] else "N/A",
            'Volume': f"{stock.get('volume_ratio', 0):.2f}x" if stock.get('volume_ratio') else "N/A",
            'Market Cap': f"${stock['market_cap']/1e9:.1f}B",
            'Sector': stock['sector']
        })
    
    return pd.DataFrame(data)


def create_price_chart(stock_data, symbol):
    """Create interactive price chart with technical indicators."""
    data = stock_data['data']
    if data is None or data.empty:
        return None
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=('Price & Moving Averages', 'RSI', 'MACD'),
        row_heights=[0.5, 0.25, 0.25]
    )
    
    # Price and moving averages
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], name='Price', line=dict(color='#1f77b4')),
        row=1, col=1
    )
    
    if 'SMA_20' in data.columns:
        fig.add_trace(
            go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20', line=dict(color='orange', dash='dash')),
            row=1, col=1
        )
    
    if 'SMA_50' in data.columns:
        fig.add_trace(
            go.Scatter(x=data.index, y=data['SMA_50'], name='SMA 50', line=dict(color='red', dash='dash')),
            row=1, col=1
        )
    
    # RSI
    if 'RSI' in data.columns:
        fig.add_trace(
            go.Scatter(x=data.index, y=data['RSI'], name='RSI', line=dict(color='purple')),
            row=2, col=1
        )
        # Add RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1, annotation_text="Overbought (70)")
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1, annotation_text="Oversold (30)")
    
    # MACD
    if 'MACD' in data.columns and 'MACD_Signal' in data.columns:
        fig.add_trace(
            go.Scatter(x=data.index, y=data['MACD'], name='MACD', line=dict(color='blue')),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(x=data.index, y=data['MACD_Signal'], name='Signal', line=dict(color='red')),
            row=3, col=1
        )
        # MACD Histogram
        if 'MACD_Histogram' in data.columns:
            colors = ['green' if x >= 0 else 'red' for x in data['MACD_Histogram']]
            fig.add_trace(
                go.Bar(x=data.index, y=data['MACD_Histogram'], name='Histogram', marker_color=colors),
                row=3, col=1
            )
    
    # Enhanced chart styling
    fig.update_layout(
        height=800,
        title={
            'text': f"{symbol} - Technical Analysis",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#667eea'}
        },
        showlegend=True,
        hovermode='x unified',
        template='plotly_white',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update axes styling
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig


def main():
    """Main application function."""
    # Enhanced Header with subtitle
    st.markdown(f'<h1 class="main-header">📈 {APP_NAME}</h1>', unsafe_allow_html=True)
    st.markdown(
        f'<p style="text-align: center; color: #666; font-size: 1.1rem; margin-top: -1rem; margin-bottom: 0.5rem;">'
        f'🤖 {APP_TAGLINE} - AI-Powered Quantitative Analysis Platform</p>'
        f'<p style="text-align: center; color: #999; font-size: 0.9rem; margin-bottom: 2rem;">'
        f'Powered by {APP_BRAND}</p>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Strategy Presets
        st.subheader("📋 Strategy Presets")
        strategy_presets = get_strategy_presets()
        selected_strategy = st.selectbox(
            "Select a strategy preset",
            options=list(strategy_presets.keys()),
            index=0,
            help="Choose a pre-configured strategy or use 'Custom' to adjust filters manually"
        )
        
        use_custom = st.checkbox("Use custom filters", value=False, help="Enable to manually adjust filter criteria")
        
        # Custom Filter Settings (shown when custom is enabled)
        if use_custom or selected_strategy == "Default":
            st.subheader("🔧 Custom Filter Settings")
            
            with st.expander("Market Filters", expanded=False):
                min_market_cap = st.number_input(
                    "Min Market Cap (B)", 
                    min_value=1.0, 
                    max_value=1000.0, 
                    value=float(strategy_presets[selected_strategy]['min_market_cap']/1e9),
                    step=1.0,
                    help="Minimum market capitalization in billions"
                )
                min_volume = st.number_input(
                    "Min Daily Volume", 
                    min_value=100_000, 
                    max_value=10_000_000, 
                    value=int(strategy_presets[selected_strategy]['min_volume']),
                    step=100_000,
                    format="%d",
                    help="Minimum daily trading volume"
                )
            
            with st.expander("Price Filters", expanded=False):
                min_price = st.number_input(
                    "Min Price ($)", 
                    min_value=1.0, 
                    max_value=100.0, 
                    value=float(strategy_presets[selected_strategy]['min_price']),
                    step=1.0
                )
                max_price = st.number_input(
                    "Max Price ($)", 
                    min_value=10.0, 
                    max_value=2000.0, 
                    value=float(strategy_presets[selected_strategy]['max_price']),
                    step=10.0
                )
            
            with st.expander("Technical Filters", expanded=False):
                min_rsi = st.slider(
                    "Min RSI", 
                    min_value=0, 
                    max_value=50, 
                    value=int(strategy_presets[selected_strategy]['min_rsi'])
                )
                max_rsi = st.slider(
                    "Max RSI", 
                    min_value=50, 
                    max_value=100, 
                    value=int(strategy_presets[selected_strategy]['max_rsi'])
                )
                max_volatility = st.slider(
                    "Max Volatility (%)", 
                    min_value=1, 
                    max_value=10, 
                    value=int(strategy_presets[selected_strategy]['max_volatility']*100)
                )
                min_volume_ratio = st.slider(
                    "Min Volume Ratio", 
                    min_value=0.0, 
                    max_value=2.0, 
                    value=float(strategy_presets[selected_strategy]['min_volume_ratio']),
                    step=0.1
                )
        else:
            # Show strategy description
            strategy_descriptions = {
                "Conservative": "Focus on large-cap, low-volatility stocks. Lower risk, stable returns.",
                "Aggressive": "Includes smaller companies and higher volatility. Higher risk, potential for higher returns.",
                "Momentum": "Emphasizes stocks with strong price momentum and high volume. Trend-following strategy.",
                "Value": "Targets established companies at reasonable prices. Value investing approach.",
                "Dividend Focus": "Prioritizes large, stable companies suitable for income investing."
            }
            if selected_strategy in strategy_descriptions:
                st.info(f"**{selected_strategy} Strategy:**\n{strategy_descriptions[selected_strategy]}")
        
        # Analysis options
        st.subheader("📊 Analysis Options")
        top_n = st.slider("Number of stocks to display", 10, 50, 20)
        min_score = st.slider("Minimum score filter", 0, 100, 0)
        
        # Filter options
        st.subheader("🔍 Display Filters")
        sectors = st.multiselect(
            "Filter by Sector",
            options=["Technology", "Healthcare", "Financial Services", "Consumer Cyclical", 
                    "Communication Services", "Energy", "Consumer Defensive"],
            default=[]
        )
        
        show_buy_signals_only = st.checkbox("Show BUY signals only", value=False)
        
        # Prepare custom filters
        if use_custom or selected_strategy == "Default":
            custom_filters = {
                'min_market_cap': min_market_cap * 1e9,
                'min_volume': int(min_volume),
                'min_price': min_price,
                'max_price': max_price,
                'min_rsi': min_rsi,
                'max_rsi': max_rsi,
                'min_volume_ratio': min_volume_ratio,
                'min_data_points': 200,
                'max_volatility': max_volatility / 100
            }
        else:
            custom_filters = strategy_presets[selected_strategy]
        
        # Refresh button
        st.markdown("---")
        refresh_data = st.button("🔄 Refresh Analysis", type="primary")
        
        if refresh_data:
            st.cache_data.clear()
            st.rerun()
    
    # Initialize system
    if 'qualified_stocks' not in st.session_state or refresh_data or 'custom_filters' not in st.session_state or st.session_state.get('custom_filters') != custom_filters:
        qualified_stocks, data_fetcher = get_stock_data(custom_filters=custom_filters)
        st.session_state.qualified_stocks = qualified_stocks
        st.session_state.data_fetcher = data_fetcher
        st.session_state.custom_filters = custom_filters
        st.session_state.selected_strategy = selected_strategy
    else:
        qualified_stocks = st.session_state.qualified_stocks
        data_fetcher = st.session_state.data_fetcher
    
    if not qualified_stocks:
        st.error("No qualified stocks found. Please check your configuration.")
        return
    
    # Generate buy signals
    strategy = TradingStrategy()
    buy_signals = []
    for stock in qualified_stocks:
        should_buy, reason = strategy.generate_buy_signal(stock)
        stock['buy_signal'] = should_buy
        stock['buy_reason'] = reason
        if should_buy:
            buy_signals.append(stock)
    
    # Apply filters
    filtered_stocks = qualified_stocks[:top_n]
    
    if min_score > 0:
        filtered_stocks = [s for s in filtered_stocks if s['score'] >= min_score]
    
    if sectors:
        filtered_stocks = [s for s in filtered_stocks if s['sector'] in sectors]
    
    if show_buy_signals_only:
        filtered_stocks = [s for s in filtered_stocks if s.get('buy_signal', False)]
    
    # Enhanced Summary metrics with visual cards
    st.markdown("### 📊 Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 12px; text-align: center; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="color: white; margin: 0; font-size: 2rem;">{len(config.STOCK_UNIVERSE)}</h3>
                <p style="color: white; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Total Analyzed</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                        padding: 1.5rem; border-radius: 12px; text-align: center; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="color: white; margin: 0; font-size: 2rem;">{len(qualified_stocks)}</h3>
                <p style="color: white; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Qualified Stocks</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
                        padding: 1.5rem; border-radius: 12px; text-align: center; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="color: white; margin: 0; font-size: 2rem;">{len(buy_signals)}</h3>
                <p style="color: white; margin: 0.5rem 0 0 0; font-size: 0.9rem;">BUY Signals</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        qualification_rate = (len(qualified_stocks) / len(config.STOCK_UNIVERSE)) * 100
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                        padding: 1.5rem; border-radius: 12px; text-align: center; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="color: white; margin: 0; font-size: 2rem;">{qualification_rate:.1f}%</h3>
                <p style="color: white; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Qualification Rate</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Main content area
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Stock Rankings", 
        "📈 Top Recommendations", 
        "🔍 Stock Details", 
        "🤖 AI Insights",
        "📚 How It Works"
    ])
    
    with tab1:
        st.markdown("### 📊 Stock Rankings")
        st.markdown("Ranked by quantitative score (0-100). Higher scores indicate better opportunities.")
        
        if not filtered_stocks:
            st.warning("No stocks match your current filters. Try adjusting your criteria.")
        else:
            # Create and display DataFrame
            df = create_stocks_dataframe(filtered_stocks)
            
            # Display with better formatting
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=600
            )
            
            # Statistics row
            if filtered_stocks:
                avg_score = sum(s['score'] for s in filtered_stocks) / len(filtered_stocks)
                high_scores = sum(1 for s in filtered_stocks if s['score'] >= 80)
                
                stat_col1, stat_col2, stat_col3 = st.columns(3)
                with stat_col1:
                    st.metric("Average Score", f"{avg_score:.1f}")
                with stat_col2:
                    st.metric("High Scores (≥80)", high_scores)
                with stat_col3:
                    st.metric("BUY Signals", sum(1 for s in filtered_stocks if s.get('buy_signal', False)))
            
            # Download button with better styling
            csv = df.to_csv(index=False)
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name=f"stock_selection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    with tab2:
        st.markdown("### 📈 Top BUY Recommendations")
        st.markdown("Stocks with strong BUY signals based on technical analysis.")
        
        if buy_signals:
            # Sort by score
            top_buy = sorted(buy_signals, key=lambda x: x['score'], reverse=True)[:10]
            
            # Summary cards at top
            st.markdown("#### 🎯 Quick Overview")
            quick_col1, quick_col2, quick_col3 = st.columns(3)
            with quick_col1:
                avg_buy_score = sum(s['score'] for s in top_buy) / len(top_buy)
                st.metric("Avg BUY Score", f"{avg_buy_score:.1f}")
            with quick_col2:
                st.metric("Top Recommendations", len(top_buy))
            with quick_col3:
                top_sector = max(set(s['sector'] for s in top_buy), key=list(s['sector'] for s in top_buy).count)
                st.metric("Top Sector", top_sector)
            
            st.markdown("---")
            
            # Individual stock cards
            for i, stock in enumerate(top_buy, 1):
                # Score badge color
                score = stock['score']
                if score >= 90:
                    badge_color = "🟢"
                elif score >= 80:
                    badge_color = "🟡"
                else:
                    badge_color = "🔴"
                
                with st.expander(
                    f"{badge_color} **#{i}. {stock['symbol']}** - Score: **{stock['score']:.1f}/100** | "
                    f"Price: ${stock['current_price']:.2f} | Sector: {stock['sector']}",
                    expanded=(i <= 3)  # Expand first 3 by default
                ):
                    # Metrics in a grid
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.metric("💰 Price", f"${stock['current_price']:.2f}")
                        st.metric("📊 RSI", f"{stock['rsi']:.1f}" if stock['rsi'] else "N/A")
                    
                    with metric_col2:
                        st.metric("📈 Momentum", f"{stock['momentum']*100:+.2f}%" if stock['momentum'] else "N/A")
                        st.metric("📦 Market Cap", f"${stock['market_cap']/1e9:.1f}B")
                    
                    with metric_col3:
                        st.metric("🏢 Sector", stock['sector'])
                        st.metric("📊 Volume Ratio", f"{stock.get('volume_ratio', 0):.2f}x" if stock.get('volume_ratio') else "N/A")
                    
                    with metric_col4:
                        # Score visualization
                        st.markdown("**Score Breakdown**")
                        score_progress = score / 100
                        st.progress(score_progress)
                        st.caption(f"{score:.1f}/100")
                    
                    # BUY signal reason in highlighted box
                    st.success(f"✅ **BUY Signal:** {stock['buy_reason']}")
                    
                    # AI Insight for each recommendation
                    st.markdown("#### 🤖 AI Insight")
                    ai = AIInsights()
                    ai_insight = ai.generate_stock_insight(stock)
                    st.info(ai_insight)
                    
                    # AI Recommendation
                    recommendation = ai.generate_recommendation(stock)
                    st.markdown(f"**AI Recommendation**: {recommendation['summary']}")
                    
                    # Show chart
                    st.markdown("#### 📊 Price Chart & Technical Analysis")
                    chart = create_price_chart(stock, stock['symbol'])
                    if chart:
                        st.plotly_chart(chart, use_container_width=True, key=f"chart_buy_{stock['symbol']}_{i}")
        else:
            st.warning("⚠️ No BUY signals found in the current analysis. Try adjusting your filters or strategy.")
            st.info("💡 **Tip:** Try using the 'Momentum' or 'Aggressive' strategy presets for more BUY signals.")
    
    with tab3:
        st.markdown("### 🔍 Detailed Stock Analysis")
        st.markdown("Select a stock to view comprehensive technical analysis and indicators.")
        
        if not filtered_stocks:
            st.warning("No stocks available. Please adjust your filters.")
        else:
            # Stock selector with search
            stock_symbols = [s['symbol'] for s in filtered_stocks]
            selected_symbol = st.selectbox(
                "🔎 Select a stock to analyze", 
                stock_symbols,
                help="Choose a stock from the filtered list to see detailed analysis"
            )
        
        if selected_symbol:
            selected_stock = next((s for s in filtered_stocks if s['symbol'] == selected_symbol), None)
            
            if selected_stock:
                # Enhanced stock overview with visual cards
                st.markdown(f"#### 📊 {selected_stock['symbol']} - Overview")
                
                # Score visualization
                score = selected_stock['score']
                score_col1, score_col2 = st.columns([2, 1])
                with score_col1:
                    st.markdown(f"**Overall Score: {score:.1f}/100**")
                    st.progress(score / 100)
                with score_col2:
                    if score >= 80:
                        st.success("🟢 High Score")
                    elif score >= 60:
                        st.warning("🟡 Medium Score")
                    else:
                        st.error("🔴 Low Score")
                
                # Metrics in grid
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown("**💰 Price & Value**")
                    st.metric("Current Price", f"${selected_stock['current_price']:.2f}")
                    st.metric("Market Cap", f"${selected_stock['market_cap']/1e9:.1f}B")
                
                with col2:
                    st.markdown("**📈 Technical Indicators**")
                    st.metric("RSI", f"{selected_stock['rsi']:.1f}" if selected_stock['rsi'] else "N/A")
                    st.metric("Momentum", f"{selected_stock['momentum']*100:+.2f}%" if selected_stock['momentum'] else "N/A")
                
                with col3:
                    st.markdown("**📊 Market Data**")
                    st.metric("Sector", selected_stock['sector'])
                    st.metric("Volume Ratio", f"{selected_stock.get('volume_ratio', 0):.2f}x" if selected_stock.get('volume_ratio') else "N/A")
                
                with col4:
                    st.markdown("**🎯 Signal**")
                    signal_status = "✅ BUY" if selected_stock.get('buy_signal') else "⏸️ HOLD"
                    if selected_stock.get('buy_signal'):
                        st.success(f"**{signal_status}**")
                    else:
                        st.info(f"**{signal_status}**")
                    st.caption("Based on technical analysis")
                
                # Technical indicators with better formatting
                st.markdown("---")
                st.markdown("#### 🔬 Technical Indicators")
                
                data = selected_stock.get('data')
                if data is not None and not data.empty:
                    latest = data.iloc[-1]
                    
                    tech_col1, tech_col2, tech_col3 = st.columns(3)
                    
                    with tech_col1:
                        st.markdown("**📈 Moving Averages**")
                        sma20 = latest.get('SMA_20', None)
                        sma50 = latest.get('SMA_50', None)
                        current_price = selected_stock['current_price']
                        
                        if pd.notna(sma20):
                            price_vs_sma20 = ((current_price - sma20) / sma20) * 100
                            st.metric("SMA 20", f"${sma20:.2f}", f"{price_vs_sma20:+.1f}%")
                        else:
                            st.metric("SMA 20", "N/A")
                        
                        if pd.notna(sma50):
                            price_vs_sma50 = ((current_price - sma50) / sma50) * 100
                            st.metric("SMA 50", f"${sma50:.2f}", f"{price_vs_sma50:+.1f}%")
                        else:
                            st.metric("SMA 50", "N/A")
                    
                    with tech_col2:
                        st.markdown("**📊 MACD**")
                        macd = latest.get('MACD', None)
                        macd_signal = latest.get('MACD_Signal', None)
                        
                        if pd.notna(macd):
                            macd_diff = macd - macd_signal if pd.notna(macd_signal) else 0
                            st.metric("MACD", f"{macd:.2f}", f"{macd_diff:+.2f}" if macd_diff != 0 else "")
                        else:
                            st.metric("MACD", "N/A")
                        
                        if pd.notna(macd_signal):
                            st.metric("Signal", f"{macd_signal:.2f}")
                        else:
                            st.metric("Signal", "N/A")
                        
                        # MACD trend
                        if pd.notna(macd) and pd.notna(macd_signal):
                            if macd > macd_signal:
                                st.success("🟢 Bullish")
                            else:
                                st.error("🔴 Bearish")
                    
                    with tech_col3:
                        st.markdown("**📉 Volatility & Bands**")
                        volatility = latest.get('Volatility', None)
                        if pd.notna(volatility):
                            st.metric("Volatility", f"{volatility*100:.2f}%")
                        else:
                            st.metric("Volatility", "N/A")
                        
                        bb_upper = latest.get('BB_Upper', None)
                        bb_lower = latest.get('BB_Lower', None)
                        if pd.notna(bb_upper) and pd.notna(bb_lower):
                            bb_position = (current_price - bb_lower) / (bb_upper - bb_lower)
                            st.metric("BB Position", f"{bb_position*100:.1f}%")
                            if bb_position < 0.2:
                                st.info("Near lower band (potentially oversold)")
                            elif bb_position > 0.8:
                                st.warning("Near upper band (potentially overbought)")
                        else:
                            st.metric("BB Position", "N/A")
                
                # Price chart with enhanced styling
                st.markdown("---")
                st.markdown("#### 📈 Price Chart & Technical Analysis")
                chart = create_price_chart(selected_stock, selected_symbol)
                if chart:
                    st.plotly_chart(chart, use_container_width=True, key=f"chart_detail_{selected_symbol}")
                
                # Buy signal info with better formatting
                st.markdown("---")
                if selected_stock.get('buy_signal'):
                    st.success(f"✅ **BUY Signal Detected**\n\n{selected_stock['buy_reason']}")
                else:
                    st.info(f"ℹ️ **Analysis:** {selected_stock['buy_reason']}")
                
                # AI Insight for selected stock
                st.markdown("---")
                st.markdown("#### 🤖 AI Insight")
                ai = AIInsights()
                ai_insight = ai.generate_stock_insight(selected_stock)
                st.info(ai_insight)
                
                # AI Recommendation
                st.markdown("#### 🎯 AI Recommendation")
                recommendation = ai.generate_recommendation(selected_stock)
                st.success(recommendation['summary'])
                
                # Score Explanation
                st.markdown("#### 📊 Score Explanation")
                score_explanation = ai.explain_score(selected_stock)
                st.markdown(score_explanation)
    
    with tab4:
        st.markdown("### 🤖 AI Insights & Analysis")
        st.markdown("AI-powered insights, recommendations, and market sentiment analysis.")
        
        # Initialize AI Insights
        ai = AIInsights()
        
        # Market Sentiment Section
        st.markdown("#### 📊 Market Sentiment Analysis")
        market_sentiment = ai.generate_market_sentiment(qualified_stocks)
        st.markdown(market_sentiment)
        
        st.markdown("---")
        
        # Portfolio Insight
        st.markdown("#### 💡 Portfolio Overview Insight")
        portfolio_insight = ai.generate_portfolio_insight(filtered_stocks if filtered_stocks else qualified_stocks)
        st.info(portfolio_insight)
        
        st.markdown("---")
        
        # Individual Stock AI Insights
        st.markdown("#### 🔍 AI Stock Analysis")
        st.markdown("Select stocks to view AI-powered insights and recommendations.")
        
        if filtered_stocks:
            # Stock selector for AI insights
            insight_stocks = [s['symbol'] for s in filtered_stocks]
            selected_ai_stock = st.selectbox(
                "Select a stock for AI analysis",
                insight_stocks,
                help="Choose a stock to see detailed AI insights"
            )
            
            if selected_ai_stock:
                selected_ai_stock_data = next((s for s in filtered_stocks if s['symbol'] == selected_ai_stock), None)
                
                if selected_ai_stock_data:
                    # AI Insight
                    st.markdown(f"##### 📈 AI Insight for {selected_ai_stock}")
                    insight = ai.generate_stock_insight(selected_ai_stock_data)
                    st.markdown(insight)
                    
                    st.markdown("---")
                    
                    # AI Recommendation
                    st.markdown("##### 🎯 AI Recommendation")
                    recommendation = ai.generate_recommendation(selected_ai_stock_data)
                    
                    rec_col1, rec_col2, rec_col3 = st.columns(3)
                    with rec_col1:
                        if recommendation['action'] == 'BUY':
                            st.success(f"**Action: {recommendation['action']}**")
                        else:
                            st.info(f"**Action: {recommendation['action']}**")
                    
                    with rec_col2:
                        if recommendation['confidence'] == 'High':
                            st.success(f"**Confidence: {recommendation['confidence']}**")
                        elif recommendation['confidence'] == 'Medium':
                            st.warning(f"**Confidence: {recommendation['confidence']}**")
                        else:
                            st.info(f"**Confidence: {recommendation['confidence']}**")
                    
                    with rec_col3:
                        if recommendation['risk_level'] == 'Low':
                            st.success(f"**Risk: {recommendation['risk_level']}**")
                        elif recommendation['risk_level'] == 'Medium':
                            st.warning(f"**Risk: {recommendation['risk_level']}**")
                        else:
                            st.error(f"**Risk: {recommendation['risk_level']}**")
                    
                    st.markdown(f"**Time Horizon**: {recommendation['time_horizon']}")
                    
                    if recommendation['reasoning']:
                        st.markdown("**Key Reasoning:**")
                        for reason in recommendation['reasoning']:
                            st.markdown(f"- {reason}")
                    
                    st.markdown("---")
                    
                    # Score Explanation
                    st.markdown("##### 📊 Score Explanation")
                    score_explanation = ai.explain_score(selected_ai_stock_data)
                    st.markdown(score_explanation)
        else:
            st.warning("No stocks available for AI analysis. Please adjust your filters.")
        
        st.markdown("---")
        
        # AI Features Info
        with st.expander("ℹ️ About AI Features"):
            st.markdown("""
            **AI-Powered Analysis Features:**
            
            - **Stock Insights**: Comprehensive analysis combining technical indicators, momentum, and market factors
            - **Recommendations**: Actionable BUY/HOLD recommendations with confidence levels and risk assessment
            - **Score Explanations**: Detailed breakdown of why stocks received their quantitative scores
            - **Market Sentiment**: Overall market analysis based on the current stock selection
            - **Portfolio Insights**: High-level analysis of your selected portfolio
            
            **Future AI Enhancements:**
            - Natural language queries about stocks
            - Predictive price forecasting
            - News sentiment analysis
            - Risk-adjusted portfolio optimization
            - Automated strategy suggestions
            """)
    
    with tab5:
        st.header("📚 Stock Selection Process Explained")
        
        st.markdown("""
        This section explains how our quantitative stock selection system works, 
        from initial filtering to final scoring and ranking.
        """)
        
        # Process Flow
        st.subheader("🔄 Selection Process Flow")
        
        process_steps = """
        1. **Data Collection**: Fetch 1 year of historical data for each stock in the universe
        2. **Technical Analysis**: Calculate technical indicators (RSI, MACD, Moving Averages, etc.)
        3. **Fundamental Filtering**: Apply quantitative filters to remove unsuitable stocks
        4. **Scoring**: Calculate composite score (0-100) based on multiple factors
        5. **Ranking**: Sort stocks by score (highest first)
        6. **Signal Generation**: Generate BUY/HOLD signals based on technical analysis
        """
        st.markdown(process_steps)
        
        st.markdown("---")
        
        # Filtering Criteria
        st.subheader("🔍 Filtering Criteria")
        st.markdown("""
        Stocks must pass **all** of the following filters to be considered for selection:
        """)
        
        filter_col1, filter_col2 = st.columns(2)
        
        with filter_col1:
            st.markdown(f"""
            **Price Filters:**
            - Minimum Price: ${config.MIN_PRICE}
            - Maximum Price: ${config.MAX_PRICE}
            
            **Market Filters:**
            - Minimum Market Cap: ${config.MIN_MARKET_CAP/1e9:.0f}B
            - Minimum Daily Volume: {config.MIN_VOLUME:,} shares
            """)
        
        with filter_col2:
            st.markdown(f"""
            **Technical Filters:**
            - RSI Range: {config.MIN_RSI} - {config.MAX_RSI}
            - Minimum Data Points: {config.MIN_DATA_POINTS} days
            - Maximum Volatility: {config.MAX_VOLATILITY*100:.0f}% daily
            - Minimum Volume Ratio: {config.MIN_VOLUME_RATIO}x (vs 20-day average)
            """)
        
        st.markdown("---")
        
        # Scoring Methodology
        st.subheader("📊 Scoring Methodology")
        st.markdown("""
        Each stock receives a composite score from **0 to 100** based on 8 different factors.
        Higher scores indicate better investment opportunities.
        """)
        
        # Create scoring breakdown
        scoring_factors = [
            {
                "Factor": "Momentum (20-day)",
                "Weight": "0-25 points",
                "Description": "Measures price momentum over 20 days. Optimal range: 3-12% gain.",
                "Best Case": "3-12% positive momentum = 25 points"
            },
            {
                "Factor": "RSI (Relative Strength Index)",
                "Weight": "0-20 points",
                "Description": "Measures overbought/oversold conditions. Optimal range: 45-65.",
                "Best Case": "RSI between 45-65 = 20 points"
            },
            {
                "Factor": "Moving Average Trend",
                "Weight": "0-20 points",
                "Description": "Evaluates price position relative to moving averages. Prefers uptrends.",
                "Best Case": "Price > SMA20 > SMA50 (strong uptrend) = 20 points"
            },
            {
                "Factor": "MACD Signal",
                "Weight": "0-15 points",
                "Description": "Measures momentum and trend changes. Prefers bullish crossovers.",
                "Best Case": "MACD > Signal and MACD > 0 = 15 points"
            },
            {
                "Factor": "Volume Confirmation",
                "Weight": "0-12 points",
                "Description": "Confirms price movements with trading volume. Higher volume = stronger signal.",
                "Best Case": "Volume ratio ≥ 1.5x = 12 points"
            },
            {
                "Factor": "Volatility",
                "Weight": "0-8 points",
                "Description": "Measures price stability. Prefers moderate volatility (1.5-2.5% daily).",
                "Best Case": "1.5-2.5% daily volatility = 8 points"
            },
            {
                "Factor": "Momentum Consistency",
                "Weight": "0-8 points",
                "Description": "Checks if momentum is consistent across different time periods.",
                "Best Case": "Consistent positive momentum = 8 points"
            },
            {
                "Factor": "Bollinger Bands Position",
                "Weight": "0-7 points",
                "Description": "Evaluates price position within Bollinger Bands. Prefers middle-upper range.",
                "Best Case": "Price in 30-70% of band range = 7 points"
            }
        ]
        
        scoring_df = pd.DataFrame(scoring_factors)
        st.dataframe(
            scoring_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Factor": st.column_config.TextColumn("Factor", width="medium"),
                "Weight": st.column_config.TextColumn("Max Points", width="small"),
                "Description": st.column_config.TextColumn("Description", width="large"),
                "Best Case": st.column_config.TextColumn("Best Case", width="medium")
            }
        )
        
        st.markdown("---")
        
        # Visual Score Breakdown
        st.subheader("📈 Score Breakdown Example")
        
        example_col1, example_col2 = st.columns(2)
        
        with example_col1:
            st.markdown("""
            **Example: High-Scoring Stock (Score: 95/100)**
            
            - Momentum: 25/25 (8% gain over 20 days)
            - RSI: 20/20 (RSI = 55)
            - MA Trend: 20/20 (Strong uptrend)
            - MACD: 15/15 (Bullish crossover)
            - Volume: 12/12 (High volume)
            - Volatility: 8/8 (Optimal range)
            - Consistency: 8/8 (Consistent momentum)
            - BB Position: 7/7 (Good position)
            """)
        
        with example_col2:
            st.markdown("""
            **Example: Low-Scoring Stock (Score: 35/100)**
            
            - Momentum: 6/25 (Weak momentum)
            - RSI: 10/20 (RSI = 35, oversold)
            - MA Trend: 4/20 (Price below MAs)
            - MACD: 5/15 (Weak signal)
            - Volume: 4/12 (Below average)
            - Volatility: 3/8 (High volatility)
            - Consistency: 0/8 (Inconsistent)
            - BB Position: 3/7 (Lower band)
            """)
        
        st.markdown("---")
        
        # BUY Signal Generation
        st.subheader("✅ BUY Signal Generation")
        st.markdown("""
        After scoring, stocks are evaluated for BUY signals based on multiple technical conditions:
        
        **A stock receives a BUY signal if it meets at least 3 of the following criteria:**
        
        1. **RSI Condition**: RSI between 30-50 (oversold to neutral) - indicates potential bounce
        2. **Moving Average Trend**: Price above 20-day MA (preferably above 50-day MA too)
        3. **MACD Crossover**: MACD line above signal line (bullish momentum)
        4. **Positive Momentum**: 20-day momentum is positive
        5. **Volume Confirmation**: Volume ratio ≥ 1.0x (above average trading activity)
        
        Stocks that meet these criteria are flagged as **BUY** recommendations.
        """)
        
        st.markdown("---")
        
        # Strategy Presets
        st.subheader("📋 Strategy Presets Explained")
        st.markdown("""
        The app includes several pre-configured strategy presets that adjust filtering criteria:
        """)
        
        strategy_info = pd.DataFrame([
            {
                "Strategy": "Conservative",
                "Market Cap": "≥ $50B",
                "Volatility": "≤ 3%",
                "Volume Ratio": "≥ 0.8x",
                "Best For": "Risk-averse investors seeking stability"
            },
            {
                "Strategy": "Aggressive",
                "Market Cap": "≥ $5B",
                "Volatility": "≤ 8%",
                "Volume Ratio": "≥ 0.3x",
                "Best For": "Risk-tolerant investors seeking growth"
            },
            {
                "Strategy": "Momentum",
                "Market Cap": "≥ $10B",
                "Volatility": "≤ 6%",
                "Volume Ratio": "≥ 1.0x",
                "Best For": "Trend-following traders"
            },
            {
                "Strategy": "Value",
                "Market Cap": "≥ $20B",
                "Volatility": "≤ 4%",
                "Volume Ratio": "≥ 0.5x",
                "Best For": "Value investors seeking undervalued stocks"
            },
            {
                "Strategy": "Dividend Focus",
                "Market Cap": "≥ $30B",
                "Volatility": "≤ 3.5%",
                "Volume Ratio": "≥ 0.6x",
                "Best For": "Income-focused investors"
            }
        ])
        
        st.dataframe(strategy_info, use_container_width=True, hide_index=True)
        
        st.markdown("""
        You can also create **custom filters** by enabling "Use custom filters" in the sidebar.
        This allows you to fine-tune every parameter to match your specific investment criteria.
        """)
        
        # Data Sources
        st.subheader("📡 Data Sources")
        st.markdown(f"""
        - **Data Provider**: Yahoo Finance (via yfinance library)
        - **Lookback Period**: {config.LOOKBACK_PERIOD_DAYS} trading days (1 year)
        - **Update Frequency**: Every {config.UPDATE_INTERVAL_HOURS} hour(s)
        - **Stock Universe**: {len(config.STOCK_UNIVERSE)} stocks (configurable in config.py)
        
        All data is fetched in real-time and cached to minimize API calls.
        """)
        
        st.markdown("---")
        
        # Important Notes
        st.subheader("⚠️ Important Notes")
        st.warning("""
        - This is a **quantitative analysis tool** for stock selection, not financial advice
        - Past performance does not guarantee future results
        - Always conduct your own research before making investment decisions
        - Market conditions change rapidly - regularly review and adjust parameters
        - Consider multiple factors beyond technical analysis (fundamentals, news, etc.)
        - Use proper risk management and never invest more than you can afford to lose
        """)
        
        # Configuration Info
        with st.expander("🔧 View Current Configuration"):
            st.code(f"""
# Current Filter Settings
MIN_MARKET_CAP = ${config.MIN_MARKET_CAP:,}
MIN_VOLUME = {config.MIN_VOLUME:,}
MIN_PRICE = ${config.MIN_PRICE}
MAX_PRICE = ${config.MAX_PRICE}
MIN_RSI = {config.MIN_RSI}
MAX_RSI = {config.MAX_RSI}
MIN_DATA_POINTS = {config.MIN_DATA_POINTS}
MAX_VOLATILITY = {config.MAX_VOLATILITY*100}%
MIN_VOLUME_RATIO = {config.MIN_VOLUME_RATIO}x

# Stock Universe Size
TOTAL_STOCKS = {len(config.STOCK_UNIVERSE)}
            """, language="python")
    
    # Enhanced Footer
    st.markdown("---")
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    
    with footer_col1:
        st.markdown(
            f"<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
            f"🕒 Last updated:<br>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            f"</div>",
            unsafe_allow_html=True
        )
    
    with footer_col2:
        st.markdown(
            "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
            "📡 Data source:<br>Yahoo Finance (yfinance)"
            "</div>",
            unsafe_allow_html=True
        )
    
    with footer_col3:
        st.markdown(
            "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
            "⚠️ Not financial advice<br>Do your own research"
            "</div>",
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()

