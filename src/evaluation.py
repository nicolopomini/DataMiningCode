from __future__ import absolute_import

import time

from logic.manager import Manager, BaselineManager

print("Our implementation")
s1 = time.time()
manager = Manager("test.csv", 2)
manager.compute_mining()
manager.filter.remove_empty()
fp = set([x for x, _ in manager.filter.get_by_importance()])
f1 = time.time()

print("Baseline")
s2 = time.time()
manager = BaselineManager("test.csv", 2)
manager.compute_mining()
manager.filter.remove_empty()
fp1 = set([x for x, _ in manager.filter.get_by_importance()])
f2 = time.time()

print("time1: %f" % (f1 - s1))
print("time2: %f" % (f2 - s2))
print(len(fp))
print(len(fp1))
