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
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import DataFetcher
from stock_selector import StockSelector
from trading_strategy import TradingStrategy
from ai_insights import AIInsights
from database import Database
from auth import AuthManager
from legal_pages import get_terms_of_service, get_privacy_policy
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

# Enhanced CSS for modern, professional styling with animations and improved UX
st.markdown("""
    <style>
    /* Main Header with animation */
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
        animation: fadeInDown 0.8s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Metric Cards with hover effects */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    
    /* Enhanced Buttons with better animations */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.5);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Sidebar enhancements */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Enhanced Dataframe styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s ease-out;
    }
    
    .dataframe thead {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .dataframe tbody tr {
        transition: background-color 0.2s ease;
    }
    
    .dataframe tbody tr:hover {
        background-color: #f0f4ff;
    }
    
    /* Enhanced Tabs with better styling and scrollability */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 0.75rem;
        border-radius: 12px;
        display: flex;
        overflow-x: auto;
        overflow-y: hidden;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: thin;
        scrollbar-color: #667eea #f8f9fa;
        position: relative;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid #e5e7eb;
    }
    
    /* Add fade effect at edges to indicate scrollability */
    .stTabs [data-baseweb="tab-list"]::before,
    .stTabs [data-baseweb="tab-list"]::after {
        content: '';
        position: absolute;
        top: 0;
        bottom: 0;
        width: 30px;
        pointer-events: none;
        z-index: 1;
    }
    
    .stTabs [data-baseweb="tab-list"]::before {
        left: 0;
        background: linear-gradient(to right, rgba(248, 249, 250, 1), rgba(248, 249, 250, 0));
    }
    
    .stTabs [data-baseweb="tab-list"]::after {
        right: 0;
        background: linear-gradient(to left, rgba(248, 249, 250, 1), rgba(248, 249, 250, 0));
    }
    
    /* Custom scrollbar for tabs */
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        height: 8px;
    }
    
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
        margin: 0 10px;
    }
    
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
        transition: background 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 12px 18px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid transparent;
        white-space: nowrap;
        min-width: fit-content;
        display: flex;
        align-items: center;
        gap: 6px;
        background: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(102, 126, 234, 0.08);
        border-color: rgba(102, 126, 234, 0.2);
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(102, 126, 234, 0.2);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-color: #667eea;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"]:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Tab icon alignment */
    .stTabs [data-baseweb="tab"] > div {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Enhanced Success/Info/Warning boxes */
    .stSuccess {
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 1rem;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
        animation: slideIn 0.4s ease-out;
    }
    
    .stInfo {
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.05) 100%);
        animation: slideIn 0.4s ease-out;
    }
    
    .stWarning {
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.05) 100%);
        animation: slideIn 0.4s ease-out;
    }
    
    .stError {
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 1rem;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
        animation: slideIn 0.4s ease-out;
    }
    
    /* Enhanced Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #667eea;
        transition: color 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        color: #764ba2;
    }
    
    /* Hide Streamlit branding but keep sidebar toggle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Keep header visible for sidebar toggle button */
    /* header {visibility: hidden;} */
    
    /* Make sidebar toggle button more visible and prominent */
    button[kind="header"] {
        background-color: #667eea !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3) !important;
    }
    
    button[kind="header"]:hover {
        background-color: #764ba2 !important;
        transform: scale(1.1);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Ensure sidebar is visible and styled */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Make the header visible so sidebar toggle is accessible */
    header[data-testid="stHeader"] {
        visibility: visible !important;
        background-color: white;
        border-bottom: 1px solid #e0e0e0;
    }
    
    /* Style the sidebar content area */
    .css-1d391kg {
        background-color: #f8f9fa;
        padding: 1rem;
    }
    
    /* Enhanced Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 5px;
        transition: background 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Enhanced Score badges with animations */
    .score-high {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
        animation: fadeIn 0.5s ease-out;
    }
    
    .score-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(245, 158, 11, 0.3);
        animation: fadeIn 0.5s ease-out;
    }
    
    .score-low {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Loading spinner enhancement */
    .stSpinner > div {
        border-top-color: #667eea !important;
        border-right-color: #667eea !important;
    }
    
    /* Metric value animations */
    [data-testid="stMetricValue"] {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Selectbox and input enhancements */
    .stSelectbox > div > div {
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    
    /* Slider enhancements */
    .stSlider > div > div {
        border-radius: 8px;
    }
    
    /* Empty state styling */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #666;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    
    /* Card hover effects */
    .stock-card {
        transition: all 0.3s ease;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .stock-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    
    /* Progress bar enhancements */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    /* Tooltip enhancements */
    [data-testid="stTooltip"] {
        font-size: 0.85rem;
    }
    
    /* Badge/Tag responsive styling - wraps on smaller screens */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .badge-item {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        white-space: nowrap;
        margin: 0.2rem 0.2rem 0.2rem 0;
        line-height: 1.4;
    }
    
    /* Responsive improvements for mobile and tablets */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
            padding: 0.5rem 0;
        }
        
        /* Make tabs scrollable on mobile - already handled in main CSS */
        .stTabs [data-baseweb="tab"] {
            padding: 10px 14px;
            font-size: 0.85rem;
            white-space: nowrap;
            min-width: fit-content;
        }
        
        /* Quick filter buttons on mobile */
        .stButton > button {
            min-height: 60px;
            font-size: 0.8rem;
            padding: 0.6rem 0.4rem;
        }
        
        /* Improve button sizes for touch */
        .stButton>button {
            padding: 0.9rem 1.2rem;
            font-size: 0.95rem;
            min-height: 44px; /* Minimum touch target size */
        }
        
        /* Make quick filter buttons stack on mobile */
        .quick-filter-container {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        /* Badge wrapping on mobile */
        .badge-container {
            gap: 0.4rem;
        }
        
        .badge-item {
            font-size: 0.7rem;
            padding: 0.3rem 0.5rem;
            margin: 0.15rem;
        }
        
        /* Improve metric cards on mobile */
        .metric-card {
            padding: 1rem;
            margin: 0.3rem 0;
        }
        
        /* Better spacing for columns on mobile */
        [data-testid="column"] {
            padding: 0.5rem;
        }
        
        /* Improve expander headers on mobile */
        .streamlit-expanderHeader {
            font-size: 0.9rem;
            padding: 0.75rem;
        }
        
        /* Make copy buttons more accessible */
        .copy-button {
            min-width: 60px;
            min-height: 36px;
            padding: 0.5rem 0.75rem;
            font-size: 0.85rem;
        }
        
        /* Improve sidebar on mobile */
        section[data-testid="stSidebar"] {
            padding: 0.5rem;
        }
        
        /* Better table display on mobile */
        .dataframe {
            font-size: 0.85rem;
        }
        
        /* Improve empty state on mobile */
        .empty-state {
            padding: 2rem 1rem;
        }
        
        .empty-state-icon {
            font-size: 3rem;
        }
    }
    
    /* Extra small screens (phones in portrait) */
    @media (max-width: 480px) {
        .main-header {
            font-size: 1.75rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 6px 10px;
            font-size: 0.8rem;
        }
        
        .badge-item {
            font-size: 0.65rem;
            padding: 0.25rem 0.4rem;
        }
        
        /* Stack columns on very small screens */
        [data-testid="column"] {
            width: 100% !important;
            margin-bottom: 1rem;
        }
    }
    
    /* Improve touch targets for all interactive elements */
    button, .stButton>button, [role="button"] {
        min-height: 44px;
        min-width: 44px;
    }
    
    /* Better spacing for form elements */
    .stSelectbox, .stTextInput, .stSlider {
        margin-bottom: 1rem;
    }
    
    /* Improve readability on all screen sizes */
    body {
        font-size: 16px; /* Prevent zoom on iOS */
    }
    
    input, select, textarea {
        font-size: 16px !important; /* Prevent zoom on iOS */
    }
    
    /* Smooth transitions for all interactive elements */
    * {
        transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data(ttl=86400)  # Cache for 24 hours (strategy presets don't change)
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


def calculate_adaptive_min_data_points(period: str, interval: str) -> int:
    """
    Calculate adaptive minimum data points based on period and interval.
    This ensures we don't filter out stocks unnecessarily when using shorter periods.
    
    Args:
        period: Time period ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
        interval: Data interval ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo")
    
    Returns:
        Adaptive minimum data points required
    """
    # Estimate expected data points based on period and interval
    # Trading days per year: ~252
    # Trading hours per day: ~6.5 (9:30 AM - 4:00 PM EST)
    
    period_days_map = {
        "1d": 1,
        "5d": 5,
        "1mo": 21,  # ~21 trading days per month
        "3mo": 63,  # ~63 trading days per quarter
        "6mo": 126,  # ~126 trading days per 6 months
        "1y": 252,  # ~252 trading days per year
        "2y": 504,
        "5y": 1260,
        "10y": 2520,
        "ytd": 252,  # Approximate, varies by date
        "max": 10000  # Very large number for max
    }
    
    # Get approximate trading days for the period
    trading_days = period_days_map.get(period, 252)
    
    # Calculate expected data points based on interval
    if interval in ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"]:
        # Intraday intervals: ~6.5 trading hours per day
        hours_per_day = 6.5
        if interval == "1m":
            points_per_day = hours_per_day * 60
        elif interval == "2m":
            points_per_day = hours_per_day * 30
        elif interval == "5m":
            points_per_day = hours_per_day * 12
        elif interval == "15m":
            points_per_day = hours_per_day * 4
        elif interval == "30m":
            points_per_day = hours_per_day * 2
        elif interval == "60m" or interval == "90m":
            points_per_day = hours_per_day
        elif interval == "1h":
            points_per_day = hours_per_day
        
        expected_points = int(trading_days * points_per_day)
    elif interval == "1d":
        expected_points = trading_days
    elif interval == "5d":
        expected_points = trading_days // 5
    elif interval == "1wk":
        expected_points = trading_days // 5  # ~5 trading days per week
    elif interval == "1mo":
        expected_points = trading_days // 21  # ~21 trading days per month
    elif interval == "3mo":
        expected_points = trading_days // 63  # ~63 trading days per quarter
    else:
        expected_points = trading_days
    
    # Set minimum data points to 80% of expected, but with reasonable bounds
    # Minimum: 20 points (for very short periods)
    # Maximum: 200 points (original default for long periods)
    adaptive_min = max(20, min(int(expected_points * 0.8), 200))
    
    # For intraday intervals, we need at least enough for technical indicators
    # SMA 20 requires 20 points, so ensure minimum is at least 30
    if interval in ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"]:
        adaptive_min = max(30, adaptive_min)
    
    return adaptive_min


@st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour
def get_stock_data(custom_filters=None, period="1y", interval="1d"):
    """
    Fetch and analyze stocks with caching.
    
    Args:
        custom_filters: Custom filter parameters
        period: Time period for data ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
        interval: Data interval ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo")
    """
    data_fetcher = DataFetcher()
    stock_selector = StockSelector(data_fetcher)
    
    # Calculate adaptive minimum data points based on period and interval
    adaptive_min_data_points = calculate_adaptive_min_data_points(period, interval)
    
    # Merge adaptive min_data_points into custom_filters
    if custom_filters is None:
        custom_filters = {}
    
    # Update min_data_points with adaptive value
    custom_filters = custom_filters.copy()  # Don't modify the original
    custom_filters['min_data_points'] = adaptive_min_data_points
    
    # Fetch and analyze stocks with specified time range
    qualified_stocks = stock_selector.filter_stocks(
        config.STOCK_UNIVERSE, 
        custom_filters=custom_filters,
        period=period,
        interval=interval
    )
    
    return qualified_stocks, data_fetcher


@st.cache_data(ttl=3600)  # Cache for 1 hour
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


# Helper functions for new features
def initialize_session_state():
    """Initialize session state variables for watchlist, recent searches, etc."""
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = []
    if 'recent_searches' not in st.session_state:
        st.session_state.recent_searches = []
    if 'last_updated' not in st.session_state:
        st.session_state.last_updated = datetime.now()
    if 'db' not in st.session_state:
        st.session_state.db = Database()
    if 'auth' not in st.session_state:
        st.session_state.auth = AuthManager(st.session_state.db)
    if 'show_new_portfolio' not in st.session_state:
        st.session_state.show_new_portfolio = False
    if 'show_premium' not in st.session_state:
        st.session_state.show_premium = False


def add_to_watchlist(symbol: str):
    """Add a stock symbol to the watchlist."""
    if symbol and symbol not in st.session_state.watchlist:
        st.session_state.watchlist.append(symbol)
        return True
    return False


def remove_from_watchlist(symbol: str):
    """Remove a stock symbol from the watchlist."""
    if symbol in st.session_state.watchlist:
        st.session_state.watchlist.remove(symbol)
        return True
    return False


def add_to_recent_searches(symbol: str):
    """Add a stock symbol to recent searches (max 10)."""
    symbol = symbol.upper().strip()
    if symbol:
        # Remove if already exists
        if symbol in st.session_state.recent_searches:
            st.session_state.recent_searches.remove(symbol)
        # Add to front
        st.session_state.recent_searches.insert(0, symbol)
        # Keep only last 10
        st.session_state.recent_searches = st.session_state.recent_searches[:10]


def get_performance_badges(stock: dict) -> list:
    """Get performance badges for a stock based on its metrics."""
    badges = []
    score = stock.get('score', 0)
    momentum = stock.get('momentum', 0)
    rsi = stock.get('rsi', 50)
    volume_ratio = stock.get('volume_ratio', 0)
    
    if score >= 90:
        badges.append(("🏆", "Top Performer", "#10b981"))
    elif score >= 80:
        badges.append(("⭐", "High Score", "#3b82f6"))
    
    if momentum and momentum > 0.05:
        badges.append(("🚀", "High Momentum", "#f59e0b"))
    
    if rsi and rsi < 30:
        badges.append(("📉", "Oversold", "#ef4444"))
    elif rsi and rsi > 70:
        badges.append(("📈", "Overbought", "#8b5cf6"))
    
    if volume_ratio and volume_ratio > 1.5:
        badges.append(("📊", "High Volume", "#06b6d4"))
    
    if stock.get('buy_signal'):
        badges.append(("✅", "BUY Signal", "#10b981"))
    
    return badges


def format_timestamp(dt: datetime) -> str:
    """Format datetime as a readable timestamp."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def create_copy_button_html(symbol: str, button_id: str) -> str:
    """Create HTML for copy to clipboard button - mobile-friendly."""
    return f"""
    <button onclick="navigator.clipboard.writeText('{symbol}'); this.innerHTML='✓ Copied!'; setTimeout(() => this.innerHTML='📋 Copy', 2000);" 
            class="copy-button"
            style="background: #667eea; color: white; border: none; padding: 0.5rem 0.75rem; border-radius: 6px; cursor: pointer; font-size: 0.85rem; margin: 0.25rem; min-width: 60px; min-height: 36px; transition: all 0.2s ease; box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);"
            onmouseover="this.style.background='#764ba2'; this.style.transform='scale(1.05)'"
            onmouseout="this.style.background='#667eea'; this.style.transform='scale(1)'">
        📋 Copy
    </button>
    """


def create_price_chart(stock_data, symbol, chart_type='candlestick'):
    """
    Create interactive price chart with technical indicators.
    
    Args:
        stock_data: Stock data dictionary
        symbol: Stock symbol
        chart_type: 'candlestick' or 'line' - type of price chart to display
    """
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
    
    # Price chart - Candlestick or Line
    if chart_type == 'candlestick' and all(col in data.columns for col in ['Open', 'High', 'Low', 'Close']):
        # Add candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price',
                increasing_line_color='#10b981',  # Green for up candles
                decreasing_line_color='#ef4444',   # Red for down candles
                increasing_fillcolor='#10b981',
                decreasing_fillcolor='#ef4444',
                line=dict(width=1),
                hovertemplate='<b>%{x}</b><br>' +
                             'Open: $%{open:.2f}<br>' +
                             'High: $%{high:.2f}<br>' +
                             'Low: $%{low:.2f}<br>' +
                             'Close: $%{close:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
    else:
        # Fallback to line chart if candlestick data not available or chart_type is 'line'
        fig.add_trace(
            go.Scatter(
                x=data.index, 
                y=data['Close'], 
                name='Price', 
                line=dict(color='#667eea', width=2.5),
                hovertemplate='<b>Price</b><br>$%{y:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
    
    if 'SMA_20' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index, 
                y=data['SMA_20'], 
                name='SMA 20', 
                line=dict(color='#f59e0b', dash='dash', width=2),
                hovertemplate='<b>SMA 20</b><br>$%{y:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
    
    if 'SMA_50' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index, 
                y=data['SMA_50'], 
                name='SMA 50', 
                line=dict(color='#ef4444', dash='dash', width=2),
                hovertemplate='<b>SMA 50</b><br>$%{y:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
    
    # RSI with enhanced styling
    if 'RSI' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index, 
                y=data['RSI'], 
                name='RSI', 
                line=dict(color='#764ba2', width=2),
                fill='tozeroy',
                fillcolor='rgba(118, 75, 162, 0.1)',
                hovertemplate='<b>RSI</b><br>%{y:.1f}<extra></extra>'
            ),
            row=2, col=1
        )
        # Add RSI levels with better styling
        fig.add_hline(
            y=70, 
            line_dash="dash", 
            line_color="#ef4444", 
            line_width=2,
            row=2, 
            col=1, 
            annotation_text="Overbought (70)",
            annotation_position="right"
        )
        fig.add_hline(
            y=30, 
            line_dash="dash", 
            line_color="#10b981", 
            line_width=2,
            row=2, 
            col=1, 
            annotation_text="Oversold (30)",
            annotation_position="right"
        )
        # Add neutral zone
        fig.add_hrect(
            y0=30, y1=70, 
            fillcolor="rgba(16, 185, 129, 0.05)", 
            layer="below", 
            line_width=0,
            row=2, col=1
        )
    
    # MACD with enhanced styling
    if 'MACD' in data.columns and 'MACD_Signal' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index, 
                y=data['MACD'], 
                name='MACD', 
                line=dict(color='#3b82f6', width=2),
                hovertemplate='<b>MACD</b><br>%{y:.3f}<extra></extra>'
            ),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=data.index, 
                y=data['MACD_Signal'], 
                name='Signal', 
                line=dict(color='#ef4444', width=2, dash='dash'),
                hovertemplate='<b>Signal</b><br>%{y:.3f}<extra></extra>'
            ),
            row=3, col=1
        )
        # MACD Histogram with better colors
        if 'MACD_Histogram' in data.columns:
            colors = ['#10b981' if x >= 0 else '#ef4444' for x in data['MACD_Histogram']]
            fig.add_trace(
                go.Bar(
                    x=data.index, 
                    y=data['MACD_Histogram'], 
                    name='Histogram', 
                    marker_color=colors,
                    hovertemplate='<b>Histogram</b><br>%{y:.3f}<extra></extra>'
                ),
                row=3, col=1
            )
    
    # Enhanced chart styling with modern design
    fig.update_layout(
        height=800,
        title={
            'text': f"<b>{symbol}</b> - Technical Analysis",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22, 'color': '#667eea', 'family': 'Arial, sans-serif'}
        },
        showlegend=True,
        hovermode='x unified',
        template='plotly_white',
        plot_bgcolor='rgba(248, 249, 250, 0.5)',
        paper_bgcolor='rgba(255, 255, 255, 0.9)',
        font=dict(family="Arial, sans-serif", size=12, color='#333'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='rgba(0, 0, 0, 0.1)',
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor='rgba(255, 255, 255, 0.95)',
            bordercolor='#667eea',
            font_size=12,
            font_family="Arial, sans-serif"
        )
    )
    
    # Update axes styling with better grid
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(0,0,0,0.08)',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='rgba(0,0,0,0.1)',
        rangeslider=dict(visible=False)  # Hide range slider for cleaner look
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(0,0,0,0.08)',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='rgba(0,0,0,0.1)'
    )
    
    # For candlestick charts, update the first subplot y-axis title
    if chart_type == 'candlestick' and all(col in data.columns for col in ['Open', 'High', 'Low', 'Close']):
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    
    return fig


def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
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
    
    # Premium Plans Modal (if triggered)
    if st.session_state.get('show_premium', False):
        with st.container():
            st.markdown("### 💎 Premium Plans")
            st.markdown("Upgrade your account to unlock advanced features!")
            
            plan_col1, plan_col2, plan_col3 = st.columns(3)
            
            with plan_col1:
                st.markdown("""
                #### 🆓 Free
                **$0/month**
                
                ✅ Basic stock analysis
                ✅ Limited stock universe (37 stocks)
                ✅ Portfolio tracking
                ✅ Watchlists
                ✅ CSV export
                ✅ Recommendation history
                """)
                if not auth.is_authenticated():
                    st.info("Current Plan")
            
            with plan_col2:
                st.markdown("""
                #### ⭐ Pro
                **$9.99/month**
                
                ✅ Everything in Free
                ✅ Unlimited stock universe
                ✅ Real-time data updates
                ✅ Email alerts
                ✅ Advanced analytics
                ✅ Priority support
                ✅ Backtesting (coming soon)
                """)
                if auth.is_authenticated() and user_tier == 'FREE':
                    if st.button("Upgrade to Pro", key="upgrade_pro", use_container_width=True, type="primary"):
                        st.info("💡 Payment integration coming soon! Contact us for early access.")
                elif not auth.is_authenticated():
                    st.warning("Login required")
            
            with plan_col3:
                st.markdown("""
                #### 💎 Premium
                **$29.99/month**
                
                ✅ Everything in Pro
                ✅ Backtesting engine
                ✅ API access
                ✅ Mobile app
                ✅ Advanced ML models
                ✅ Custom strategies
                ✅ White-label options
                """)
                if auth.is_authenticated() and user_tier == 'FREE':
                    if st.button("Upgrade to Premium", key="upgrade_premium", use_container_width=True, type="primary"):
                        st.info("💡 Payment integration coming soon! Contact us for early access.")
                elif not auth.is_authenticated():
                    st.warning("Login required")
            
            st.markdown("---")
            if st.button("Close", use_container_width=True):
                st.session_state.show_premium = False
                st.rerun()
            
            st.markdown("---")
    
    # Sidebar for controls with enhanced organization
    with st.sidebar:
        # Authentication Section
        auth = st.session_state.auth
        if auth.is_authenticated():
            user = auth.get_current_user()
            user_tier = user.get('subscription_tier', 'free').upper()
            tier_colors = {
                'FREE': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'PRO': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                'PREMIUM': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
            }
            tier_color = tier_colors.get(user_tier, tier_colors['FREE'])
            
            st.markdown(f"""
            <div style="background: {tier_color}; 
                        padding: 1rem; border-radius: 8px; margin-bottom: 1rem; color: white;">
                <p style="margin: 0; font-weight: 600;">👤 {user['username']}</p>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.85rem; opacity: 0.9;">
                    {user_tier} Plan
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show upgrade button if on free plan
            if user_tier == 'FREE':
                if st.button("⭐ Upgrade to Premium", use_container_width=True, type="primary"):
                    st.session_state.show_premium = True
                    st.rerun()
            
            if st.button("🚪 Logout", use_container_width=True):
                auth.logout()
        else:
            st.markdown("### 🔐 Account")
            login_tab, register_tab = st.tabs(["Login", "Register"])
            
            with login_tab:
                with st.form("login_form"):
                    login_username = st.text_input("Username or Email", key="login_username")
                    login_password = st.text_input("Password", type="password", key="login_password")
                    login_submit = st.form_submit_button("Login", use_container_width=True)
                    
                    if login_submit:
                        success, message = auth.login(login_username, login_password)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
            
            with register_tab:
                with st.form("register_form"):
                    reg_username = st.text_input("Username", key="reg_username")
                    reg_email = st.text_input("Email", key="reg_email")
                    reg_password = st.text_input("Password", type="password", key="reg_password")
                    reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
                    reg_submit = st.form_submit_button("Register", use_container_width=True)
                    
                    if reg_submit:
                        success, message = auth.register(reg_username, reg_email, reg_password, reg_confirm)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
            
            # Show premium plans info for non-authenticated users
            with st.expander("💎 View Premium Plans", expanded=False):
                st.markdown("### 🚀 Subscription Plans")
                
                plan_col1, plan_col2, plan_col3 = st.columns(3)
                
                with plan_col1:
                    st.markdown("""
                    #### 🆓 Free
                    **$0/month**
                    
                    ✅ Basic stock analysis
                    ✅ Limited stock universe (37 stocks)
                    ✅ Portfolio tracking
                    ✅ Watchlists
                    ✅ CSV export
                    """)
                
                with plan_col2:
                    st.markdown("""
                    #### ⭐ Pro
                    **$9.99/month**
                    
                    ✅ Everything in Free
                    ✅ Unlimited stock universe
                    ✅ Real-time data updates
                    ✅ Email alerts
                    ✅ Advanced analytics
                    ✅ Priority support
                    """)
                
                with plan_col3:
                    st.markdown("""
                    #### 💎 Premium
                    **$29.99/month**
                    
                    ✅ Everything in Pro
                    ✅ Backtesting engine
                    ✅ API access
                    ✅ Mobile app
                    ✅ Advanced ML models
                    ✅ Custom strategies
                    """)
                
                st.info("💡 **Premium plans coming soon!** Sign up now to get early access and special pricing.")
            
            st.markdown("---")
        
        # Header with branding
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0; border-bottom: 2px solid #667eea; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #667eea; font-size: 1.5rem;">⚙️ Settings</h2>
            <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.85rem;">Configure your analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Strategy Presets with better organization
        st.markdown("### 📋 Strategy Presets")
        strategy_presets = get_strategy_presets()
        selected_strategy = st.selectbox(
            "Select a strategy preset",
            options=list(strategy_presets.keys()),
            index=0,
            help="Choose a pre-configured strategy. Each strategy has optimized filter settings for different investment styles.",
            key="strategy_select"
        )
        
        # Show strategy description immediately
        strategy_descriptions = {
            "Default": "Balanced approach with standard filter settings suitable for most investors.",
            "Conservative": "Focus on large-cap, low-volatility stocks. Lower risk, stable returns.",
            "Aggressive": "Includes smaller companies and higher volatility. Higher risk, potential for higher returns.",
            "Momentum": "Emphasizes stocks with strong price momentum and high volume. Trend-following strategy.",
            "Value": "Targets established companies at reasonable prices. Value investing approach.",
            "Dividend Focus": "Prioritizes large, stable companies suitable for income investing."
        }
        if selected_strategy in strategy_descriptions:
            st.caption(f"💡 {strategy_descriptions[selected_strategy]}")
        
        st.markdown("---")
        
        # Time Range Settings
        st.markdown("### ⏱️ Time Range Settings")
        
        # Period selector (time range)
        period_options = {
            "1 Month": "1mo",
            "3 Months": "3mo",
            "6 Months": "6mo",
            "1 Year": "1y",
            "2 Years": "2y",
            "5 Years": "5y",
            "10 Years": "10y",
            "Year to Date": "ytd",
            "Maximum Available": "max"
        }
        
        selected_period_label = st.selectbox(
            "Time Period",
            options=list(period_options.keys()),
            index=3,  # Default to "1 Year"
            help="Select the historical time period for analysis. Longer periods provide more data but may include outdated trends."
        )
        selected_period = period_options[selected_period_label]
        
        # Interval selector (data frequency)
        # Note: Intraday intervals (1m-1h) are only available for periods up to 60 days
        interval_options = {
            "1 Minute": "1m",
            "2 Minutes": "2m",
            "5 Minutes": "5m",
            "15 Minutes": "15m",
            "30 Minutes": "30m",
            "60 Minutes": "60m",
            "90 Minutes": "90m",
            "Hourly": "1h",
            "Daily": "1d",
            "Weekly": "1wk",
            "Monthly": "1mo",
            "Quarterly": "3mo"
        }
        
        selected_interval_label = st.selectbox(
            "Data Interval",
            options=list(interval_options.keys()),
            index=8,  # Default to "Daily"
            help="Select the data frequency. Intraday intervals (1m-1h) are only available for periods up to 60 days. Daily provides most detail for longer periods."
        )
        selected_interval = interval_options[selected_interval_label]
        
        # Validate period/interval combination
        intraday_intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"]
        long_periods = ["6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
        
        if selected_interval in intraday_intervals and selected_period in long_periods:
            st.warning(f"⚠️ **Note:** {selected_interval_label} data is typically only available for periods up to 60 days. Consider using '1 Month' or '3 Months' period, or switch to Daily/Weekly intervals for longer periods.")
        
        st.caption(f"📊 Analyzing data: {selected_period_label} period with {selected_interval_label.lower()} intervals")
        
        st.markdown("---")
        
        use_custom = st.checkbox(
            "🔧 Use custom filters", 
            value=False, 
            help="Enable to manually adjust filter criteria. This allows fine-tuning of all parameters."
        )
        
        # Custom Filter Settings (shown when custom is enabled)
        if use_custom or selected_strategy == "Default":
            st.markdown("### 🔧 Custom Filter Settings")
            st.caption("Adjust these parameters to fine-tune your stock selection criteria.")
            
            with st.expander("Market Filters", expanded=False, icon="📊"):
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
            
            with st.expander("Price Filters", expanded=False, icon="💰"):
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
            
            with st.expander("Technical Filters", expanded=False, icon="📈"):
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
        
        st.markdown("---")
        
        # Chart Display Options
        st.markdown("### 📈 Chart Display Options")
        chart_type = st.radio(
            "Price Chart Type",
            options=["Candlestick", "Line"],
            index=0,  # Default to Candlestick
            help="Choose between candlestick chart (shows OHLC) or line chart (closing prices only). Candlestick provides more detail about price action.",
            horizontal=True
        )
        chart_type_lower = chart_type.lower()
        
        st.markdown("---")
        
        # Analysis options with better labels
        st.markdown("### 📊 Analysis Options")
        top_n = st.slider(
            "Number of stocks to display", 
            10, 50, 20,
            help="Maximum number of stocks to show in the results. Lower values show only top performers."
        )
        min_score = st.slider(
            "Minimum score filter", 
            0, 100, 0,
            help="Only show stocks with scores above this threshold. Higher values filter for better opportunities."
        )
        
        st.markdown("---")
        
        # Filter options
        st.markdown("### 🔍 Display Filters")
        sectors = st.multiselect(
            "Filter by Sector",
            options=["Technology", "Healthcare", "Financial Services", "Consumer Cyclical", 
                    "Communication Services", "Energy", "Consumer Defensive"],
            default=[]
        )
        
        show_buy_signals_only = st.checkbox(
            "✅ Show BUY signals only", 
            value=False,
            help="Filter results to show only stocks with active BUY signals based on technical analysis."
        )
        
        st.markdown("---")
        
        # Prepare custom filters
        # Note: min_data_points will be calculated adaptively based on period and interval
        if use_custom or selected_strategy == "Default":
            custom_filters = {
                'min_market_cap': min_market_cap * 1e9,
                'min_volume': int(min_volume),
                'min_price': min_price,
                'max_price': max_price,
                'min_rsi': min_rsi,
                'max_rsi': max_rsi,
                'min_volume_ratio': min_volume_ratio,
                # min_data_points will be set adaptively in get_stock_data()
                'max_volatility': max_volatility / 100
            }
        else:
            custom_filters = strategy_presets[selected_strategy].copy()
            # Remove min_data_points from strategy preset so adaptive calculation applies
            if 'min_data_points' in custom_filters:
                del custom_filters['min_data_points']
        
        # Refresh button with better styling
        st.markdown("---")
        refresh_data = st.button(
            "🔄 Refresh Analysis", 
            type="primary",
            use_container_width=True,
            help="Clear cache and re-analyze all stocks with current filter settings. This may take a minute."
        )
        
        # Cache status indicator
        st.caption("💾 Data is cached for 1 hour to improve performance. Click refresh to get latest data.")
        
        if refresh_data:
            st.cache_data.clear()
            st.session_state.last_updated = datetime.now()
            st.rerun()
        
        # Watchlist section
        st.markdown("---")
        st.markdown("### ⭐ Watchlist")
        watchlist_col1, watchlist_col2 = st.columns([3, 1])
        with watchlist_col1:
            watchlist_input = st.text_input(
                "Add to watchlist",
                placeholder="e.g., AAPL",
                key="watchlist_input",
                label_visibility="collapsed"
            ).upper().strip()
        with watchlist_col2:
            if st.button("➕", key="add_watchlist", help="Add symbol to watchlist"):
                if watchlist_input:
                    if add_to_watchlist(watchlist_input):
                        st.success(f"Added {watchlist_input} to watchlist")
                    else:
                        st.info(f"{watchlist_input} is already in watchlist")
        
        # Display watchlist
        if st.session_state.watchlist:
            st.markdown("**Your Watchlist:**")
            for symbol in st.session_state.watchlist:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(symbol)
                with col2:
                    if st.button("🗑️", key=f"remove_{symbol}", help=f"Remove {symbol}"):
                        remove_from_watchlist(symbol)
                        st.rerun()
        else:
            st.caption("No stocks in watchlist. Add symbols above.")
    
    # Initialize system with enhanced loading state
    # Check if we need to refresh (new filters, period, interval, or strategy)
    needs_refresh = (
        'qualified_stocks' not in st.session_state or 
        refresh_data or 
        'custom_filters' not in st.session_state or 
        st.session_state.get('custom_filters') != custom_filters or
        st.session_state.get('period') != selected_period or
        st.session_state.get('interval') != selected_interval or
        st.session_state.get('selected_strategy') != selected_strategy
    )
    
    if needs_refresh:
        # Calculate adaptive min_data_points for display
        adaptive_min_points = calculate_adaptive_min_data_points(selected_period, selected_interval)
        
        # Show loading state with progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text(f"🔄 Initializing analysis...")
        progress_bar.progress(5)
        
        status_text.text(f"📊 Preparing to analyze {len(config.STOCK_UNIVERSE)} stocks...")
        progress_bar.progress(10)
        
        # Show loading state with better progress tracking
        status_text.text(f"🔄 **Analyzing stocks...** Fetching {selected_period_label.lower()} data with {selected_interval_label.lower()} intervals. This may take a minute.")
        progress_bar.progress(20)
        
        # Fetch data (now with parallel processing for better performance)
        qualified_stocks, data_fetcher = get_stock_data(
            custom_filters=custom_filters,
            period=selected_period,
            interval=selected_interval
        )
        
        progress_bar.progress(90)
        status_text.text(f"✅ Analysis complete! Found {len(qualified_stocks)} qualified stocks.")
        progress_bar.progress(100)
        
        # Clear progress indicators
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
        
        # Show success message with adaptive data points info
        success_msg = st.success(
            f"✅ **Analysis complete!** Found {len(qualified_stocks)} qualified stocks using {selected_period_label.lower()} data. "
            f"(Minimum data points required: {adaptive_min_points})"
        )
        
        st.session_state.qualified_stocks = qualified_stocks
        st.session_state.data_fetcher = data_fetcher
        st.session_state.custom_filters = custom_filters
        st.session_state.selected_strategy = selected_strategy
        st.session_state.period = selected_period
        st.session_state.interval = selected_interval
        st.session_state.chart_type = chart_type_lower
    else:
        qualified_stocks = st.session_state.qualified_stocks
        data_fetcher = st.session_state.data_fetcher
        # Update chart type if changed
        if 'chart_type' not in st.session_state or st.session_state.get('chart_type') != chart_type_lower:
            st.session_state.chart_type = chart_type_lower
    
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
    
    # Quick filter buttons - use session state to track active filter
    if 'active_quick_filter' not in st.session_state:
        st.session_state.active_quick_filter = None
    
    st.markdown("**Quick Filters:**")
    
    # Add CSS for better button alignment
    st.markdown("""
    <style>
    /* Quick filter buttons - improved alignment */
    .stButton > button {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        padding: 0.75rem 0.5rem;
        min-height: 70px;
        line-height: 1.3;
        text-align: center;
    }
    
    /* Ensure emoji and text are properly aligned */
    .stButton > button > div {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.3rem;
    }
    
    /* Icon alignment fix */
    .stButton > button {
        font-size: 0.85rem;
    }
    
    /* Make buttons more visually appealing */
    .stButton > button {
        border: 2px solid #e5e7eb;
        background: white;
        color: #374151;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #f9fafb;
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.15);
    }
    
    /* Active filter button styling */
    .stButton > button:active {
        transform: translateY(0);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Use responsive columns - stack on mobile
    quick_filter_col1, quick_filter_col2, quick_filter_col3, quick_filter_col4, quick_filter_col5 = st.columns([1, 1, 1, 1, 1])
    
    with quick_filter_col1:
        if st.button("🏆\n\nTop 10", use_container_width=True, help="Show only top 10 stocks", key="quick_top10"):
            st.session_state.active_quick_filter = 'top10'
            st.rerun()
    
    with quick_filter_col2:
        if st.button("✅\n\nBUY Only", use_container_width=True, help="Show only stocks with BUY signals", key="quick_buy"):
            st.session_state.active_quick_filter = 'buy'
            st.rerun()
    
    with quick_filter_col3:
        if st.button("⭐\n\nHigh Score\n(≥80)", use_container_width=True, help="Show stocks with score ≥80", key="quick_highscore"):
            st.session_state.active_quick_filter = 'highscore'
            st.rerun()
    
    with quick_filter_col4:
        if st.button("🚀\n\nHigh\nMomentum", use_container_width=True, help="Show stocks with high momentum", key="quick_momentum"):
            st.session_state.active_quick_filter = 'momentum'
            st.rerun()
    
    with quick_filter_col5:
        if st.button("🔄\n\nReset\nFilters", use_container_width=True, help="Reset all filters", key="quick_reset"):
            st.session_state.active_quick_filter = None
            st.rerun()
    
    # Apply quick filter if active
    if st.session_state.active_quick_filter == 'top10':
        filtered_stocks = filtered_stocks[:10]
    elif st.session_state.active_quick_filter == 'buy':
        filtered_stocks = [s for s in filtered_stocks if s.get('buy_signal', False)]
    elif st.session_state.active_quick_filter == 'highscore':
        filtered_stocks = [s for s in filtered_stocks if s['score'] >= 80]
    elif st.session_state.active_quick_filter == 'momentum':
        filtered_stocks = [s for s in filtered_stocks if s.get('momentum', 0) > 0.03]
    
    # Last updated timestamp
    last_updated_time = st.session_state.get('last_updated', datetime.now())
    st.caption(f"📅 Last updated: {format_timestamp(last_updated_time)}")
    
    st.markdown("---")
    
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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "📊 Stock Rankings", 
        "📈 Top Recommendations", 
        "🔍 Stock Details", 
        "🔎 Stock Search",
        "⚖️ Compare Stocks",
        "🤖 AI Insights",
        "💼 My Portfolio",
        "📚 How It Works",
        "⚖️ Legal"
    ])
    
    with tab1:
        st.markdown("### 📊 Stock Rankings")
        st.markdown("Ranked by quantitative score (0-100). Higher scores indicate better opportunities.")
        
        if not filtered_stocks:
            # Enhanced empty state
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📊</div>
                <h3>No stocks match your current filters</h3>
                <p>Try adjusting your criteria to see more results:</p>
                <ul style="text-align: left; display: inline-block;">
                    <li>Lower the minimum score filter</li>
                    <li>Select different sectors</li>
                    <li>Try a different strategy preset</li>
                    <li>Adjust custom filter settings</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            st.info("💡 **Tip:** Start with the 'Default' strategy and gradually adjust filters to find your preferred stocks.")
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
                
                # Get badges for this stock
                badges = get_performance_badges(stock)
                badge_display = " ".join([badge[0] for badge in badges]) if badges else ""
                
                with st.expander(
                    f"{badge_color} **#{i}. {stock['symbol']}** {badge_display} - Score: **{stock['score']:.1f}/100** | "
                    f"Price: ${stock['current_price']:.2f} | Sector: {stock['sector']}",
                    expanded=(i <= 3)  # Expand first 3 by default
                ):
                    # Copy button and badges
                    col_copy, col_badges = st.columns([1, 4])
                    with col_copy:
                        st.markdown(create_copy_button_html(stock['symbol'], f"copy_buy_{i}"), unsafe_allow_html=True)
                    with col_badges:
                        if badges:
                            badge_html = '<div class="badge-container">' + "".join([f'<span class="badge-item" style="background: {badge[2]}; color: white;">{badge[0]} {badge[1]}</span>' for badge in badges]) + '</div>'
                            st.markdown(badge_html, unsafe_allow_html=True)
                    
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
                    
                    # Initialize AI insights
                    ai = AIInsights()
                    
                    # Suggested Buy Price
                    st.markdown("#### 💰 Suggested Buy Price")
                    buy_price_info = ai.calculate_suggested_buy_price(
                        stock, 
                        strategy=selected_strategy,
                        period=selected_period
                    )
                    
                    price_col1, price_col2, price_col3 = st.columns(3)
                    with price_col1:
                        st.metric(
                            "Suggested Price",
                            f"${buy_price_info['suggested_price']:.2f}",
                            delta=f"{buy_price_info['discount_pct']:.1f}% vs current" if buy_price_info['discount_pct'] > 0 else None
                        )
                    with price_col2:
                        st.metric("Price Range Low", f"${buy_price_info['price_range_low']:.2f}")
                    with price_col3:
                        st.metric("Price Range High", f"${buy_price_info['price_range_high']:.2f}")
                    
                    st.caption(f"💡 **Reasoning**: {buy_price_info['reasoning']}")
                    st.info(f"**Current Price**: ${buy_price_info['current_price']:.2f} | **Suggested Entry**: ${buy_price_info['suggested_price']:.2f}")
                    
                    # Sell Targets and Hold Time - Prominently Displayed
                    st.markdown("---")
                    st.markdown("#### 🎯 Sell Targets & Hold Strategy")
                    
                    # Calculate sell targets using suggested buy price as entry
                    sell_targets = ai.calculate_sell_targets(
                        stock, 
                        buy_price_info['suggested_price'],
                        strategy=selected_strategy
                    )
                    
                    # Display hold time prominently
                    hold_col1, hold_col2, hold_col3 = st.columns(3)
                    with hold_col1:
                        st.metric(
                            "📅 Suggested Hold Time",
                            f"{sell_targets['suggested_hold_days']} days",
                            delta=f"~{sell_targets['suggested_hold_months']:.1f} months"
                        )
                    with hold_col2:
                        st.metric(
                            "📊 Strategy",
                            sell_targets['sell_strategy']
                        )
                    with hold_col3:
                        st.metric(
                            "🎯 Target Gain",
                            f"+{sell_targets['potential_gain_pct']:.1f}%",
                            delta=f"${sell_targets['target_sell_price']:.2f}"
                        )
                    
                    # Display sell targets in columns
                    st.markdown("**💰 Sell Price Targets:**")
                    target_col1, target_col2, target_col3, target_col4 = st.columns(4)
                    
                    with target_col1:
                        st.metric(
                            "🎯 Target Price",
                            f"${sell_targets['target_sell_price']:.2f}",
                            delta=f"+{sell_targets['potential_gain_pct']:.1f}%"
                        )
                        st.caption("Primary target")
                    
                    with target_col2:
                        st.metric(
                            "🛡️ Conservative",
                            f"${sell_targets['conservative_target']:.2f}",
                            delta=f"+{sell_targets['conservative_gain_pct']:.1f}%"
                        )
                        st.caption("Take profit early")
                    
                    with target_col3:
                        st.metric(
                            "🚀 Aggressive",
                            f"${sell_targets['aggressive_target']:.2f}",
                            delta=f"+{sell_targets['aggressive_gain_pct']:.1f}%"
                        )
                        st.caption("Hold for more gains")
                    
                    with target_col4:
                        st.metric(
                            "🛑 Stop Loss",
                            f"${sell_targets['stop_loss_price']:.2f}",
                            delta=f"-{sell_targets['stop_loss_pct']:.1f}%"
                        )
                        st.caption("Risk management")
                    
                    # Display reasoning for sell targets
                    st.info(f"💡 **Sell Strategy Reasoning**: {sell_targets['reasoning']}")
                    
                    # Summary box with key information
                    st.markdown("**📋 Position Summary:**")
                    summary_text = f"""
                    - **Entry Price**: ${buy_price_info['suggested_price']:.2f}
                    - **Target Sell**: ${sell_targets['target_sell_price']:.2f} (+{sell_targets['potential_gain_pct']:.1f}%)
                    - **Hold Period**: {sell_targets['suggested_hold_days']} days (~{sell_targets['suggested_hold_months']:.1f} months)
                    - **Stop Loss**: ${sell_targets['stop_loss_price']:.2f} (-{sell_targets['stop_loss_pct']:.1f}%)
                    - **Strategy**: {sell_targets['sell_strategy']}
                    """
                    st.markdown(summary_text)
                    
                    st.markdown("---")
                    
                    # AI Insight for each recommendation
                    st.markdown("#### 🤖 AI Insight")
                    ai_insight = ai.generate_stock_insight(stock)
                    st.markdown(ai_insight)
                    
                    # AI Recommendation
                    recommendation = ai.generate_recommendation(stock)
                    st.markdown("#### 🎯 Full AI Recommendation")
                    st.markdown(recommendation['summary'])
                    
                    # Show chart
                    st.markdown("#### 📊 Price Chart & Technical Analysis")
                    # Get chart type from session state or use default
                    current_chart_type = st.session_state.get('chart_type', 'candlestick')
                    chart = create_price_chart(stock, stock['symbol'], chart_type=current_chart_type)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True, key=f"chart_buy_{stock['symbol']}_{i}")
        else:
            # Enhanced empty state for no BUY signals
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <h3>No BUY signals found</h3>
                <p>The current market conditions or your filter settings don't match any stocks with strong BUY signals.</p>
            </div>
            """, unsafe_allow_html=True)
            st.warning("⚠️ **No BUY signals found** in the current analysis. Try adjusting your filters or strategy.")
            st.info("💡 **Tips to find more BUY signals:**\n- Try the 'Momentum' or 'Aggressive' strategy presets\n- Lower the minimum score filter\n- Adjust RSI range to allow more oversold conditions\n- Check different sectors")
    
    with tab3:
        st.markdown("### 🔍 Detailed Stock Analysis")
        st.markdown("Select a stock to view comprehensive technical analysis and indicators.")
        
        if not filtered_stocks:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📈</div>
                <h3>No stocks available for analysis</h3>
                <p>Please adjust your filters to see stock details.</p>
            </div>
            """, unsafe_allow_html=True)
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
                # Header with copy button and watchlist
                header_col1, header_col2, header_col3 = st.columns([3, 1, 1])
                with header_col1:
                    st.markdown(f"#### 📊 {selected_stock['symbol']} - Overview")
                with header_col2:
                    st.markdown(create_copy_button_html(selected_stock['symbol'], "copy_detail"), unsafe_allow_html=True)
                with header_col3:
                    is_in_watchlist = selected_stock['symbol'] in st.session_state.watchlist
                    if is_in_watchlist:
                        if st.button("⭐ Remove from Watchlist", key="remove_watchlist_detail"):
                            remove_from_watchlist(selected_stock['symbol'])
                            st.rerun()
                    else:
                        if st.button("➕ Add to Watchlist", key="add_watchlist_detail"):
                            add_to_watchlist(selected_stock['symbol'])
                            st.success(f"Added {selected_stock['symbol']} to watchlist")
                            st.rerun()
                
                # Badges
                badges = get_performance_badges(selected_stock)
                if badges:
                    badge_html = '<div class="badge-container">' + "".join([f'<span class="badge-item" style="background: {badge[2]}; color: white;">{badge[0]} {badge[1]}</span>' for badge in badges]) + '</div>'
                    st.markdown(badge_html, unsafe_allow_html=True)
                
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
                # Get chart type from session state or use default
                current_chart_type = st.session_state.get('chart_type', 'candlestick')
                chart = create_price_chart(selected_stock, selected_symbol, chart_type=current_chart_type)
                if chart:
                    st.plotly_chart(chart, use_container_width=True, key=f"chart_detail_{selected_symbol}")
                
                # Buy signal info with better formatting
                st.markdown("---")
                if selected_stock.get('buy_signal'):
                    st.success(f"✅ **BUY Signal Detected**\n\n{selected_stock['buy_reason']}")
                else:
                    st.info(f"ℹ️ **Analysis:** {selected_stock['buy_reason']}")
                
                # Suggested Buy Price
                st.markdown("---")
                st.markdown("#### 💰 Suggested Buy Price & Range")
                ai = AIInsights()
                buy_price_info = ai.calculate_suggested_buy_price(
                    selected_stock, 
                    strategy=selected_strategy,
                    period=selected_period
                )
                
                price_col1, price_col2, price_col3, price_col4 = st.columns(4)
                with price_col1:
                    st.metric("Current Price", f"${buy_price_info['current_price']:.2f}")
                with price_col2:
                    st.metric(
                        "Suggested Price",
                        f"${buy_price_info['suggested_price']:.2f}",
                        delta=f"{buy_price_info['discount_pct']:.1f}% discount" if buy_price_info['discount_pct'] > 0 else f"{abs(buy_price_info['discount_pct']):.1f}% premium"
                    )
                with price_col3:
                    st.metric("Range Low", f"${buy_price_info['price_range_low']:.2f}")
                with price_col4:
                    st.metric("Range High", f"${buy_price_info['price_range_high']:.2f}")
                
                st.info(f"💡 **Calculation Basis**: {buy_price_info['reasoning']}")
                
                if buy_price_info['support_levels']:
                    st.caption("**Support Levels Considered**: " + ", ".join([f"{s[0]} (${s[1]:.2f})" for s in buy_price_info['support_levels'][:3]]))
                
                # AI Insight for selected stock
                st.markdown("---")
                st.markdown("#### 🤖 AI Insight")
                ai_insight = ai.generate_stock_insight(selected_stock)
                st.markdown(ai_insight)
                
                # AI Recommendation
                st.markdown("---")
                st.markdown("#### 🎯 AI Recommendation")
                recommendation = ai.generate_recommendation(selected_stock)
                st.markdown(recommendation['summary'])
                
                # Score Explanation
                st.markdown("#### 📊 Score Explanation")
                score_explanation = ai.explain_score(selected_stock)
                st.markdown(score_explanation)
    
    with tab4:
        st.markdown("### 🔎 Stock Search")
        st.markdown("Search for any stock by symbol to get comprehensive analysis and insights.")
        
        # Recent searches
        if st.session_state.recent_searches:
            st.markdown("**Recent Searches:**")
            recent_cols = st.columns(min(len(st.session_state.recent_searches), 5))
            for idx, recent_symbol in enumerate(st.session_state.recent_searches[:5]):
                with recent_cols[idx]:
                    if st.button(recent_symbol, key=f"recent_{recent_symbol}", use_container_width=True):
                        st.session_state.search_symbol = recent_symbol
                        st.rerun()
            st.markdown("---")
        
        # Search input
        col_search1, col_search2 = st.columns([3, 1])
        with col_search1:
            search_symbol = st.text_input(
                "Enter Stock Symbol",
                placeholder="e.g., AAPL, MSFT, GOOGL, TSLA",
                help="Enter a stock ticker symbol (e.g., AAPL for Apple Inc.)",
                key="stock_search_input",
                value=st.session_state.get('search_symbol', '')
            ).upper().strip()
        
        with col_search2:
            search_button = st.button("🔍 Search", type="primary", use_container_width=True)
        
        # Use period and interval from sidebar settings
        search_period = st.session_state.get('period', selected_period)
        search_interval = st.session_state.get('interval', selected_interval)
        
        if search_button or (search_symbol and search_symbol != ""):
            if not search_symbol:
                st.warning("⚠️ Please enter a stock symbol to search.")
            else:
                with st.spinner(f"🔍 **Analyzing {search_symbol}...** Fetching data and calculating indicators..."):
                    try:
                        # Initialize data fetcher
                        search_data_fetcher = DataFetcher()
                        
                        # Fetch stock data
                        stock_data = search_data_fetcher.get_stock_data(
                            search_symbol, 
                            period=search_period, 
                            interval=search_interval
                        )
                        
                        if stock_data is None or stock_data.empty:
                            st.error(f"❌ **Error**: Could not fetch data for {search_symbol}. Please check the symbol and try again.")
                            st.info("💡 **Tip**: Make sure you're using the correct ticker symbol (e.g., AAPL for Apple, not APPL).")
                        else:
                            # Calculate technical indicators
                            stock_data = search_data_fetcher.calculate_technical_indicators(stock_data)
                            
                            # Get stock info
                            stock_info = search_data_fetcher.get_stock_info(search_symbol)
                            
                            if stock_info is None:
                                st.warning(f"⚠️ **Warning**: Could not fetch detailed info for {search_symbol}, but price data is available.")
                                stock_info = {
                                    'symbol': search_symbol,
                                    'market_cap': 0,
                                    'sector': 'Unknown',
                                    'industry': 'Unknown',
                                    'current_price': float(stock_data['Close'].iloc[-1]),
                                    'volume': int(stock_data['Volume'].iloc[-1]) if not stock_data['Volume'].empty else 0,
                                    'avg_volume': 0,
                                    'pe_ratio': None,
                                    'dividend_yield': 0
                                }
                            
                            # Create stock data structure for analysis
                            latest = stock_data.iloc[-1]
                            current_price = float(latest['Close'])
                            
                            searched_stock = {
                                'symbol': search_symbol,
                                'current_price': current_price,
                                'rsi': float(latest['RSI']) if not pd.isna(latest['RSI']) else None,
                                'momentum': float(latest['Momentum']) if not pd.isna(latest['Momentum']) else None,
                                'volume_ratio': float(latest['Volume_Ratio']) if not pd.isna(latest['Volume_Ratio']) else None,
                                'market_cap': stock_info.get('market_cap', 0),
                                'sector': stock_info.get('sector', 'Unknown'),
                                'industry': stock_info.get('industry', 'Unknown'),
                                'data': stock_data,
                                'info': stock_info
                            }
                            
                            # Calculate score using stock selector
                            stock_selector = StockSelector(search_data_fetcher)
                            searched_stock['score'] = stock_selector._calculate_score(stock_data, stock_info)
                            
                            # Generate buy signal
                            strategy = TradingStrategy()
                            should_buy, reason = strategy.generate_buy_signal(searched_stock)
                            searched_stock['buy_signal'] = should_buy
                            searched_stock['buy_reason'] = reason
                            
                            # Add to recent searches
                            add_to_recent_searches(search_symbol)
                            
                            # Display results
                            st.success(f"✅ **Successfully analyzed {search_symbol}**")
                            
                            # Copy button and badges
                            col_copy, col_badges = st.columns([1, 4])
                            with col_copy:
                                st.markdown(create_copy_button_html(search_symbol, "copy_search"), unsafe_allow_html=True)
                            with col_badges:
                                badges = get_performance_badges(searched_stock)
                                if badges:
                                    badge_html = '<div class="badge-container">' + "".join([f'<span class="badge-item" style="background: {badge[2]}; color: white;">{badge[0]} {badge[1]}</span>' for badge in badges]) + '</div>'
                                    st.markdown(badge_html, unsafe_allow_html=True)
                            
                            st.markdown("---")
                            
                            # Stock Overview
                            st.markdown("#### 📊 Stock Overview")
                            
                            overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)
                            
                            with overview_col1:
                                st.markdown("**💰 Price & Score**")
                                st.metric("Current Price", f"${searched_stock['current_price']:.2f}")
                                
                                # Score with color coding
                                score = searched_stock['score']
                                if score >= 80:
                                    score_display = f"🟢 {score:.1f}"
                                elif score >= 60:
                                    score_display = f"🟡 {score:.1f}"
                                else:
                                    score_display = f"🔴 {score:.1f}"
                                st.metric("Quantitative Score", score_display)
                            
                            with overview_col2:
                                st.markdown("**📈 Technical Indicators**")
                                rsi_display = f"{searched_stock['rsi']:.1f}" if searched_stock['rsi'] else "N/A"
                                st.metric("RSI", rsi_display)
                                
                                momentum_display = f"{searched_stock['momentum']*100:+.2f}%" if searched_stock['momentum'] else "N/A"
                                st.metric("Momentum", momentum_display)
                            
                            with overview_col3:
                                st.markdown("**🏢 Company Info**")
                                st.metric("Sector", searched_stock['sector'])
                                st.metric("Industry", searched_stock['industry'])
                            
                            with overview_col4:
                                st.markdown("**🎯 Signal**")
                                signal_status = "✅ BUY" if searched_stock.get('buy_signal') else "⏸️ HOLD"
                                if searched_stock.get('buy_signal'):
                                    st.success(f"**{signal_status}**")
                                else:
                                    st.info(f"**{signal_status}**")
                                
                                # Market cap
                                market_cap = searched_stock.get('market_cap', 0)
                                if market_cap > 0:
                                    if market_cap >= 1e12:
                                        market_cap_display = f"${market_cap/1e12:.2f}T"
                                    elif market_cap >= 1e9:
                                        market_cap_display = f"${market_cap/1e9:.2f}B"
                                    else:
                                        market_cap_display = f"${market_cap/1e6:.2f}M"
                                    st.metric("Market Cap", market_cap_display)
                            
                            st.markdown("---")
                            
                            # Price Chart
                            st.markdown("#### 📈 Price Chart & Technical Analysis")
                            current_chart_type = st.session_state.get('chart_type', 'candlestick')
                            chart = create_price_chart(searched_stock, search_symbol, chart_type=current_chart_type)
                            if chart:
                                st.plotly_chart(chart, use_container_width=True, key=f"chart_search_{search_symbol}")
                            
                            st.markdown("---")
                            
                            # Detailed Technical Indicators
                            st.markdown("#### 🔬 Detailed Technical Indicators")
                            
                            tech_detail_col1, tech_detail_col2, tech_detail_col3 = st.columns(3)
                            
                            with tech_detail_col1:
                                st.markdown("**📈 Moving Averages**")
                                sma20 = latest.get('SMA_20', None)
                                sma50 = latest.get('SMA_50', None)
                                sma200 = latest.get('SMA_200', None)
                                
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
                                
                                if pd.notna(sma200):
                                    price_vs_sma200 = ((current_price - sma200) / sma200) * 100
                                    st.metric("SMA 200", f"${sma200:.2f}", f"{price_vs_sma200:+.1f}%")
                                else:
                                    st.metric("SMA 200", "N/A")
                            
                            with tech_detail_col2:
                                st.markdown("**📊 MACD Analysis**")
                                macd = latest.get('MACD', None)
                                macd_signal = latest.get('MACD_Signal', None)
                                macd_hist = latest.get('MACD_Histogram', None)
                                
                                if pd.notna(macd):
                                    st.metric("MACD", f"{macd:.2f}")
                                else:
                                    st.metric("MACD", "N/A")
                                
                                if pd.notna(macd_signal):
                                    st.metric("Signal Line", f"{macd_signal:.2f}")
                                else:
                                    st.metric("Signal Line", "N/A")
                                
                                if pd.notna(macd_hist):
                                    hist_color = "🟢" if macd_hist > 0 else "🔴"
                                    st.metric("Histogram", f"{hist_color} {macd_hist:.2f}")
                                
                                # MACD trend
                                if pd.notna(macd) and pd.notna(macd_signal):
                                    if macd > macd_signal:
                                        st.success("🟢 Bullish Trend")
                                    else:
                                        st.error("🔴 Bearish Trend")
                            
                            with tech_detail_col3:
                                st.markdown("**📉 Volatility & Bands**")
                                volatility = latest.get('Volatility', None)
                                if pd.notna(volatility):
                                    st.metric("Daily Volatility", f"{volatility*100:.2f}%")
                                else:
                                    st.metric("Daily Volatility", "N/A")
                                
                                bb_upper = latest.get('BB_Upper', None)
                                bb_lower = latest.get('BB_Lower', None)
                                bb_middle = latest.get('BB_Middle', None)
                                
                                if pd.notna(bb_upper) and pd.notna(bb_lower) and pd.notna(bb_middle):
                                    bb_position = (current_price - bb_lower) / (bb_upper - bb_lower)
                                    st.metric("BB Position", f"{bb_position*100:.1f}%")
                                    st.metric("BB Upper", f"${bb_upper:.2f}")
                                    st.metric("BB Lower", f"${bb_lower:.2f}")
                                    
                                    if bb_position < 0.2:
                                        st.info("📍 Near lower band (potentially oversold)")
                                    elif bb_position > 0.8:
                                        st.warning("📍 Near upper band (potentially overbought)")
                                    else:
                                        st.success("📍 Within normal range")
                                else:
                                    st.metric("Bollinger Bands", "N/A")
                            
                            st.markdown("---")
                            
                            # Buy Signal Details
                            if searched_stock.get('buy_signal'):
                                st.success(f"✅ **BUY Signal Detected**\n\n{searched_stock['buy_reason']}")
                            else:
                                st.info(f"ℹ️ **Analysis:** {searched_stock['buy_reason']}")
                            
                            st.markdown("---")
                            
                            # Suggested Buy Price
                            st.markdown("#### 💰 Suggested Buy Price & Range")
                            ai = AIInsights()
                            buy_price_info = ai.calculate_suggested_buy_price(
                                searched_stock, 
                                strategy=selected_strategy,
                                period=search_period
                            )
                            
                            price_col1, price_col2, price_col3, price_col4 = st.columns(4)
                            with price_col1:
                                st.metric("Current Price", f"${buy_price_info['current_price']:.2f}")
                            with price_col2:
                                discount_text = f"{buy_price_info['discount_pct']:.1f}% discount" if buy_price_info['discount_pct'] > 0 else f"{abs(buy_price_info['discount_pct']):.1f}% premium"
                                st.metric(
                                    "Suggested Price",
                                    f"${buy_price_info['suggested_price']:.2f}",
                                    delta=discount_text
                                )
                            with price_col3:
                                st.metric("Range Low", f"${buy_price_info['price_range_low']:.2f}")
                            with price_col4:
                                st.metric("Range High", f"${buy_price_info['price_range_high']:.2f}")
                            
                            st.info(f"💡 **Calculation Basis**: {buy_price_info['reasoning']}")
                            
                            if buy_price_info['support_levels']:
                                st.caption("**Support Levels Considered**: " + ", ".join([f"{s[0]} (${s[1]:.2f})" for s in buy_price_info['support_levels'][:3]]))
                            
                            st.markdown("---")
                            
                            # AI Insight
                            st.markdown("#### 🤖 AI Insight")
                            ai_insight = ai.generate_stock_insight(searched_stock)
                            st.markdown(ai_insight)
                            
                            st.markdown("---")
                            
                            # AI Recommendation
                            st.markdown("#### 🎯 AI Recommendation")
                            recommendation = ai.generate_recommendation(searched_stock)
                            
                            rec_col1, rec_col2, rec_col3 = st.columns(3)
                            with rec_col1:
                                confidence_color = "🟢" if recommendation['confidence'] == 'High' else "🟡" if recommendation['confidence'] == 'Medium' else "🔴"
                                st.metric("Confidence", f"{confidence_color} {recommendation['confidence']}")
                            with rec_col2:
                                risk_color = "🟢" if recommendation['risk_level'] == 'Low' else "🟡" if recommendation['risk_level'] == 'Medium' else "🔴"
                                st.metric("Risk Level", f"{risk_color} {recommendation['risk_level']}")
                            with rec_col3:
                                st.metric("Time Horizon", recommendation['time_horizon'])
                            
                            st.markdown(recommendation['summary'])
                            
                            if recommendation.get('reasoning'):
                                with st.expander("📋 Detailed Reasoning", expanded=False):
                                    for reason in recommendation['reasoning']:
                                        st.markdown(f"- {reason}")
                            
                            st.markdown("---")
                            
                            # Score Explanation
                            st.markdown("#### 📊 Score Explanation")
                            score_explanation = ai.explain_score(searched_stock)
                            st.markdown(score_explanation)
                            
                            # Additional Company Info
                            if stock_info and stock_info.get('pe_ratio'):
                                st.markdown("---")
                                st.markdown("#### 📋 Additional Company Information")
                                
                                info_col1, info_col2, info_col3 = st.columns(3)
                                
                                with info_col1:
                                    if stock_info.get('pe_ratio'):
                                        st.metric("P/E Ratio", f"{stock_info['pe_ratio']:.2f}")
                                    if stock_info.get('dividend_yield'):
                                        st.metric("Dividend Yield", f"{stock_info['dividend_yield']*100:.2f}%")
                                
                                with info_col2:
                                    if stock_info.get('volume'):
                                        st.metric("Current Volume", f"{stock_info['volume']:,}")
                                    if stock_info.get('avg_volume'):
                                        st.metric("Avg Volume", f"{stock_info['avg_volume']:,}")
                                
                                with info_col3:
                                    if searched_stock.get('volume_ratio'):
                                        st.metric("Volume Ratio", f"{searched_stock['volume_ratio']:.2f}x")
                    
                    except Exception as e:
                        st.error(f"❌ **Error analyzing {search_symbol}**: {str(e)}")
                        st.info("💡 **Tip**: Make sure the stock symbol is correct and the stock is actively traded.")
        
        else:
            # Show placeholder/instructions
            st.info("""
            **🔍 How to use Stock Search:**
            
            1. Enter a stock ticker symbol in the search box above (e.g., AAPL, MSFT, GOOGL)
            2. Click the "Search" button or press Enter
            3. View comprehensive analysis including:
               - Current price and quantitative score
               - Technical indicators (RSI, MACD, Moving Averages, Bollinger Bands)
               - Interactive price charts
               - AI-powered insights and recommendations
               - Suggested buy price and entry range
               - Detailed score breakdown
            
            **💡 Tip**: You can search for any stock listed on major exchanges (NYSE, NASDAQ, etc.)
            """)
    
    with tab6:
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
                    # Suggested Buy Price
                    st.markdown(f"##### 💰 Suggested Buy Price for {selected_ai_stock}")
                    buy_price_info = ai.calculate_suggested_buy_price(
                        selected_ai_stock_data, 
                        strategy=selected_strategy,
                        period=selected_period
                    )
                    
                    ai_price_col1, ai_price_col2, ai_price_col3 = st.columns(3)
                    with ai_price_col1:
                        st.metric("Suggested Price", f"${buy_price_info['suggested_price']:.2f}")
                    with ai_price_col2:
                        st.metric("Range Low", f"${buy_price_info['price_range_low']:.2f}")
                    with ai_price_col3:
                        st.metric("Range High", f"${buy_price_info['price_range_high']:.2f}")
                    
                    st.caption(f"💡 **Basis**: {buy_price_info['reasoning']} | Current: ${buy_price_info['current_price']:.2f}")
                    
                    st.markdown("---")
                    
                    # AI Insight
                    st.markdown(f"##### 📈 AI Insight for {selected_ai_stock}")
                    insight = ai.generate_stock_insight(selected_ai_stock_data)
                    st.markdown(insight)
                    
                    st.markdown("---")
                    
                    # AI Recommendation
                    st.markdown("##### 🎯 AI Recommendation")
                    recommendation = ai.generate_recommendation(selected_ai_stock_data)
                    
                    # Display enhanced recommendation
                    st.markdown(recommendation['summary'])
                    
                    st.markdown("---")
                    
                    # Score Explanation
                    st.markdown("##### 📊 Score Explanation")
                    score_explanation = ai.explain_score(selected_ai_stock_data)
                    st.markdown(score_explanation)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🤖</div>
                <h3>No stocks available for AI analysis</h3>
                <p>Please adjust your filters to enable AI-powered insights.</p>
            </div>
            """, unsafe_allow_html=True)
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
        st.markdown("### ⚖️ Compare Stocks")
        st.markdown("Compare up to 3 stocks side-by-side to make informed investment decisions.")
        
        # Stock selection for comparison
        comparison_stocks = []
        available_symbols = [s['symbol'] for s in filtered_stocks] if filtered_stocks else []
        
        if not available_symbols:
            st.warning("⚠️ No stocks available for comparison. Please adjust your filters first.")
        else:
            # Allow selection from filtered stocks or manual entry
            st.markdown("#### Select Stocks to Compare")
            
            compare_col1, compare_col2, compare_col3 = st.columns(3)
            
            with compare_col1:
                stock1 = st.selectbox(
                    "Stock 1",
                    options=[""] + available_symbols,
                    key="compare_stock1"
                )
                if stock1:
                    stock1_manual = st.text_input("Or enter symbol", key="compare_stock1_manual", value="").upper().strip()
                    if stock1_manual:
                        stock1 = stock1_manual
            
            with compare_col2:
                stock2 = st.selectbox(
                    "Stock 2",
                    options=[""] + available_symbols,
                    key="compare_stock2"
                )
                if stock2:
                    stock2_manual = st.text_input("Or enter symbol", key="compare_stock2_manual", value="").upper().strip()
                    if stock2_manual:
                        stock2 = stock2_manual
            
            with compare_col3:
                stock3 = st.selectbox(
                    "Stock 3 (Optional)",
                    options=[""] + available_symbols,
                    key="compare_stock3"
                )
                if stock3:
                    stock3_manual = st.text_input("Or enter symbol", key="compare_stock3_manual", value="").upper().strip()
                    if stock3_manual:
                        stock3 = stock3_manual
            
            compare_button = st.button("🔍 Compare Stocks", type="primary", use_container_width=True)
            
            if compare_button:
                comparison_symbols = [s for s in [stock1, stock2, stock3] if s]
                
                if len(comparison_symbols) < 2:
                    st.warning("⚠️ Please select at least 2 stocks to compare.")
                else:
                    with st.spinner("🔄 Fetching and analyzing stocks for comparison..."):
                        comparison_data = []
                        search_period = st.session_state.get('period', selected_period)
                        search_interval = st.session_state.get('interval', selected_interval)
                        compare_data_fetcher = DataFetcher()
                        
                        for symbol in comparison_symbols:
                            try:
                                # Fetch stock data
                                stock_data = compare_data_fetcher.get_stock_data(
                                    symbol, 
                                    period=search_period, 
                                    interval=search_interval
                                )
                                
                                if stock_data is not None and not stock_data.empty:
                                    # Calculate technical indicators
                                    stock_data = compare_data_fetcher.calculate_technical_indicators(stock_data)
                                    
                                    # Get stock info
                                    stock_info = compare_data_fetcher.get_stock_info(symbol)
                                    
                                    if stock_info is None:
                                        stock_info = {
                                            'symbol': symbol,
                                            'market_cap': 0,
                                            'sector': 'Unknown',
                                            'industry': 'Unknown',
                                            'current_price': float(stock_data['Close'].iloc[-1]),
                                            'volume': int(stock_data['Volume'].iloc[-1]) if not stock_data['Volume'].empty else 0,
                                            'avg_volume': 0,
                                            'pe_ratio': None,
                                            'dividend_yield': 0
                                        }
                                    
                                    # Create stock data structure
                                    latest = stock_data.iloc[-1]
                                    current_price = float(latest['Close'])
                                    
                                    compare_stock = {
                                        'symbol': symbol,
                                        'current_price': current_price,
                                        'rsi': float(latest['RSI']) if not pd.isna(latest['RSI']) else None,
                                        'momentum': float(latest['Momentum']) if not pd.isna(latest['Momentum']) else None,
                                        'volume_ratio': float(latest['Volume_Ratio']) if not pd.isna(latest['Volume_Ratio']) else None,
                                        'market_cap': stock_info.get('market_cap', 0),
                                        'sector': stock_info.get('sector', 'Unknown'),
                                        'industry': stock_info.get('industry', 'Unknown'),
                                        'data': stock_data,
                                        'info': stock_info
                                    }
                                    
                                    # Calculate score
                                    stock_selector = StockSelector(compare_data_fetcher)
                                    compare_stock['score'] = stock_selector._calculate_score(stock_data, stock_info)
                                    
                                    # Generate buy signal
                                    strategy = TradingStrategy()
                                    should_buy, reason = strategy.generate_buy_signal(compare_stock)
                                    compare_stock['buy_signal'] = should_buy
                                    compare_stock['buy_reason'] = reason
                                    
                                    comparison_data.append(compare_stock)
                                else:
                                    st.warning(f"⚠️ Could not fetch data for {symbol}")
                            except Exception as e:
                                st.error(f"❌ Error analyzing {symbol}: {str(e)}")
                        
                        if comparison_data:
                            st.success(f"✅ Successfully compared {len(comparison_data)} stocks")
                            st.markdown("---")
                            
                            # Comparison table
                            st.markdown("#### 📊 Side-by-Side Comparison")
                            
                            # Create comparison DataFrame
                            compare_df_data = []
                            for stock in comparison_data:
                                compare_df_data.append({
                                    'Symbol': stock['symbol'],
                                    'Score': f"{stock['score']:.1f}",
                                    'Price': f"${stock['current_price']:.2f}",
                                    'RSI': f"{stock['rsi']:.1f}" if stock['rsi'] else "N/A",
                                    'Momentum': f"{stock['momentum']*100:+.2f}%" if stock['momentum'] else "N/A",
                                    'Volume Ratio': f"{stock.get('volume_ratio', 0):.2f}x" if stock.get('volume_ratio') else "N/A",
                                    'Market Cap': f"${stock['market_cap']/1e9:.1f}B" if stock['market_cap'] > 0 else "N/A",
                                    'Sector': stock['sector'],
                                    'Signal': "✅ BUY" if stock.get('buy_signal') else "⏸️ HOLD"
                                })
                            
                            compare_df = pd.DataFrame(compare_df_data)
                            st.dataframe(compare_df, use_container_width=True, hide_index=True)
                            
                            # Metrics comparison
                            st.markdown("---")
                            st.markdown("#### 📈 Key Metrics Comparison")
                            
                            num_stocks = len(comparison_data)
                            metric_cols = st.columns(num_stocks)
                            
                            for idx, stock in enumerate(comparison_data):
                                with metric_cols[idx]:
                                    st.markdown(f"**{stock['symbol']}**")
                                    
                                    # Badges
                                    badges = get_performance_badges(stock)
                                    if badges:
                                        badge_html = '<div class="badge-container">' + "".join([f'<span class="badge-item" style="background: {badge[2]}; color: white;">{badge[0]} {badge[1]}</span>' for badge in badges]) + '</div>'
                                        st.markdown(badge_html, unsafe_allow_html=True)
                                    
                                    st.metric("Score", f"{stock['score']:.1f}")
                                    st.metric("Price", f"${stock['current_price']:.2f}")
                                    st.metric("RSI", f"{stock['rsi']:.1f}" if stock['rsi'] else "N/A")
                                    st.metric("Momentum", f"{stock['momentum']*100:+.2f}%" if stock['momentum'] else "N/A")
                                    st.metric("Signal", "✅ BUY" if stock.get('buy_signal') else "⏸️ HOLD")
                            
                            # Charts comparison
                            st.markdown("---")
                            st.markdown("#### 📊 Price Charts Comparison")
                            
                            current_chart_type = st.session_state.get('chart_type', 'candlestick')
                            chart_cols = st.columns(num_stocks)
                            
                            for idx, stock in enumerate(comparison_data):
                                with chart_cols[idx]:
                                    st.markdown(f"**{stock['symbol']}**")
                                    chart = create_price_chart(stock, stock['symbol'], chart_type=current_chart_type)
                                    if chart:
                                        st.plotly_chart(chart, use_container_width=True, key=f"compare_chart_{stock['symbol']}")
                            
                            # AI Insights comparison
                            st.markdown("---")
                            st.markdown("#### 🤖 AI Insights Comparison")
                            
                            ai = AIInsights()
                            insight_cols = st.columns(num_stocks)
                            
                            for idx, stock in enumerate(comparison_data):
                                with insight_cols[idx]:
                                    st.markdown(f"**{stock['symbol']}**")
                                    insight = ai.generate_stock_insight(stock)
                                    st.markdown(insight)
    
    with tab7:
        st.markdown("### 💼 My Portfolio")
        
        auth = st.session_state.auth
        if not auth.is_authenticated():
            st.warning("🔒 Please log in to access portfolio tracking.")
            st.info("💡 Create an account in the sidebar to save your portfolios and track performance.")
            
            st.markdown("---")
            st.markdown("#### 🎯 Benefits of Creating an Account")
            benefits_col1, benefits_col2 = st.columns(2)
            
            with benefits_col1:
                st.markdown("""
                **✨ Free Account Features:**
                - 💼 Create unlimited portfolios
                - 📊 Track your stock positions
                - 📈 Save recommendation history
                - ⭐ Personal watchlists
                - 💾 Data persistence across sessions
                - 📧 Email alerts (coming soon)
                """)
            
            with benefits_col2:
                st.markdown("""
                **🚀 Premium Features (Coming Soon):**
                - 🔄 Real-time data updates
                - 📊 Advanced analytics & backtesting
                - 🎯 Unlimited stock universe
                - 📱 Mobile app access
                - 🔔 Priority support
                - 📈 Performance tracking
                """)
        else:
            user_id = st.session_state.user_id
            db = st.session_state.db
            
            # Get user portfolios
            portfolios = db.get_user_portfolios(user_id)
            
            # Portfolio management
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("#### 📊 Your Portfolios")
            with col2:
                if st.button("➕ New Portfolio", use_container_width=True):
                    st.session_state.show_new_portfolio = True
            
            if st.session_state.get('show_new_portfolio', False):
                with st.form("new_portfolio_form"):
                    portfolio_name = st.text_input("Portfolio Name", value="My Portfolio")
                    initial_capital = st.number_input("Initial Capital ($)", min_value=1000, value=100000, step=1000)
                    create_portfolio = st.form_submit_button("Create Portfolio", use_container_width=True)
                    
                    if create_portfolio:
                        portfolio_id = db.create_portfolio(user_id, portfolio_name, initial_capital)
                        if portfolio_id:
                            st.success(f"Portfolio '{portfolio_name}' created!")
                            st.session_state.show_new_portfolio = False
                            st.rerun()
                        else:
                            st.error("Failed to create portfolio")
            
            if portfolios:
                for portfolio in portfolios:
                    with st.expander(f"📁 {portfolio['name']} - ${portfolio['initial_capital']:,.2f}"):
                        positions = db.get_portfolio_positions(portfolio['id'])
                        trades = db.get_user_recommendations(user_id, limit=10)
                        
                        if positions:
                            st.markdown("#### Current Positions")
                            pos_data = []
                            for pos in positions:
                                pos_data.append({
                                    "Symbol": pos['symbol'],
                                    "Shares": pos['shares'],
                                    "Entry Price": f"${pos['entry_price']:.2f}",
                                    "Entry Date": pos['entry_date']
                                })
                            st.dataframe(pd.DataFrame(pos_data), use_container_width=True, hide_index=True)
                        else:
                            st.info("No positions yet. Add stocks from recommendations to track your portfolio.")
                        
                        if trades:
                            st.markdown("#### Recent Recommendations")
                            trade_data = []
                            for trade in trades[:5]:
                                trade_data.append({
                                    "Symbol": trade['symbol'],
                                    "Action": trade['recommendation'],
                                    "Entry": f"${trade['entry_price']:.2f}" if trade['entry_price'] else "N/A",
                                    "Target": f"${trade['target_price']:.2f}" if trade['target_price'] else "N/A",
                                    "Score": f"{trade['score']:.1f}" if trade['score'] else "N/A",
                                    "Date": trade['created_at']
                                })
                            st.dataframe(pd.DataFrame(trade_data), use_container_width=True, hide_index=True)
            else:
                st.info("💡 You don't have any portfolios yet. Create one to start tracking your investments!")
                
                st.markdown("---")
                st.markdown("#### 🎯 Account Benefits")
                
                benefits_col1, benefits_col2 = st.columns(2)
                
                with benefits_col1:
                    st.markdown("""
                    **✨ What You Get with an Account:**
                    - 💼 **Portfolio Tracking**: Create unlimited portfolios
                    - 📊 **Position Management**: Track entry prices and dates
                    - 📈 **History**: Save all your recommendations
                    - ⭐ **Watchlists**: Personal stock lists
                    - 💾 **Data Persistence**: Your data saved across sessions
                    - 🔔 **Alerts**: Set price and signal alerts (coming soon)
                    """)
                
                with benefits_col2:
                    st.markdown("""
                    **🚀 Premium Features (Coming Soon):**
                    - 🔄 Real-time data updates
                    - 📊 Advanced analytics & backtesting
                    - 🎯 Unlimited stock universe
                    - 📱 Mobile app access
                    - 🔔 Priority email alerts
                    - 📈 Performance tracking & reports
                    - 🔌 API access for developers
                    """)
                
                st.markdown("---")
                st.markdown("""
                **💡 Difference Between Free and Premium:**
                
                **Free Account:**
                - Access to all current features
                - Limited to 37 pre-selected stocks
                - Basic portfolio tracking
                - Standard data refresh rates
                
                **Premium Plans:**
                - Unlimited stock analysis
                - Real-time data updates
                - Advanced features (backtesting, API, etc.)
                - Priority support
                - Early access to new features
                """)
    
    with tab8:
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
        - **Time Range**: Configurable in sidebar (1 month to 10 years, or maximum available)
        - **Data Interval**: Configurable (Daily, Weekly, Monthly, Quarterly)
        - **Update Frequency**: Every {config.UPDATE_INTERVAL_HOURS} hour(s)
        - **Stock Universe**: {len(config.STOCK_UNIVERSE)} stocks (configurable in config.py)
        
        **Time Range Options:**
        - **Period**: 1 Month, 3 Months, 6 Months, 1 Year, 2 Years, 5 Years, 10 Years, Year to Date, or Maximum Available
        - **Interval**: Daily (most detailed), Weekly, Monthly, or Quarterly (smoothed)
        
        All data is fetched in real-time and cached to minimize API calls. Different time ranges are cached separately for optimal performance.
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
    footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)
    
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
            f"<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
            f"🌐 Live App:<br><a href='https://quantify701.streamlit.app/' target='_blank' style='color: #667eea;'>quantify701.streamlit.app</a>"
            f"</div>",
            unsafe_allow_html=True
        )
    
    with footer_col4:
        st.markdown(
            "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
            "⚠️ Not financial advice<br>Do your own research"
            "</div>",
            unsafe_allow_html=True
        )


    
    with tab9:
        st.markdown("### ⚖️ Legal Information")
        
        legal_tab1, legal_tab2 = st.tabs(["Terms of Service", "Privacy Policy"])
        
        with legal_tab1:
            st.markdown(get_terms_of_service())
        
        with legal_tab2:
            st.markdown(get_privacy_policy())
        
        st.markdown("---")
        st.info("""
        **Questions about our legal policies?**
        
        Contact us through the GitHub repository or app support channels.
        """)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"❌ **Application Error**: {str(e)}")
        st.info("💡 **Troubleshooting**: Please refresh the page. If the error persists, check the logs or contact support.")
        import traceback
        with st.expander("🔍 Technical Details (for debugging)"):
            st.code(traceback.format_exc())

