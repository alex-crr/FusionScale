import json
import os

_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

_DEFAULTS = {
    "px_per_cm": None,
    "reference_length_mm": 50.0,
}


def load() -> dict:
    if os.path.exists(_CONFIG_PATH):
        with open(_CONFIG_PATH, "r") as f:
            return {**_DEFAULTS, **json.load(f)}
    return dict(_DEFAULTS)


def save(cfg: dict):
    with open(_CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


def is_calibrated() -> bool:
    return load().get("px_per_cm") is not None
