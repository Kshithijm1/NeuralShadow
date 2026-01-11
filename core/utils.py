import sys
from loguru import logger
from .config import LOGS_DIR

def setup_logger():
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(LOGS_DIR / "app.log", rotation="10 MB", level="DEBUG")
    return logger

log = setup_logger()
