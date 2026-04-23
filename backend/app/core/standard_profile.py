from pathlib import Path
import yaml

PROFILE_PATH = Path(__file__).resolve().parents[2] / "config" / "standard_profile_v1.yaml"

with open(PROFILE_PATH, "r", encoding="utf-8") as f:
    STANDARD_PROFILE = yaml.safe_load(f)
