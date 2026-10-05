import json
import os

# Outside the add-in folder so calibration survives App Store updates/reinstalls.
_BASE = os.environ.get("APPDATA") or os.path.expanduser("~/Library/Application Support")
_CONFIG_PATH = os.path.join(_BASE, "Autodesk", "FusionScale", "config.json")

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
    os.makedirs(os.path.dirname(_CONFIG_PATH), exist_ok=True)
    with open(_CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


def is_calibrated() -> bool:
    return load().get("px_per_cm") is not None
