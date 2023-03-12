from threading import Lock
from typing import Any, Dict, List, Optional

from tinydb import Query, TinyDB


class DBIO:
    """Thread-safe logging for Databases."""

    def __init__(
        self, db_url: str, table_name: Optional[str] = "_default", *args, **kwargs
    ):
        self.lock = Lock()
        self.db_url: Optional[str] = db_url
        self.table_name: Optional[str] = table_name
        self.db = TinyDB(self.db_url).table(self.table_name)

    def read_from_db(
        self, query: Dict[str, Any], *args, **kwargs
    ) -> List[Dict[str, Any]]:
        """Read operations don't need to synchronized.
        So we don't use locks to read the database."""
        db_query = Query()
        return self.db.search(db_query.fragment(query))

    def read_all_from_db(self) -> List[Dict[str, Any]]:
        return self.db.all()

    def write_to_db(self, data: Dict[Any, Any], *args, **kwargs) -> None:
        """Write operations need to be synchronized.
        So we use locks while writing into the database."""
        self.lock.acquire()
        try:
            self.db.insert(data)
        finally:
            self.lock.release()
