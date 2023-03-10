from functools import cache, lru_cache
from typing import Any, Dict, List, Optional, Tuple

from serpytor.components.utils.algorithms.allocation.base_allocation import (
    BaseAllocation,
)


class RoundRobinAllocation(BaseAllocation):
    """ """

    def queue(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        ...
