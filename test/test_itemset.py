from __future__ import absolute_import

from unittest import TestCase

from logic.input import InputManager
from logic.itemset import ItemSetGenerator


class TestItemSet(TestCase):
    def test_item_set_generation(self):
        manager = InputManager()
        manager.read_input("output.csv")
        trees = manager.build_tree()
        generator = ItemSetGenerator(trees)
        patterns = generator.itemset_mining()
        trees.filter_attributes(patterns)
        for tree in trees.trees:
            for node in tree.get_subtree():
                print(node.fields)
