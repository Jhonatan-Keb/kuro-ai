"""Carga y guarda configuración desde config/config.yaml."""

import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config" / "config.yaml"


def load() -> dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def save(config: dict):
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
