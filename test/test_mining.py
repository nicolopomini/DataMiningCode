from __future__ import absolute_import

from unittest import TestCase

from logic.manager import Manager
from models.tree import PNode


class TestItemSet(TestCase):
    def test_pattern_rec(self):
        to_find1 = PNode(['06b7bde2b5eb49efb00dc260edfd1bae = 1ec1b7ccd60a444d99e16cf4ce5021be',
                          'a71fb85d222b4d30819d8b442a6ab945 = 3b5ed2de66fc4892a9508e150c118941'])
        to_find1.add_child(PNode(['06b7bde2b5eb49efb00dc260edfd1bae = 92d3476104de4b06bd1a38573f07a5d7']))
        to_find2 = PNode(['a71fb85d222b4d30819d8b442a6ab945 = b2c04646744240568e66f9c13e434476'])
        to_find2.add_child(PNode(['06b7bde2b5eb49efb00dc260edfd1bae = 781831ce63d046da9b217b606aff5f45',
                                  'a71fb85d222b4d30819d8b442a6ab945 = fc3c2abfc9304942bccf089977cacc16']))
        to_find2.children[0].add_child(PNode(['a71fb85d222b4d30819d8b442a6ab945 = f9bfbd58d8764011b9266d06c00b84f5']))
        thr = 5
        top = 10
        manager = Manager("test_itemsets.csv", thr)
        manager.compute_mining()
        manager.filter.remove_empty()
        f_patterns = manager.filter.get_first_n_frequents(top)
        if top != -1:
            print("LISTING TOP " + str(top) + " PATTERNS threshold = " + str(thr))
        else:
            print("LISTING ALL FREQUENT PATTERNS threshold = " + str(thr))
        print()
        for pattern in f_patterns:
            print("Number of appearences: " + str(pattern[1]))
            print()
            pattern[0].print_tree()
            print()
        if to_find1 in manager.filter.counters:
            print("Pattern")
            print()
            to_find1.print_tree()
            print()
            print("Appeared " + str(manager.filter.counters[to_find1]) + " times")
        if to_find2 in manager.filter.counters:
            print("Pattern")
            print()
            to_find2.print_tree()
            print()
            print("Appeared " + str(manager.filter.counters[to_find2]) + " times")
