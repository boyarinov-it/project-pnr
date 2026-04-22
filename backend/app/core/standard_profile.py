from pathlib import Path

import yaml


BASE_DIR = Path(__file__).resolve().parents[2]
PROFILE_PATH = BASE_DIR / "config" / "standard_profile_v1.yaml"


with PROFILE_PATH.open("r", encoding="utf-8") as f:
    STANDARD_PROFILE = yaml.safe_load(f)
