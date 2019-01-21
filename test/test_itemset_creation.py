from __future__ import absolute_import

from typing import List
from unittest import TestCase

from input import InputManager
from itemset import ItemSetTree


class TestItemset(TestCase):
    def test_itemset_creation(self):
        manager = InputManager()
        manager.read_input("test_itemsets.csv")
        trees = manager.build_tree()
        item_sets: List[ItemSetTree] = []
        for tree in trees.trees:
            item_sets.append(ItemSetTree(tree))
        self.assertEqual(len(item_sets), 2)
        for item_set in item_sets:
            self.assertEqual(len(item_set.item_sets), 4)
            # just for debug
            for attr, dist in item_set:
                print("%s %d" % (str(attr), dist))
