"""
Database module for persistent data storage.
Uses SQLite for simplicity (can be upgraded to PostgreSQL later).
"""

import sqlite3
import hashlib
import secrets
from datetime import datetime
from typing import Optional, Dict, List
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class Database:
    """
    Database manager for user data, portfolios, and preferences.
    """
    
    def __init__(self, db_path: str = "quantify701.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        # Create data directory if it doesn't exist
        db_dir = Path(db_path).parent
        if db_dir and not db_dir.exists():
            db_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self._init_tables()
        logger.info(f"Database initialized at {db_path}")
    
    def _init_tables(self):
        """Initialize database tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                subscription_tier TEXT DEFAULT 'free'
            )
        """)
        
        # User preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER PRIMARY KEY,
                default_strategy TEXT DEFAULT 'Default',
                default_period TEXT DEFAULT '1y',
                default_interval TEXT DEFAULT '1d',
                watchlist TEXT,  -- JSON array of symbols
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Portfolios table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                initial_capital REAL DEFAULT 100000,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Positions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                portfolio_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                shares INTEGER NOT NULL,
                entry_price REAL NOT NULL,
                entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                current_price REAL,
                FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
            )
        """)
        
        # Trade history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trade_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                portfolio_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                action TEXT NOT NULL,  -- 'BUY' or 'SELL'
                shares INTEGER NOT NULL,
                price REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
            )
        """)
        
        # Alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                alert_type TEXT NOT NULL,  -- 'price_target', 'stop_loss', 'signal'
                target_value REAL,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                triggered_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Recommendations history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                recommendation TEXT NOT NULL,  -- 'BUY', 'HOLD', 'SELL'
                entry_price REAL,
                target_price REAL,
                hold_days INTEGER,
                score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        self.conn.commit()
        logger.info("Database tables initialized")
    
    # User management methods
    def create_user(self, username: str, email: str, password: str) -> Optional[int]:
        """
        Create a new user account.
        
        Args:
            username: Unique username
            email: Unique email address
            password: Plain text password (will be hashed)
        
        Returns:
            User ID if successful, None otherwise
        """
        try:
            password_hash = self._hash_password(password)
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            """, (username, email, password_hash))
            user_id = cursor.lastrowid
            
            # Create default preferences
            cursor.execute("""
                INSERT INTO user_preferences (user_id)
                VALUES (?)
            """, (user_id,))
            
            self.conn.commit()
            logger.info(f"User created: {username} (ID: {user_id})")
            return user_id
        except sqlite3.IntegrityError as e:
            logger.error(f"Failed to create user {username}: {e}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """
        Authenticate a user.
        
        Args:
            username: Username or email
            password: Plain text password
        
        Returns:
            User dictionary if authenticated, None otherwise
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM users 
            WHERE (username = ? OR email = ?) AND is_active = 1
        """, (username, username))
        user = cursor.fetchone()
        
        if user and self._verify_password(password, user['password_hash']):
            # Update last login
            cursor.execute("""
                UPDATE users SET last_login = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (user['id'],))
            self.conn.commit()
            
            user_dict = dict(user)
            logger.info(f"User authenticated: {username}")
            return user_dict
        else:
            logger.warning(f"Authentication failed for: {username}")
            return None
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None
    
    def get_user_preferences(self, user_id: int) -> Dict:
        """Get user preferences."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user_preferences WHERE user_id = ?", (user_id,))
        prefs = cursor.fetchone()
        if prefs:
            return dict(prefs)
        return {}
    
    def update_user_preferences(self, user_id: int, **kwargs):
        """Update user preferences."""
        if not kwargs:
            return
        
        cursor = self.conn.cursor()
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [user_id]
        
        cursor.execute(f"""
            UPDATE user_preferences SET {set_clause}
            WHERE user_id = ?
        """, values)
        self.conn.commit()
        logger.debug(f"Updated preferences for user {user_id}")
    
    # Portfolio methods
    def create_portfolio(self, user_id: int, name: str, initial_capital: float = 100000) -> Optional[int]:
        """Create a new portfolio for a user."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO portfolios (user_id, name, initial_capital)
                VALUES (?, ?, ?)
            """, (user_id, name, initial_capital))
            portfolio_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Portfolio created: {name} (ID: {portfolio_id})")
            return portfolio_id
        except Exception as e:
            logger.error(f"Failed to create portfolio: {e}")
            return None
    
    def get_user_portfolios(self, user_id: int) -> List[Dict]:
        """Get all portfolios for a user."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM portfolios WHERE user_id = ?
            ORDER BY updated_at DESC
        """, (user_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def add_position(self, portfolio_id: int, symbol: str, shares: int, entry_price: float):
        """Add a position to a portfolio."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO positions (portfolio_id, symbol, shares, entry_price)
            VALUES (?, ?, ?, ?)
        """, (portfolio_id, symbol, shares, entry_price))
        self.conn.commit()
    
    def get_portfolio_positions(self, portfolio_id: int) -> List[Dict]:
        """Get all positions for a portfolio."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM positions WHERE portfolio_id = ?
        """, (portfolio_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def add_trade(self, portfolio_id: int, symbol: str, action: str, shares: int, price: float):
        """Record a trade in history."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO trade_history (portfolio_id, symbol, action, shares, price)
            VALUES (?, ?, ?, ?, ?)
        """, (portfolio_id, symbol, action, shares, price))
        self.conn.commit()
    
    # Alert methods
    def create_alert(self, user_id: int, symbol: str, alert_type: str, target_value: float) -> Optional[int]:
        """Create a new alert."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO alerts (user_id, symbol, alert_type, target_value)
                VALUES (?, ?, ?, ?)
            """, (user_id, symbol, alert_type, target_value))
            alert_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Alert created: {symbol} {alert_type} @ {target_value}")
            return alert_id
        except Exception as e:
            logger.error(f"Failed to create alert: {e}")
            return None
    
    def get_user_alerts(self, user_id: int, active_only: bool = True) -> List[Dict]:
        """Get alerts for a user."""
        cursor = self.conn.cursor()
        if active_only:
            cursor.execute("""
                SELECT * FROM alerts 
                WHERE user_id = ? AND is_active = 1
                ORDER BY created_at DESC
            """, (user_id,))
        else:
            cursor.execute("""
                SELECT * FROM alerts 
                WHERE user_id = ?
                ORDER BY created_at DESC
            """, (user_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    # Recommendation history
    def save_recommendation(self, user_id: int, symbol: str, recommendation: str, 
                          entry_price: float, target_price: float, hold_days: int, score: float):
        """Save a recommendation to history."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO recommendation_history 
            (user_id, symbol, recommendation, entry_price, target_price, hold_days, score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, symbol, recommendation, entry_price, target_price, hold_days, score))
        self.conn.commit()
    
    def get_user_recommendations(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Get recommendation history for a user."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM recommendation_history 
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]
    
    # Password hashing utilities
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256 with salt."""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against a hash."""
        try:
            salt, stored_hash = password_hash.split(':')
            computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return computed_hash == stored_hash
        except:
            return False
    
    def close(self):
        """Close database connection."""
        self.conn.close()
        logger.info("Database connection closed")

