import functools
import logging
from typing_extensions import override

import numpy as np
from rapidfuzz import fuzz

from dupegrouper.definitions import TMP_ATTR_LABEL, frames
from dupegrouper.strategy import DeduplicationStrategy


# LOGGER:


logger = logging.getLogger(__name__)


# FUZZY:


class Fuzzy(DeduplicationStrategy):

    def __init__(self, tolerance: float = 0.05):
        self._tolerance = tolerance
        self._ratio = 100 * (1 - tolerance)

    @staticmethod
    @functools.cache
    def _fuzz_ratio(s1, s2):
        return fuzz.ratio(s1, s2)

    @override
    def dedupe(self, attr: str, /) -> frames:
        logger.debug(
            f'Deduping attribute "{attr}" with {self.__class__.__name__}'
            f"(tolerance={self._tolerance})"
        )

        frame_methods = self.frame_methods

        tmp_attr: str = attr + TMP_ATTR_LABEL

        uattrs = np.unique(frame_methods.get_col(attr))

        similarity_matrix = np.array(
            [[self._fuzz_ratio(s1, s2) for s1 in uattrs] for s2 in uattrs]
        )

        match_indices = np.where(similarity_matrix >= self._ratio)

        fuzzy_map = {uattrs[i]: uattrs[j] for i, j in zip(*match_indices)}

        attr_map = frame_methods.map_dict(attr, fuzzy_map)

        logger.debug(
            f'Assigning duplicated "{attr}" instances to attribute "{tmp_attr}"'
        )

        frame_methods.put_col(tmp_attr, attr_map)

        return self._assign_group_id(tmp_attr).drop_col(tmp_attr).frame

        # logger.debug(f"Finished grouping dupes of attribute {attr}")
        # return df
