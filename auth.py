"""
Authentication module for user login and registration.
Integrates with Streamlit for session management.
"""

import streamlit as st
import re
from typing import Optional, Dict
from database import Database
import logging

logger = logging.getLogger(__name__)


class AuthManager:
    """
    Manages user authentication and session state.
    """
    
    def __init__(self, db: Database):
        """
        Initialize authentication manager.
        
        Args:
            db: Database instance
        """
        self.db = db
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize authentication-related session state."""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'user_data' not in st.session_state:
            st.session_state.user_data = None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current authenticated user data."""
        if self.is_authenticated():
            return st.session_state.user_data
        return None
    
    def login(self, username: str, password: str) -> tuple[bool, str]:
        """
        Authenticate a user.
        
        Args:
            username: Username or email
            password: Password
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not username or not password:
            return False, "Please enter both username and password"
        
        user = self.db.authenticate_user(username, password)
        
        if user:
            st.session_state.authenticated = True
            st.session_state.user_id = user['id']
            st.session_state.username = user['username']
            st.session_state.user_data = user
            logger.info(f"User logged in: {user['username']}")
            return True, "Login successful!"
        else:
            return False, "Invalid username or password"
    
    def register(self, username: str, email: str, password: str, confirm_password: str) -> tuple[bool, str]:
        """
        Register a new user.
        
        Args:
            username: Desired username
            email: Email address
            password: Password
            confirm_password: Password confirmation
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validation
        if not username or not email or not password:
            return False, "Please fill in all fields"
        
        if password != confirm_password:
            return False, "Passwords do not match"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        if not self._is_valid_email(email):
            return False, "Invalid email address"
        
        if not self._is_valid_username(username):
            return False, "Username must be 3-20 characters and contain only letters, numbers, and underscores"
        
        # Create user
        user_id = self.db.create_user(username, email, password)
        
        if user_id:
            # Auto-login after registration
            st.session_state.authenticated = True
            st.session_state.user_id = user_id
            st.session_state.username = username
            st.session_state.user_data = self.db.get_user(user_id)
            logger.info(f"User registered: {username}")
            return True, "Registration successful! You are now logged in."
        else:
            return False, "Registration failed. Username or email may already be taken."
    
    def logout(self):
        """Log out the current user."""
        username = st.session_state.get('username', 'Unknown')
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.user_data = None
        logger.info(f"User logged out: {username}")
        st.rerun()
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _is_valid_username(self, username: str) -> bool:
        """Validate username format."""
        if len(username) < 3 or len(username) > 20:
            return False
        pattern = r'^[a-zA-Z0-9_]+$'
        return re.match(pattern, username) is not None
    
    def require_auth(self):
        """
        Require authentication - redirect to login if not authenticated.
        This should be called at the start of protected pages.
        """
        if not self.is_authenticated():
            st.warning("🔒 Please log in to access this feature.")
            st.stop()

