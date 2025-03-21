import typing
from typing_extensions import override

import pandas as pd

from strategy import DeduplicationStrategy


# TYPES:


_T = typing.TypeVar("_T")


# CUSTOM:


class Custom(DeduplicationStrategy):

    def __init__(
        self,
        func: typing.Callable[..., dict[_T, _T]],
        df: pd.DataFrame,
        attr: str,
        **kwargs,
    ):
        self._func = func
        self._df = df
        self._attr = attr
        self._kwargs = kwargs

    @override
    def dedupe(self) -> pd.DataFrame:
        print(f"evaluating {self.__class__.__name__}")
        return self._assign_group_id(
            self._df,
            self._df[self._attr].map(
                self._func(
                    self._df,
                    self._attr,
                    **self._kwargs,
                )
            ),
        )


def my_func(df: pd.DataFrame, attr: str, /, match_str: str) -> dict[str, str]:
    my_map = {}
    for irow, _ in df.iterrows():
        left = df.loc[irow, attr]
        my_map[left] = left
        for jrow, _ in df.iterrows():
            right = df.loc[jrow, attr]
            if match_str in left.lower() and match_str in right.lower():
                my_map[left] = right
                break
    return my_map


# import data
# df = data.df3
# my_func(df, "address", "london")
