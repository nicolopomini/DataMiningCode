from __future__ import absolute_import

from typing import Dict, List

from models.tree import PNode


class Filter:
    """
    Class to count each pattern and filter the most frequents only
    """
    def __init__(self, threshold: int) -> None:
        self.threshold = threshold
        self.counters: Dict[PNode, int] = {}

    def count_on_one_transaction(self, patterns: List[PNode]) -> None:
        """
        Counts the patterns of a single transaction
        :param patterns: the list of patterns found in a transaction
        """
        for pattern in patterns:
            if pattern in self.counters:
                self.counters[pattern] += 1
            else:
                self.counters[pattern] = 1

    def get_frequents(self) -> List[PNode]:
        """
        Get the patterns that appear at least threshold times
        :return: a list of patterns
        """
        return [p for p in self.counters if self.counters[p] >= self.threshold]
