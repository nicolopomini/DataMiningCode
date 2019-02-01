from __future__ import absolute_import

from unittest import TestCase

from logic.input import InputManager
from logic.itemset import ItemSetGenerator


class TestItemSet(TestCase):
    def test_pattern_rec(self):
        manager = InputManager()
        manager.read_input("test_itemsets.csv")
        trees = manager.build_tree()
        generator = ItemSetGenerator(trees)
        patterns = generator.itemset_mining()
        trees.filter_attributes(patterns)
        i = 0
        for tree in trees.trees:
            i = i + 1
            print("Tree " + str(i))
            print()
            tree.print_tree()
            flat_tree = tree.get_subtree()
            print(flat_tree)
            global_patterns = []
            for node in flat_tree:
                if len(node.children) == 0:
                    patterns_to_expand = []
                    generator.compute_patterns_by_node(node, flat_tree, global_patterns, patterns_to_expand)
            print()
            for node in global_patterns:
                node.print_tree()
                print()