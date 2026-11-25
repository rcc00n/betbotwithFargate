"""Runtime configuration; values must never be committed or logged."""
import json
import os


def required_env(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Set {name} in the environment before starting this program.")
    return value


def json_object(name):
    raw = os.environ.get(name, "{}").strip() or "{}"
    try:
        value = json.loads(raw)
    except (ValueError, TypeError):
        raise RuntimeError(f"{name} must contain a JSON object.") from None
    if not isinstance(value, dict):
        raise RuntimeError(f"{name} must contain a JSON object.")
    return value
