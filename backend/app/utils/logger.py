import json
import os
from datetime import datetime, timezone
from typing import Dict

AUDIT_LOG_FILE = "data/audit_logs.json"


def log_event(event: Dict):
    """
    Appends an audit event to audit_logs.json
    """
    event["timestamp"] = datetime.now(timezone.utc).isoformat()

    if not os.path.exists(AUDIT_LOG_FILE):
        logs = []
    else:
        try:
            with open(AUDIT_LOG_FILE, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

    logs.append(event)

    with open(AUDIT_LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
