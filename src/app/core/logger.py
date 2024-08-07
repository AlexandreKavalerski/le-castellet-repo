import logging
import os
import requests
import json
from logging.handlers import RotatingFileHandler
from logging import LogRecord
from ..core.config import settings
from ..core.utils.json_formater import CustomJsonFormatter

class SplunkHandler(logging.Handler):
    def __init__(self, splunk_url: str, splunk_token: str) -> None:
        super().__init__()
        self.splunk_url = splunk_url
        self.splunk_token = splunk_token

    def emit(self, record: LogRecord) -> None:
        log_entry = self.format(record)
        headers = {
            'Authorization': f'Splunk {self.splunk_token}'
        }
        data = {
            "event": json.loads(log_entry),
            # "sourcetype": "_raw",
            "sourcetype": "_json",
            "index": "lecastelet",
        }
        try:
            requests.post(self.splunk_url, headers=headers, data=json.dumps(data))
        except Exception as e:
            print(f"Failed to send log to Splunk: {e}")


LOGGING_LEVEL = logging.INFO
# LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGGING_FORMAT = "%(asctime)s %(filename)s %(funcName)s %(levelname)s %(lineno)d %(module)s %(message)s %(pathname)s %(process)s"

logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT)
logger = logging.getLogger("lecastellet")

if settings.SPLUNK_IS_ENABLED:
    splunk_url = settings.SPLUNK_URL
    splunk_token = settings.SPLUNK_TOKEN


    splunk_handler = SplunkHandler(splunk_url, splunk_token)
    splunk_handler.setLevel(LOGGING_LEVEL)
    splunk_handler.setFormatter(CustomJsonFormatter(LOGGING_FORMAT))

    logger.addHandler(splunk_handler)


LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")

file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=10485760, backupCount=5)
file_handler.setLevel(LOGGING_LEVEL)
file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))

logger.addHandler(file_handler)
