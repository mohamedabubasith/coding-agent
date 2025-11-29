"""Centralized logging system for coding-agent-plugin."""

import logging
import os
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str, 
    level: str = "INFO",
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with console and optional file output.
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with color
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Detailed format for file, simpler for console
    console_format = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        detailed_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(detailed_format)
        logger.addHandler(file_handler)
    
    return logger


def get_project_logger(project_id: str, agent_name: str) -> logging.Logger:
    """
    Get a logger for a specific project and agent.
    
    Args:
        project_id: Project identifier
        agent_name: Name of the agent
        
    Returns:
        Logger with file output to project's log directory
    """
    log_dir = Path(f"projects/{project_id}/.agent_context/logs")
    log_file = log_dir / f"{agent_name}.log"
    
    return setup_logger(
        name=f"{project_id}.{agent_name}",
        level="DEBUG",
        log_file=str(log_file)
    )


# Global logger for general use
logger = setup_logger("coding_agent_plugin")
