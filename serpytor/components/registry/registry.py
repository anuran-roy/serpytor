from datetime import datetime
from functools import lru_cache
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional
from uuid import uuid4

from serpytor.components.database.db import DBIO

REGISTRY_DIR = Path("")


class SimpleModelRegistry:
    """Simple, thread-safe model registry.
    Conventions:
        1. Stores all data in the ``model_registry`` table in the database.
        2. Stores all data in-memory until ``write_all_to_db()`` is invoked, to avoid excessive database writes.
        3. Add a model to the main memory using ``add_to_registry()``.
    """

    def __init__(self, db_url: str) -> None:
        self.db: DBIO = DBIO(table_name="model_registry", db_url=db_url)
        self.registry: Dict[str, Any] = {}
        self.lock = Lock()

    def write_all_to_db(self) -> None:
        """Write all the in-memory models to the database.
        Can be used as a batch process, to avoid writing bottlenecks.
        """
        for i in self.registry:
            self.db.write_to_db(self.registry[i] | {"id": i})

        self.registry: Dict[str, Any] = {}

    def add_to_registry(
        self,
        model_name: Optional[str] = datetime.now(),
        params: Dict[str, Any] = None,
        id: Optional[str] = str(uuid4().hex),
    ) -> None:
        """Add a model to the model registry.
        This operation is atomic, and performed in-memory to avoid database writes that are slow in nature.
        """
        self.lock.acquire()
        self.registry[id]: Dict[str, Any] = {"params": params} | {
            "model_name": model_name
        }
        self.lock.release()

    @lru_cache(maxsize=100)
    def get_from_registry(self, model_id: str, *args, **kwargs) -> Dict[str, Any]:
        """Read the database and return model details by id.
        LRU Caching is used to speed up lookups and reduce database reads.
        """
        return self.db.read_from_db(model_id, *args, **kwargs)

    @lru_cache(maxsize=10)
    def get_all_from_registry(self) -> List[Dict[str, Any]]:
        """Get all model entries from the registry.
        LRU Caching is used to speed up lookups and reduce database reads.
        """
        return self.db.read_all_from_db()
