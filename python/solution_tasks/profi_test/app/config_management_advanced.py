# -*- coding: utf-8 -*-
"""
Advanced Configuration Management System
Provides dynamic configuration management with hot reloading and validation
"""
import os
import json
import yaml
import logging
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict
from enum import Enum
from threading import Thread, Lock
import time
from pathlib import Path
from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

class ConfigFormat(Enum):
    """Supported configuration formats"""
    JSON = "json"
    YAML = "yaml"
    ENV = "env"

class ConfigScope(Enum):
    """Configuration scope levels"""
    GLOBAL = "global"
    APPLICATION = "application"
    MODULE = "module"
    USER = "user"

@dataclass
class ConfigMetadata:
    """Configuration metadata"""
    name: str
    scope: ConfigScope
    format: ConfigFormat
    version: str
    last_modified: float
    source: str
    description: str = ""

class AdvancedConfigManager:
    """Advanced configuration management system"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.configurations: Dict[str, Dict[str, Any]] = {}
        self.metadata: Dict[str, ConfigMetadata] = {}
        self.watchers: List[Thread] = []
        self.lock = Lock()
        self.validators: Dict[str, callable] = {}
        
        # Initialize default configurations
        self._initialize_default_configs()
    
    def _initialize_default_configs(self):
        """Initialize default configuration files"""
        default_configs = {
            'app': {
                'name': 'profi_test',
                'version': '1.0.0',
                'debug': False,
                'environment': 'production',
                'logging': {
                    'level': 'INFO',
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                }
            },
            'database': {
                'url': 'sqlite:///profi_test.db',
                'pool_size': 10,
                'pool_recycle': 3600,
                'echo': False
            },
            'cache': {
                'type': 'redis',
                'host': 'localhost',
                'port': 6379,
                'db': 0,
                'default_timeout': 300
            },
            'security': {
                'secret_key': 'change-me-in-production',
                'password_min_length': 8,
                'session_timeout': 3600,
                'rate_limit': {
                    'requests_per_minute': 60,
                    'requests_per_hour': 1000
                }
            },
            'monitoring': {
                'enabled': True,
                'metrics_interval': 30,
                'health_check_interval': 60,
                'log_retention_days': 30
            }
        }
        
        for config_name, config_data in default_configs.items():
            self.set_config(config_name, config_data, ConfigScope.APPLICATION)
            self._save_config_to_file(config_name, config_data)
    
    def set_config(self, name: str, config: Dict[str, Any], scope: ConfigScope = ConfigScope.APPLICATION,
                   description: str = "") -> bool:
        """Set configuration with metadata"""
        try:
            with self.lock:
                # Validate configuration if validator exists
                if name in self.validators:
                    if not self.validators[name](config):
                        logger.error(f"Configuration validation failed for {name}")
                        return False
                
                # Store configuration
                self.configurations[name] = config
                
                # Update metadata
                metadata = ConfigMetadata(
                    name=name,
                    scope=scope,
                    format=ConfigFormat.JSON,
                    version="1.0.0",
                    last_modified=time.time(),
                    source="runtime",
                    description=description
                )
                self.metadata[name] = metadata
                
                logger.info(f"Configuration {name} updated successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error setting configuration {name}: {e}")
            return False
    
    def get_config(self, name: str, default: Any = None) -> Any:
        """Get configuration value"""
        try:
            with self.lock:
                return self.configurations.get(name, default)
        except Exception as e:
            logger.error(f"Error getting configuration {name}: {e}")
            return default
    
    def get_nested_config(self, name: str, path: str, default: Any = None) -> Any:
        """Get nested configuration value using dot notation"""
        try:
            config = self.get_config(name, {})
            keys = path.split('.')
            value = config
            
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default
            
            return value
        except Exception as e:
            logger.error(f"Error getting nested configuration {name}.{path}: {e}")
            return default
    
    def update_config(self, name: str, updates: Dict[str, Any]) -> bool:
        """Update existing configuration with new values"""
        try:
            with self.lock:
                if name not in self.configurations:
                    logger.warning(f"Configuration {name} not found")
                    return False
                
                # Merge updates
                current_config = self.configurations[name].copy()
                self._deep_merge(current_config, updates)
                
                # Validate if validator exists
                if name in self.validators and not self.validators[name](current_config):
                    logger.error(f"Configuration validation failed for {name}")
                    return False
                
                # Update configuration
                self.configurations[name] = current_config
                self.metadata[name].last_modified = time.time()
                self.metadata[name].version = self._increment_version(self.metadata[name].version)
                
                # Save to file
                self._save_config_to_file(name, current_config)
                
                logger.info(f"Configuration {name} updated successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error updating configuration {name}: {e}")
            return False
    
    def _deep_merge(self, base: Dict, updates: Dict) -> Dict:
        """Deep merge two dictionaries"""
        for key, value in updates.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base
    
    def _increment_version(self, version: str) -> str:
        """Increment version string"""
        try:
            parts = version.split('.')
            parts[-1] = str(int(parts[-1]) + 1)
            return '.'.join(parts)
        except:
            return version
    
    def register_validator(self, name: str, validator: callable):
        """Register configuration validator"""
        self.validators[name] = validator
        logger.info(f"Validator registered for configuration {name}")
    
    def load_config_from_file(self, name: str, file_path: str, 
                            format: ConfigFormat = ConfigFormat.JSON) -> bool:
        """Load configuration from file"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.warning(f"Configuration file {file_path} not found")
                return False
            
            # Load based on format
            if format == ConfigFormat.JSON:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            elif format == ConfigFormat.YAML:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
            else:
                logger.error(f"Unsupported configuration format: {format}")
                return False
            
            # Set configuration
            scope = ConfigScope.APPLICATION  # Default scope
            self.set_config(name, config_data, scope, f"Loaded from {file_path}")
            
            logger.info(f"Configuration {name} loaded from {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading configuration from {file_path}: {e}")
            return False
    
    def _save_config_to_file(self, name: str, config_data: Dict[str, Any]):
        """Save configuration to file"""
        try:
            file_path = self.config_dir / f"{name}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving configuration {name}: {e}")
    
    def watch_config_file(self, name: str, file_path: str, 
                         format: ConfigFormat = ConfigFormat.JSON, 
                         interval: int = 5):
        """Watch configuration file for changes"""
        def watcher():
            last_modified = 0
            file_path_obj = Path(file_path)
            
            while True:
                try:
                    if file_path_obj.exists():
                        current_modified = file_path_obj.stat().st_mtime
                        if current_modified > last_modified:
                            logger.info(f"Configuration file {file_path} changed, reloading...")
                            self.load_config_from_file(name, file_path, format)
                            last_modified = current_modified
                    
                    time.sleep(interval)
                except Exception as e:
                    logger.error(f"Error in config watcher for {name}: {e}")
                    time.sleep(interval)
        
        watcher_thread = Thread(target=watcher, daemon=True)
        watcher_thread.start()
        self.watchers.append(watcher_thread)
        logger.info(f"Started watching configuration file: {file_path}")
    
    def get_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get all configurations"""
        with self.lock:
            return self.configurations.copy()
    
    def get_config_metadata(self, name: str) -> Optional[Dict]:
        """Get configuration metadata"""
        with self.lock:
            if name in self.metadata:
                return asdict(self.metadata[name])
            return None
    
    def get_configs_by_scope(self, scope: ConfigScope) -> Dict[str, Dict[str, Any]]:
        """Get configurations by scope"""
        result = {}
        with self.lock:
            for name, metadata in self.metadata.items():
                if metadata.scope == scope and name in self.configurations:
                    result[name] = self.configurations[name]
        return result
    
    def export_config(self, name: str, format: ConfigFormat = ConfigFormat.JSON) -> Optional[str]:
        """Export configuration in specified format"""
        try:
            config = self.get_config(name)
            if config is None:
                return None
            
            if format == ConfigFormat.JSON:
                return json.dumps(config, indent=2, ensure_ascii=False)
            elif format == ConfigFormat.YAML:
                return yaml.dump(config, default_flow_style=False, allow_unicode=True)
            else:
                return None
        except Exception as e:
            logger.error(f"Error exporting configuration {name}: {e}")
            return None
    
    def validate_all_configs(self) -> Dict[str, bool]:
        """Validate all configurations"""
        results = {}
        with self.lock:
            for name, config in self.configurations.items():
                if name in self.validators:
                    results[name] = self.validators[name](config)
                else:
                    results[name] = True  # No validator means valid by default
        return results

# Global configuration manager instance
config_manager = AdvancedConfigManager()

# Flask blueprint for configuration management API
config_bp = Blueprint('config_management', __name__)

@config_bp.route('/api/config')
def get_all_configs():
    """Get all configurations"""
    try:
        configs = config_manager.get_all_configs()
        metadata = {}
        for name in configs.keys():
            meta = config_manager.get_config_metadata(name)
            if meta:
                metadata[name] = meta
        
        return jsonify({
            'success': True,
            'configs': configs,
            'metadata': metadata
        })
    except Exception as e:
        logger.error(f"Error getting configurations: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@config_bp.route('/api/config/<name>')
def get_config(name):
    """Get specific configuration"""
    try:
        config = config_manager.get_config(name)
        if config is None:
            return jsonify({
                'success': False,
                'error': f'Configuration {name} not found'
            }), 404
        
        metadata = config_manager.get_config_metadata(name)
        
        return jsonify({
            'success': True,
            'config': config,
            'metadata': metadata
        })
    except Exception as e:
        logger.error(f"Error getting configuration {name}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@config_bp.route('/api/config/<name>', methods=['POST'])
def update_config(name):
    """Update configuration"""
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        updates = request.get_json()
        if not isinstance(updates, dict):
            return jsonify({
                'success': False,
                'error': 'Invalid configuration format'
            }), 400
        
        success = config_manager.update_config(name, updates)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Configuration {name} updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to update configuration {name}'
            }), 400
            
    except Exception as e:
        logger.error(f"Error updating configuration {name}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@config_bp.route('/api/config/<name>/validate')
def validate_config(name):
    """Validate configuration"""
    try:
        config = config_manager.get_config(name)
        if config is None:
            return jsonify({
                'success': False,
                'error': f'Configuration {name} not found'
            }), 404
        
        # Perform validation
        validation_results = config_manager.validate_all_configs()
        is_valid = validation_results.get(name, True)
        
        return jsonify({
            'success': True,
            'valid': is_valid,
            'details': validation_results
        })
    except Exception as e:
        logger.error(f"Error validating configuration {name}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@config_bp.route('/api/config/export/<name>')
def export_config(name):
    """Export configuration"""
    try:
        format_str = request.args.get('format', 'json').upper()
        try:
            format_enum = ConfigFormat[format_str]
        except KeyError:
            return jsonify({
                'success': False,
                'error': f'Unsupported format: {format_str}'
            }), 400
        
        exported = config_manager.export_config(name, format_enum)
        if exported is None:
            return jsonify({
                'success': False,
                'error': f'Configuration {name} not found or export failed'
            }), 404
        
        return jsonify({
            'success': True,
            'format': format_enum.value,
            'data': exported
        })
    except Exception as e:
        logger.error(f"Error exporting configuration {name}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def init_config_management(app):
    """Initialize configuration management system"""
    # Register blueprint
    app.register_blueprint(config_bp, url_prefix='/admin')
    
    # Setup configuration validators
    def validate_app_config(config):
        required_keys = ['name', 'version', 'environment']
        return all(key in config for key in required_keys)
    
    def validate_database_config(config):
        required_keys = ['url']
        return all(key in config for key in required_keys)
    
    def validate_security_config(config):
        required_keys = ['secret_key']
        return all(key in config for key in required_keys)
    
    config_manager.register_validator('app', validate_app_config)
    config_manager.register_validator('database', validate_database_config)
    config_manager.register_validator('security', validate_security_config)
    
    # Watch configuration files for changes
    config_files = [
        ('app', 'config/app.json'),
        ('database', 'config/database.json'),
        ('security', 'config/security.json')
    ]
    
    for name, file_path in config_files:
        if Path(file_path).exists():
            config_manager.watch_config_file(name, file_path)
    
    logger.info("Configuration management system initialized")
