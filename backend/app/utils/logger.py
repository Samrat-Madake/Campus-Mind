"""
Audit Logger
=============
Appends structured audit events to a JSON log file.
Separate from operational/application logging.
"""

import json
import logging
import os
from datetime import datetime, timezone
from typing import Dict

from app.core.settings import AUDIT_LOG_PATH

logger = logging.getLogger(__name__)


def log_event(event: Dict):
    """
    Appends an audit event to the audit log file.
    Each event gets a UTC timestamp automatically.
    """
    event["timestamp"] = datetime.now(timezone.utc).isoformat()

    if not os.path.exists(AUDIT_LOG_PATH):
        logs = []
    else:
        try:
            with open(AUDIT_LOG_PATH, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logger.warning("Corrupt audit log file, starting fresh.")
            logs = []

    logs.append(event)

    with open(AUDIT_LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)

    logger.info(
        "Audit event logged: type=%s action=%s",
        event.get("type", "unknown"),
        event.get("action", "N/A"),
    )
