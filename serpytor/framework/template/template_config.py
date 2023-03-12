from pathlib import Path
from typing import Any, Dict, Tuple, Union

import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from serpytor.components.events.event_capture import EventCapture

BASE_DIR: Path = Path(__file__).parent

REGISTRY_DIR: Path = BASE_DIR / "registry/"

MODELS_DIR: Path = BASE_DIR / "models/"

PIPELINE: Tuple[Union[None, Any]] = ()

SENTRY_SETTINGS: Dict[str, Any] = {
    "dsn": "",  # Enter your sentry DSN key here
    "integrations": [AioHttpIntegration()],  # Add more integrations if needed.
    "traces_sample_rate": 1.0,
}

sentry_sdk.init(**SENTRY_SETTINGS)

event_capture: EventCapture = EventCapture(db_url=str(BASE_DIR / "db.json"))
