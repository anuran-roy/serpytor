"""
"""

from serpytor.components.utils.algorithms.allocation.fair_resource_allocation import (
    FairResourceAllocation,
)
from serpytor.components.utils.algorithms.allocation.fcfs_allocation import (
    FCFSAllocation,
)
from serpytor.components.utils.algorithms.allocation.round_robin_allocation import (
    RoundRobinAllocation,
)

from typing import Tuple

__all__: Tuple = ("FairResourceAllocation", "FCFSAllocation", "RoundRobinAllocation")
