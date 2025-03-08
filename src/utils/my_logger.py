import datetime as dt
import json
import logging.config
import logging.handlers
import sys
from typing import Any, override
from pathlib import Path
import atexit

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


# Refer to this video: https://youtu.be/9L77QExPmI0 For further explanation
# Src code: https://github.com/mCodingLLC/VideosSampleCode/tree/master/videos/135_modern_logging
# Python >= 3.12 required
class MyJSONFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(record.created).strftime(
                "%Y-%m-%dT%H:%M:%S"
            ),
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: msg_val
            if (msg_val := always_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        for (
            key,
            val,
        ) in (
            record.__dict__.items()
        ):  # extra logging details (i.e. logger.info(info, extra={"key": "val"}))
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message


# class NonErrorFilter(logging.Filter):
#     @override
#     def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
#         return record.levelno <= logging.INFO


logger = logging.getLogger("bait-zakat-backend")


def setup_logging():
    # Check if running as PyInstaller bundle
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # Running in PyInstaller bundle
        base_path = Path(sys._MEIPASS)
        config_file = base_path.joinpath("queued-json-file-logging-config.json")
    else:
        # Running in normal Python environment
        config_file = Path("src").joinpath("queued-json-file-logging-config.json")
    with open(config_file) as f_in:
        config = json.load(f_in)

    # Create directories for any file handlers
    for handler_config in config.get("handlers", {}).values():
        if handler_config.get("class") in (
            "logging.FileHandler",
            "logging.handlers.RotatingFileHandler",
        ):
            if "filename" in handler_config:
                log_path = Path(handler_config["filename"])
                log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler: Any
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


def control_uvicorn_loggers():
    """
    Silence uvicorn INFO logs but keep warnings and errors
    Note: Must be called after uvicorn.run or it will have no effect 
    """ 
    uvicorn_loggers = [
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
    ]

    for uvicorn_logger in uvicorn_loggers:
        # Remove any existing handlers to prevent stdout output
        for handler in uvicorn_logger.handlers:
            uvicorn_logger.removeHandler(handler)

        # Set level to WARNING so we only capture warnings and above
        uvicorn_logger.setLevel(logging.WARNING)

        # Only use our configured handlers
        uvicorn_logger.propagate = True
