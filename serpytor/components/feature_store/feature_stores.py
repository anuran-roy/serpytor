# from rich import print as rich_print
from functools import lru_cache
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

import pandas as pd
import polars as pl

from serpytor.components.feature_store.config import CONFIG


class SimpleFeatureStore:
    def __init__(
        self,
        dataframe: Union[pd.DataFrame, pl.DataFrame],
        index_col: Optional[Union[str, None]] = None,
        cache_size: int = 1000,
        backend: Optional[str] = "pandas",
    ) -> None:
        """Initialize the Simple Feature Storage Object."""
        self.dataframe = dataframe
        self.index_col_position: int = 0
        self.backend = backend
        self.features_dict: Dict[str, Any] = {}
        self.dataframe_cols: List[str] = list(dataframe.columns)
        self.index_col = index_col

        if "cache_size" in CONFIG:
            self.cache_size = int(CONFIG["cache_size"])

        if self.backend == "pandas":
            self.features_dict: Dict = dataframe.T.to_dict()
        elif self.backend == "polars":
            self.features_dict: Dict = dataframe.transpose().to_dict()

        self.features_dict = self.mould_df(self.features_dict, index_col)
        if index_col is not None and index_col in self.dataframe_cols:
            self.index_col_position: int = self.dataframe_cols.index(index_col)

    def get_feature_index(self, column_name: str) -> int:
        """Get feature index for given feature name. Returns -1 if not found."""
        if column_name in self.dataframe_cols:
            return self.dataframe_cols.index(column_name)

        return -1

    def update_indices(self) -> None:
        """Update the indices for the Simple Feature Storage object when new data is entered.
        Not needed for Pandas backend.
        """
        pass

    def mould_df(
        self,
        features_dict: Union[pd.DataFrame, pl.DataFrame],
        index_field: Union[str, None] = None,
    ) -> Dict[str, Any]:
        """Mould the features dictionary to the Simple Feature Storage object into an indexable form.
        Not required for Pandas backend.
        """
        if self.backend == "pandas":
            return features_dict

    def register_feature(
        self,
        feature_name: str,
        feature_definition: Optional[Callable] = lambda x: x,
        feature_data: Optional[Union[Iterable, None]] = None,
        in_place: bool = False,
    ) -> Union[Iterable, None]:
        """Add a new feature to the Simple Feature Storage object."""
        feature_index: int = self.get_feature_index(feature_name)

        if feature_index == -1:
            if feature_data is None:
                raise Exception("Neither feature data nor feature name found")
            if len(feature_data) == len(self.features_dict):
                for row in range(len(feature_data)):
                    feature_data[row] = feature_definition(feature_data[row])
                self.features_dict[feature_name] = pd.Series(
                    self.features_dict[feature_name]
                )

    @lru_cache(maxsize=CONFIG["cache_size"])
    def get_feature(
        self,
        feature_name: Optional[Union[str, None]] = None,
        comparator: Optional[Union[Callable, None]] = None,
    ) -> Dict[str, Any]:
        """Get Feature Data from a given feature name and/or comparator function."""
        if self.backend == "pandas":
            self.selected_data = self.dataframe.T.to_dict()
            if feature_name is not None and feature_name in self.features_dict:
                self.selected_data = self.features_dict[feature_name]
            return filter(comparator, self.selected_data)

    def get_all_data(self) -> Dict[str, Any]:
        """Returns all the data stored in the Simple Feature Storage object as a dictionary."""
        return self.features_dict
