"""
This module contains the different supported feature store implementations.
Currently, the only supported feature store is ``SimpleFeatureStore``.
"""

from serpytor.components.feature_store.config import CONFIG
from serpytor.components.feature_store.feature_stores import SimpleFeatureStore

__all__ = (
    "SimpleFeatureStore",
    "CONFIG",
)
