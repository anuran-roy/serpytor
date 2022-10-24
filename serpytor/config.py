from pathlib import Path
from yaml import safe_load

BASE_DIR = Path(__file__).parent

CONFIG = safe_load(open(str(BASE_DIR / "config.yaml")).read())
