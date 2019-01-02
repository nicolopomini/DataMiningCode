from __future__ import absolute_import

from tree_for_generator import TreePattern
from values import ValueGenerator

class Gen:
    def __init__(self, total_trees: int, total_patterns: int, min_pattern_nodes: int, max_pattern_nodes: int, min_nodes: int, max_nodes: int) -> None:
        """
        Create a node that is part of a pattern
        :param total_patterns: the total number of patterns that will be used
        :param total_trees: the total number of trees that will be generated
        :param min_nodes: the minimum number of nodes a tree must have (no less than 2)
        :param max_nodes: the maximum number of nodes a tree can have
        """
        self.total_patterns: int = total_patterns
        self.min_nodes: int = min_nodes
        self.max_nodes: int = max_nodes
        if min_nodes <= 1:
            raise ValueError("There must be at least 2 nodes in a tree. Given %d" % min_nodes)

    def generateData(self) -> [TreePattern]:
        pass