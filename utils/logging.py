# Logging utility code
import logging
from functools import wraps
from flask import request, current_app
import time


def log_request(f):
    """
    A decorator that logs incoming requests.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_app.logger.info(
            f"Request: {request.method} {request.path} {request.headers}"
        )
        return f(*args, **kwargs)

    return decorated_function


def record_execution_time(f):
    """
    A decorator that records the execution time of a function.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        current_app.logger.info(f"Execution time: {elapsed_time:.3f} seconds")
        return result

    return decorated_function


def setup_logging(log_level=logging.INFO):
    """
    Initialize the logger for the application.
    """
    # Create a logger object
    logger = logging.getLogger(__name__)

    # Set the logging level
    logger.setLevel(log_level)

    # Create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)

    return logger
