import json
from pathlib import Path

def _load(path, default):
    p = Path(path)
    if not p.exists():
        return default
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def _save(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_tokens(path):
    return _load(path, {"users": []})

def save_tokens(path, data):
    _save(path, data)

def load_last_sync(path):
    return _load(path, {})

def save_last_sync(path, data):
    _save(path, data)
