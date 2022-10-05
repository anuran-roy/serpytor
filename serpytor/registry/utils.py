from typing import Union, Optional, List, Tuple, Dict, Callable, Iterable
from sklearn.pipeline import Pipeline
import datetime
from pathlib import Path

# from ..config import MODELS_DIR, EXTENSIONS
import joblib
from serpytor.exports import export


async def save_pipeline(
    pipeline: Pipeline,
    timestamp: Optional[Union[str, Callable]] = str(datetime.datetime.now()),
    output_format: Optional[str] = "pickle",
) -> str:
    """Saves the pipeline in a format."""
    EXTENSIONS: Dict[str, str] = {
        "pickle": ".pkl",
        "json": ".json",
        "yaml": ".yaml",
        "csv": ".csv",
        "tsv": ".tsv",
        "xml": ".xml",
    }
    model_path: Path = MODELS_DIR / f"model-{timestamp}{EXTENSIONS[output_format]}"
    joblib.dump(pipeline, model_path.resolve())

    return model_path
