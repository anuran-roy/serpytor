from serpytor.feature_store.feature_stores import SimpleFeatureStore
from serpytor.feature_store.config import CONFIG

"""
This module contains the implementations for the different feature stores to be supported.  
Currently, the only supported feature store is ``SimpleFeatureStore``.
"""


__all__ = (
    "SimpleFeatureStore",
    "CONFIG",
)
