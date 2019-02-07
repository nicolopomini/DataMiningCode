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
        print("Parsed trees!")
        itemset_generator = ItemSetGenerator(trees)
        itemsets = itemset_generator.itemset_mining()
        print("Computed itemsets!")
        trees.filter_attributes(itemsets)
        print("Filtered attributes!")
        i = 0
        for transaction in trees.trees:
            i = i + 1
            print("Tree " + str(i))
            print()
            transaction.print_tree()
            itemset_generator.compute_tree_recursion_limit(transaction)
            flat_tree = transaction.get_subtree()
            print()
            print(flat_tree)
            print("Computing patterns...")
            local_patterns: List[PNode] = []
            for node in flat_tree:
                if len(node.children) == 0:
                    patterns_to_expand: List[PNode] = []
                    itemset_generator.compute_patterns_by_node(node, flat_tree, local_patterns, patterns_to_expand)
            print("Computed patterns for tree " + str(i))
            print(len(local_patterns))
            print("Counting patterns...")
            self.filter.count_on_one_transaction(local_patterns)
            print("Counted patterns for tree " + str(i))
            print()


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