from __future__ import absolute_import

import argparse
from typing import List

from logic.manager import Manager
from models.tree import PNode

argument_parser = argparse.ArgumentParser(description="Miner of frequent patterns in tree-like complex objects")
argument_parser.add_argument("-out", dest="output", type=str, help="Output file name (txt format)", action="store", default="output.txt")
argument_parser.add_argument("-in", dest="input", type=str, help="Input file name (csv format)", action="store", default="input.csv")
argument_parser.add_argument("-thr", dest="threshold", type=int, help="Minimum number of times a pattern has to appear", action="store", default=4)

args = argument_parser.parse_args()
if args.threshold < 1:
    raise ValueError("The threshold must be at least 1. Given %d" % args.threshold)

manager = Manager(args.input, args.threshold)
manager.compute_mining()
manager.filter.remove_empty()
patterns = manager.filter.get_by_importance()
with open(args.output, "w") as f_out:
    for pattern, freq in patterns:
        l = len(pattern.get_subtree())
        f_out.write("Pattern: frequency: %d, length: %d, importance: %d\n" % (freq, l, l * freq))
        f_out.write(pattern.get_string())
        f_out.write("\n\n")
