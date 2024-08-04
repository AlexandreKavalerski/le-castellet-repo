from pythonjsonlogger import jsonlogger
from logging import LogRecord
from typing import Any, Dict


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: Dict[str, Any], record: LogRecord, message_dict: Dict[str, Any]) -> None:
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        if log_record.get("level"):
            log_record["level"] = log_record["level"].lower()
        else:
            log_record["level"] = record.levelname.lower()

        del log_record["levelname"]
