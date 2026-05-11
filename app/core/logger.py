import json
import logging
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        for field in ["campaign_id", "agent", "lead_id", "step"]:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value

        return json.dumps(payload)


def get_logger(name: str = "arip"):
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    logger.addHandler(handler)
    logger.propagate = False

    return logger