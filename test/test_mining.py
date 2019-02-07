from __future__ import absolute_import

from unittest import TestCase

from logic.manager import Manager


class TestItemSet(TestCase):
    def test_pattern_rec(self):
        manager = Manager("test_itemsets.csv", 5)
        manager.compute_mining()
        f_patterns = manager.filter.get_first_n_frequents(5)
        for pattern in f_patterns:
            print("Number of appearences: " + str(pattern[1]))
            print()
            pattern[0].print_tree()
            print()