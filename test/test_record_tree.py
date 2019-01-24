from __future__ import absolute_import

from unittest import TestCase

from logic.input import InputManager
from logic.itemset import ItemSetGenerator


class TestRecordTree(TestCase):
    def test_itemset_creation(self):
        manager = InputManager()
        manager.read_input("test_itemsets.csv")
        trees = manager.build_tree()
        generator = ItemSetGenerator(trees)
        record_trees = generator.generate_record_trees()
        self.assertEqual(len(record_trees), 2)
        for record_tree in record_trees:
            self.assertEqual(len(record_tree.fields), 4)
            # just for debug
            for attr, dist in record_tree:
                print("%s %d" % (str(attr), dist))
