import os
import logging

LOG_DIR = os.path.join(os.path.expanduser("~"), ".dev-dashboard")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "dashboard.log")


def get_logger():

    logger = logging.getLogger("dev-dashboard")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(message)s",
        "%H:%M:%S"
    )

    file_handler = logging.FileHandler(LOG_FILE)

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger