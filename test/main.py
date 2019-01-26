from __future__ import absolute_import

from logic.input import InputManager
from logic.itemset import ItemSetGenerator
from logic.frequents import FrequentCounter

manager = InputManager()
manager.read_input("test_itemsets.csv")
trees = manager.build_tree()
generator = ItemSetGenerator(trees)
patterns = generator.itemset_mining()
frequent_counter = FrequentCounter(manager, threshold=1)
print(patterns[0])
generator.scan_forest_for_patterns(patterns)