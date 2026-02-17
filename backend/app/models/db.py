import json
import os
from typing import List, Dict

QUEUE_FILE = "data/mentor_queue.json"


def load_queue() -> List[Dict]:
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, "r") as f:
        return json.load(f)


def save_queue(queue: List[Dict]):
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)
