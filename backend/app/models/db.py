"""
JSON File Persistence for Mentor Queue
=======================================
Uses centralized path from settings instead of hardcoded strings.
"""

import json
import os
from typing import List, Dict

from app.core.settings import MENTOR_QUEUE_PATH


def load_queue() -> List[Dict]:
    """Load the mentor queue from JSON file."""
    if not os.path.exists(MENTOR_QUEUE_PATH):
        return []
    with open(MENTOR_QUEUE_PATH, "r") as f:
        return json.load(f)


def save_queue(queue: List[Dict]):
    """Save the mentor queue to JSON file."""
    with open(MENTOR_QUEUE_PATH, "w") as f:
        json.dump(queue, f, indent=2)
