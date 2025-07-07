"""
Configuration management for UPID CLI
"""
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
import yaml

class Config:
    """Configuration manager for UPID CLI"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_dir = Path.home() / '.upid'
        self.config_file = self.config_dir / 'config.json'
        self.auth_file = self.config_dir / 'auth.json'
        
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)
        
        # Load configuration
        self.config = self._load_config()
        
        # Set default values
        self._set_defaults()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            raise Exception(f"Failed to save configuration: {e}")
    
    def _set_defaults(self):
        """Set default configuration values"""
        defaults = {
            'api_url': 'https://api.upid.io',
            'api_version': 'v1',
            'timeout': 30,
            'verbose': False,
            'output_format': 'table',
            'color_output': True,
            'default_cluster': None,
            'optimization_strategy': 'balanced',
            'safety_level': 'strict',
            'auto_rollback': True,
            'notification_channels': [],
            'cost_model': 'aws',
            'currency': 'USD'
        }
        
        for key, value in defaults.items():
            if key not in self.config:
                self.config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value
        self._save_config()
    
    def get_auth_token(self) -> Optional[str]:
        """Get authentication token"""
        if self.auth_file.exists():
            try:
                with open(self.auth_file, 'r') as f:
                    auth_data = json.load(f)
                    return auth_data.get('token')
            except (json.JSONDecodeError, IOError):
                return None
        return None
    
    def set_auth_token(self, token: str):
        """Set authentication token"""
        auth_data = {'token': token}
        try:
            with open(self.auth_file, 'w') as f:
                json.dump(auth_data, f)
        except IOError as e:
            raise Exception(f"Failed to save auth token: {e}")
    
    def clear_auth_token(self):
        """Clear authentication token"""
        if self.auth_file.exists():
            self.auth_file.unlink()
    
    def get_api_url(self) -> str:
        """Get API URL"""
        return self.get('api_url')
    
    def get_api_version(self) -> str:
        """Get API version"""
        return self.get('api_version')
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.get_auth_token() is not None
    
    def get_default_cluster(self) -> Optional[str]:
        """Get default cluster ID"""
        return self.get('default_cluster')
    
    def set_default_cluster(self, cluster_id: str):
        """Set default cluster ID"""
        self.set('default_cluster', cluster_id)
    
    def get_optimization_strategy(self) -> str:
        """Get optimization strategy"""
        return self.get('optimization_strategy')
    
    def set_optimization_strategy(self, strategy: str):
        """Set optimization strategy"""
        self.set('optimization_strategy', strategy)
    
    def get_safety_level(self) -> str:
        """Get safety level"""
        return self.get('safety_level')
    
    def set_safety_level(self, level: str):
        """Set safety level"""
        self.set('safety_level', level)
    
    def get_cost_model(self) -> str:
        """Get cost model"""
        return self.get('cost_model')
    
    def set_cost_model(self, model: str):
        """Set cost model"""
        self.set('cost_model', model)
    
    def get_currency(self) -> str:
        """Get currency"""
        return self.get('currency')
    
    def set_currency(self, currency: str):
        """Set currency"""
        self.set('currency', currency)
    
    def is_verbose(self) -> bool:
        """Check if verbose mode is enabled"""
        return self.get('verbose', False)
    
    def set_verbose(self, verbose: bool):
        """Set verbose mode"""
        self.set('verbose', verbose)
    
    def get_output_format(self) -> str:
        """Get output format"""
        return self.get('output_format')
    
    def set_output_format(self, format: str):
        """Set output format"""
        self.set('output_format', format)
    
    def is_color_output(self) -> bool:
        """Check if color output is enabled"""
        return self.get('color_output', True)
    
    def set_color_output(self, color: bool):
        """Set color output"""
        self.set('color_output', color)
    
    def get_timeout(self) -> int:
        """Get request timeout"""
        return self.get('timeout', 30)
    
    def set_timeout(self, timeout: int):
        """Set request timeout"""
        self.set('timeout', timeout)
    
    def get_notification_channels(self) -> list:
        """Get notification channels"""
        return self.get('notification_channels', [])
    
    def add_notification_channel(self, channel: str):
        """Add notification channel"""
        channels = self.get_notification_channels()
        if channel not in channels:
            channels.append(channel)
            self.set('notification_channels', channels)
    
    def remove_notification_channel(self, channel: str):
        """Remove notification channel"""
        channels = self.get_notification_channels()
        if channel in channels:
            channels.remove(channel)
            self.set('notification_channels', channels)
    
    def export_config(self, file_path: str):
        """Export configuration to file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            raise Exception(f"Failed to export configuration: {e}")
    
    def import_config(self, file_path: str):
        """Import configuration from file"""
        try:
            with open(file_path, 'r') as f:
                imported_config = json.load(f)
                self.config.update(imported_config)
                self._save_config()
        except (json.JSONDecodeError, IOError) as e:
            raise Exception(f"Failed to import configuration: {e}")
    
    def reset_config(self):
        """Reset configuration to defaults"""
        self.config = {}
        self._set_defaults()
        self._save_config()
        self.clear_auth_token() 