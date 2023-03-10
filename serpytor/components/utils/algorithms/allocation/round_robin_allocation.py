from typing import Any, Dict, List

from serpytor.components.utils.algorithms.allocation.base_allocation import \
    BaseAllocation


class RoundRobinAllocation(BaseAllocation):
    """ """

    def queue(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        ...
