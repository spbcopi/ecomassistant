from pathlib import Path
import os
import yaml

def _project_root() -> Path:
    # .../utils/config_loader.py -> parents[1] == project root
    return Path(__file__).resolve().parents[1]

def load_config(cfg_path: str | None = None) -> dict:
    """
    Resolve config path reliably irrespective of CWD.
    Priority: explicit arg > CONFIG_PATH env > <project_root>/config/config.yaml
    """
    env_path = os.getenv("CONFIG_PATH")
    if not cfg_path:
        cfg_path = env_path or str(_project_root() / "config" / "config.yaml")

    path = Path(cfg_path)
    if not path.is_absolute():
        path = _project_root() / path

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        # Return empty dict if file is empty
        return yaml.safe_load(f) or {}