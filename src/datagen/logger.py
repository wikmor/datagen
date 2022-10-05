import logging
import warnings


def error(message: str):
    """Log error message and exit the application"""
    logging.error(message)
    exit(1)


def warn(message: str):
    """Utility function for logging application warnings"""
    warnings.warn(message)
