import os
import json


def load_config(config_file="config.json"):
    if not os.path.exists(config_file):
        # Fallback Values
        return {
            "days": [
                "Samstag",
                "Sonntag",
            ],
            "times": [f"{h:02d}:00" for h in range(10, 14)]
            + [f"{h:02d}:30" for h in range(10, 14)],
            "leagues": [],
            "age_classes": [],
        }
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)
