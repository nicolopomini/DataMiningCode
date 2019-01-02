from __future__ import absolute_import

from tree_for_generator import TreePattern
from values import ValueGenerator

class Gen:
    def __init__(self, total_trees: int, total_patterns: int, min_pattern_nodes: int, max_pattern_nodes: int, min_nodes: int, max_nodes: int) -> None:
        """
        Create a node that is part of a pattern
        :param total_trees: the total number of trees that will be generated
        :param total_patterns: the total number of patterns that will be used
        :param min_pattern_nodes the minimum number of nodes a pattern must have
        :param min_pattern_nodes the maximum number of nodes a pattern can have (must be smaller than max_nodes)
        :param min_nodes: the minimum number of nodes a tree must have (no less than 2)
        :param max_nodes: the maximum number of nodes a tree can have
        """
        self.total_patterns: int = total_patterns
        self.min_nodes: int = min_nodes
        self.max_nodes: int = max_nodes
        if total_trees < 1:
            raise ValueError("There must be at least one tree. Given %d" % total_trees)
        if min_nodes <= 1:
            raise ValueError("There must be at least 2 nodes in a tree. Given %d" % min_nodes)
        if min_pattern_nodes <= 1:
            raise ValueError("There must be at least 2 nodes in a pattern. Given %d" % min_pattern_nodes)
        if min_pattern_nodes > max_pattern_nodes:
            raise ValueError("The minimum number of nodes in each pattern must be "
                             "smaller than the maximum number of nodes in each pattern. "
                             "Given min_pattern_nodes %d and max_pattern_nodes %d" % min_pattern_nodes, max_pattern_nodes)
        if min_nodes > max_nodes:
            raise ValueError("The minimum number of nodes in each tree must be "
                             "smaller than the maximum number of nodes in each tree. "
                             "Given min_nodes %d and max_nodes %d" % min_nodes, max_nodes)
        if max_nodes < max_pattern_nodes:
            raise ValueError("The maximum number of nodes in each tree must "
                             "be greater than the maximum number of nodes in each pattern."
                             " Given max_nodes %d and max_pattern_nodes %d" % max_nodes, max_pattern_nodes)

    def generateData(self) -> [TreePattern]:
        pass