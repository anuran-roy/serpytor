import datetime
from pathlib import Path
from typing import Callable, Dict, Optional, Union

import joblib
from sklearn.pipeline import Pipeline


async def save_pipeline(
    pipeline: Pipeline,
    save_dir: str,
    timestamp: Optional[Union[str, Callable]] = str(datetime.datetime.now()),
    output_format: Optional[str] = "pickle",
) -> str:
    """Saves the pipeline in a format of the user's choice."""
    EXTENSIONS: Dict[str, str] = {
        "pickle": ".pkl",
        "json": ".json",
        "yaml": ".yaml",
        "csv": ".csv",
        "tsv": ".tsv",
        "xml": ".xml",
        "pt": ".pt",
    }

    MODELS_DIR = save_dir
    model_path: Path = MODELS_DIR / f"model-{timestamp}{EXTENSIONS[output_format]}"
    joblib.dump(pipeline, model_path.resolve())

    return model_path
