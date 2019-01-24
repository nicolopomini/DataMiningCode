from __future__ import absolute_import

from unittest import TestCase

from logic.input import InputManager
from logic.itemset import ItemSetGenerator


class TestItemSet(TestCase):
    def test_item_set_generation(self):
        manager = InputManager()
        manager.read_input("test_itemsets.csv")
        trees = manager.build_tree()
        generator = ItemSetGenerator(trees)
        patterns = generator.itemset_mining()
        print(patterns)