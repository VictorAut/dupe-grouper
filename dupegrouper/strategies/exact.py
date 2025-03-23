import logging
from typing_extensions import override

import pandas as pd

from dupegrouper.strategy import DeduplicationStrategy


# LOGGER:


logger = logging.getLogger(__name__)


# EXACT:


class Exact(DeduplicationStrategy):

    @override
    def dedupe(self, df: pd.DataFrame, attr: str, /) -> pd.DataFrame:
        logger.debug(f'Deduping attribute "{attr}" with {self.__class__.__name__}()')
        df = self._assign_group_id(df, attr)
        logger.debug(f"Finished grouping dupes of attribute {attr}")
        return df
