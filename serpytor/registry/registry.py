from functools import lru_cache
from tinydb import TinyDB, Query, Document
from ..feature_store.feature_stores import SimpleFeatureStore
import yaml
from ..config import CONFIG
from pathlib import Path
from typing import Optional, Dict, Tuple, Depends, Any
from datetime import datetime

REGISTRY_DIR = ""


class SimpleModelRegistry:
    def __init__(
        self, db_path: Optional[str] = str(REGISTRY_DIR / "registry.json")
    ) -> None:
        self.db = TinyDB(db_path)
        self.registry: Dict[str, Any] = {}

    def write_to_db(self, entry: Dict[str, Any]) -> None:
        for index, i in enumerate(self.registry):
            self.db.insert({i: self.registry[i], "id": index + 1})

    def add_to_registry(
        self,
        model_name: Optional[str] = datetime.now(),
        params: Dict[str, Any] = None,
        id: int = len(self.db) + 1,
    ) -> None:
        pass
