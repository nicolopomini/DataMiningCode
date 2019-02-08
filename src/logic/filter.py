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

    def get_first_n_frequents(self, n: int) -> List[PNode]:
        """
        Get the patterns that appear at least threshold times
        :return: a list of patterns
        """
        filtered_patterns = {}
        for pattern in self.counters:
            if self.counters[pattern] >= self.threshold:
                filtered_patterns[pattern] = self.counters[pattern]
        sorted_patterns = sorted(filtered_patterns.items(), key=lambda kv: kv[1])
        if n > 0:
            return sorted_patterns[-n:]
        else:
            return sorted_patterns

    def remove_empty(self):
        sorted_patterns = sorted(self.counters.items(), key=lambda kv: kv[1], reverse=True)
        for pattern, _ in sorted_patterns:
            if pattern.is_empty():
                self.counters.pop(pattern, None)

    def get_by_importance(self) -> list:
        sorted_patterns = sorted(self.counters.items(), reverse=True, key=lambda kv: len(kv[0].get_subtree()) * kv[1])
        return [(x, f) for x, f in sorted_patterns if f >= self.threshold]
