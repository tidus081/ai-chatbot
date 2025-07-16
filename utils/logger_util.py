import logging
import os
from datetime import datetime


class LoggerUtil:
    @staticmethod
    def get_log_filename() -> str:
        logs_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs"
        )
        os.makedirs(logs_dir, exist_ok=True)
        log_filename = os.path.join(
            logs_dir, f"log_{datetime.now().strftime('%Y-%m-%d')}.log"
        )
        return log_filename
    
    @staticmethod
    def get_logger(
        name: str = "app_logger", level: int = logging.INFO, for_client: bool = False
    ) -> logging.Logger:
        logger = logging.getLogger(name)
        if not logger.handlers:
            # Console handler
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            if for_client:
                stream_handler.setFormatter(
                    logging.Formatter(
                        "%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
                    )
                )
            else:
                stream_handler.setFormatter(
                    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
                )

            # File handler
            file_handler = logging.FileHandler(LoggerUtil.get_log_filename())
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )

            # Add handlers to the logger
            logger.addHandler(stream_handler)
            logger.addHandler(file_handler)
            logger.setLevel(level)
        return logger
