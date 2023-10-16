"""
AppLogger Module
----------------
This module provides a singleton logger for the application,
as well as a rich console handler for enhanced logging output.
"""

import logging

from rich.console import Console
from rich.logging import RichHandler


from src.utils.singleton import SingletonMeta


class AppLogger(metaclass=SingletonMeta):
    """This class provides a logger that follows the Singleton pattern."""

    _logger = None

    def __init__(self):
        """Initialize the logger."""
        self._logger = logging.getLogger(__name__)

    def get_logger(self):
        """Return the logger instance."""
        return self._logger

    @staticmethod
    def get_instance():
        """Return the singleton instance of the AppLogger class."""
        return AppLogger()


class RichConsoleHandler(RichHandler):
    """Custom RichHandler for console output."""

    def __init__(self, width=200, style=None, **kwargs):
        """Initialize the RichConsoleHandler."""
        super().__init__(
            console=Console(color_system="256", width=width, style=style), **kwargs
        )
