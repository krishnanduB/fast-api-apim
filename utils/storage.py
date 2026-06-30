import json
import os

def read_data(filepath: str) -> list:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_data(filepath: str, data: list):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
