"""Configuration management utilities."""

from pathlib import Path
from typing import Any, Dict
import yaml


def load_yaml(path: Path) -> Dict[str, Any]:
    """
    Load YAML configuration file.
    
    Args:
        path: Path to YAML file
        
    Returns:
        Parsed configuration dictionary
    """
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def merge_configs(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two configuration dictionaries.
    
    Args:
        base: Base configuration
        override: Override configuration (takes precedence)
        
    Returns:
        Merged configuration
    """
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    
    return result


def load_team_config(team_config_path: Path, base_config_path: Path) -> Dict[str, Any]:
    """
    Load and merge team configuration with base configuration.
    
    Args:
        team_config_path: Path to team-specific config
        base_config_path: Path to base config
        
    Returns:
        Merged configuration dictionary
    """
    base = load_yaml(base_config_path)
    team = load_yaml(team_config_path)
    
    return merge_configs(base, team)


def get_config_value(config: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    Get nested configuration value using dot notation.
    
    Args:
        config: Configuration dictionary
        key_path: Dot-separated key path (e.g., "simulation.churn_base_rate")
        default: Default value if key not found
        
    Returns:
        Configuration value or default
    """
    keys = key_path.split('.')
    value = config
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    
    return value
