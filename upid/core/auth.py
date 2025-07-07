"""
Authentication management for UPID CLI
"""
import json
import time
from typing import Optional, Dict, Any
from upid.core.api_client import UPIDAPIClient

class AuthManager:
    """Authentication manager for UPID CLI"""
    
    def __init__(self, config):
        self.config = config
        self.api_client = UPIDAPIClient(config)
        self._current_user = None
    
    def login(self, email: str, password: str, server: str = None) -> str:
        """Login to UPID platform"""
        if server:
            self.config.set('api_url', server)
            self.api_client = UPIDAPIClient(self.config)
        
        try:
            response = self.api_client.login(email, password)
            token = response.get('token')
            
            if not token:
                raise Exception("No token received from server")
            
            # Store token
            self.config.set_auth_token(token)
            self.api_client.set_auth_token(token)
            
            # Store user info
            self._current_user = response.get('user', {})
            
            return token
            
        except Exception as e:
            raise Exception(f"Login failed: {e}")
    
    def logout(self):
        """Logout from UPID platform"""
        try:
            if self.config.is_authenticated():
                self.api_client.logout()
        except Exception:
            # Ignore logout errors
            pass
        finally:
            self.config.clear_auth_token()
            self.api_client.clear_auth_token()
            self._current_user = None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        if not self.config.is_authenticated():
            return False
        
        # Verify token is still valid
        try:
            self.get_current_user()
            return True
        except Exception:
            # Token is invalid, clear it
            self.config.clear_auth_token()
            return False
    
    def get_current_user(self) -> Dict[str, Any]:
        """Get current user information"""
        if self._current_user is None:
            try:
                response = self.api_client.get_profile()
                self._current_user = response.get('user', {})
            except Exception as e:
                raise Exception(f"Failed to get user profile: {e}")
        
        return self._current_user
    
    def refresh_token(self) -> str:
        """Refresh authentication token"""
        try:
            response = self.api_client.refresh_token()
            token = response.get('token')
            
            if not token:
                raise Exception("No token received from refresh")
            
            # Update stored token
            self.config.set_auth_token(token)
            self.api_client.set_auth_token(token)
            
            return token
            
        except Exception as e:
            raise Exception(f"Token refresh failed: {e}")
    
    def get_token(self) -> Optional[str]:
        """Get current authentication token"""
        return self.config.get_auth_token()
    
    def validate_token(self) -> bool:
        """Validate current token"""
        try:
            self.get_current_user()
            return True
        except Exception:
            return False
    
    def get_user_email(self) -> Optional[str]:
        """Get current user email"""
        try:
            user = self.get_current_user()
            return user.get('email')
        except Exception:
            return None
    
    def get_user_organization(self) -> Optional[str]:
        """Get current user organization"""
        try:
            user = self.get_current_user()
            return user.get('organization')
        except Exception:
            return None
    
    def get_user_roles(self) -> list:
        """Get current user roles"""
        try:
            user = self.get_current_user()
            return user.get('roles', [])
        except Exception:
            return []
    
    def has_role(self, role: str) -> bool:
        """Check if user has specific role"""
        roles = self.get_user_roles()
        return role in roles
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        try:
            user = self.get_current_user()
            permissions = user.get('permissions', [])
            return permission in permissions
        except Exception:
            return False 