import logging
import os
from utils.logger_util import LoggerUtil

def test_get_logger_returns_logger():
    logger = LoggerUtil.get_logger("test_logger_util")
    assert isinstance(logger, logging.Logger)


def test_logger_writes_to_file():
    logger = LoggerUtil.get_logger("test_logger_util_file")
    test_message = "LoggerUtil test message"
    logger.info(test_message)
    # Always resolve logs/ relative to the project root, not tests/
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    logs_dir = os.path.join(project_root, "logs")
    log_filename = os.path.join(
        logs_dir,
        f"log_{__import__('datetime').datetime.now().strftime('%Y-%m-%d')}.log",
    )
    with open(log_filename, "r") as f:
        log_content = f.read()
    assert test_message in log_content
