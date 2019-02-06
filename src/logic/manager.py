from __future__ import absolute_import

from typing import List

from logic.filter import Filter
from logic.input import InputManager
from logic.itemset import ItemSetGenerator
from models.tree import PNode


class Manager:
    def __init__(self, filename: str, threshold: int) -> None:
        self.filename = filename
        self.threshold = threshold
        self.filter = Filter(self.threshold)

    def get_frequent_patterns(self) -> List[PNode]:
        return self.filter.get_frequents()

    def compute_mining(self) -> None:
        manager = InputManager()
        manager.read_input(self.filename)
        trees = manager.build_tree()
        itemset_generator = ItemSetGenerator(trees)
        itemsets = itemset_generator.itemset_mining()
        trees.filter_attributes(itemsets)

        for transaction in trees.trees:
            flat_tree = transaction.get_subtree()
            local_patterns: List[PNode] = []
            for node in flat_tree:
                if len(node.children) == 0:
                    patterns_to_expand: List[PNode] = []
                    itemset_generator.compute_patterns_by_node(node, flat_tree, local_patterns, patterns_to_expand)
                    self.filter.count_on_one_transaction(local_patterns)


class BaselineManager(Manager):
    def compute_mining(self) -> None:
        manager = InputManager()
        manager.read_input(self.filename)
        trees = manager.build_tree()
        itemset_generator = ItemSetGenerator(trees)

        for transaction in trees.trees:
            flat_tree = transaction.get_subtree()
            local_patterns: List[PNode] = []
            for node in flat_tree:
                if len(node.children) == 0:
                    patterns_to_expand: List[PNode] = []
                    itemset_generator.compute_patterns_by_node(node, flat_tree, local_patterns, patterns_to_expand)
                    self.filter.count_on_one_transaction(local_patterns)