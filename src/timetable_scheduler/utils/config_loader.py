"""Configuration loader utility."""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigLoader:
    """Utility class for loading and managing configuration files."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the config loader.
        
        Args:
            config_dir: Directory containing configuration files
        """
        if config_dir is None:
            # Default to config directory relative to project root
            project_root = Path(__file__).parent.parent.parent.parent
            config_dir = project_root / "config"
        
        self.config_dir = Path(config_dir)
        self._configs: Dict[str, Any] = {}
    
    def load_config(self, config_name: str) -> Dict[str, Any]:
        """
        Load a configuration file.
        
        Args:
            config_name: Name of the config file (without .yaml extension)
            
        Returns:
            Dictionary containing configuration data
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid YAML
        """
        if config_name in self._configs:
            return self._configs[config_name]
        
        config_path = self.config_dir / f"{config_name}.yaml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
                self._configs[config_name] = config_data
                return config_data
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in config file {config_path}: {e}")
    
    def get_default_config(self) -> Dict[str, Any]:
        """Load the default configuration."""
        return self.load_config("default")
    
    def get_constraints_config(self) -> Dict[str, Any]:
        """Load the constraints configuration."""
        return self.load_config("constraints")
    
    def merge_configs(self, *config_names: str) -> Dict[str, Any]:
        """
        Merge multiple configuration files.
        
        Args:
            config_names: Names of config files to merge
            
        Returns:
            Merged configuration dictionary
        """
        merged = {}
        
        for config_name in config_names:
            config = self.load_config(config_name)
            merged.update(config)
        
        return merged
    
    def get_config_value(self, config_name: str, key_path: str, default: Any = None) -> Any:
        """
        Get a specific value from a configuration using dot notation.
        
        Args:
            config_name: Name of the config file
            key_path: Dot-separated path to the value (e.g., "database.host")
            default: Default value if key is not found
            
        Returns:
            Configuration value or default
        """
        config = self.load_config(config_name)
        
        keys = key_path.split('.')
        value = config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def reload_config(self, config_name: str) -> Dict[str, Any]:
        """
        Reload a configuration file from disk.
        
        Args:
            config_name: Name of the config file to reload
            
        Returns:
            Reloaded configuration dictionary
        """
        if config_name in self._configs:
            del self._configs[config_name]
        
        return self.load_config(config_name)
    
    def clear_cache(self):
        """Clear all cached configuration data."""
        self._configs.clear()
    
    def list_available_configs(self) -> list:
        """
        List all available configuration files.
        
        Returns:
            List of available config file names (without .yaml extension)
        """
        if not self.config_dir.exists():
            return []
        
        config_files = []
        for file_path in self.config_dir.glob("*.yaml"):
            config_files.append(file_path.stem)
        
        return sorted(config_files)


# Global config loader instance
_config_loader = None


def get_config_loader(config_dir: Optional[str] = None) -> ConfigLoader:
    """
    Get the global config loader instance.
    
    Args:
        config_dir: Directory containing configuration files
        
    Returns:
        ConfigLoader instance
    """
    global _config_loader
    
    if _config_loader is None:
        _config_loader = ConfigLoader(config_dir)
    
    return _config_loader


def load_config(config_name: str) -> Dict[str, Any]:
    """
    Convenience function to load a configuration file.
    
    Args:
        config_name: Name of the config file
        
    Returns:
        Configuration dictionary
    """
    return get_config_loader().load_config(config_name)