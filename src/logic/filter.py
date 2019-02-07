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
        #debug variable
        self.test_node = PNode([])
        self.test_node.add_child(PNode(['b = c']))
        self.test_node.add_child(PNode([]))

    def count_on_one_transaction(self, patterns: List[PNode]) -> None:
        """
        Counts the patterns of a single transaction
        :param patterns: the list of patterns found in a transaction
        """
        for pattern in patterns:
            if pattern in self.counters:
                if pattern in [self.test_node]:
                    # debug prints
                    '''
                    self.test_node.print_tree()
                    print()
                    print("equals")
                    print()
                    pattern.print_tree()
                    print()
                    '''
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
        for pattern in sorted_patterns:
            if pattern[0].is_empty():
                self.counters.pop(pattern[0], None)