from __future__ import absolute_import

from typing import List
from typing import Dict
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import itertools as it

from models.itemset import RecordTree
from models.tree import TreeList
from models.tree import Tree


class ItemSetGenerator:
    """
    Incapsulation of the logic to create a list of item sets from a list of trees
    """
    def __init__(self, trees: TreeList, threshold: float = 0.5) -> None:
        self.trees = trees
        self.threshold = threshold

    def generate_record_trees(self) -> List[RecordTree]:
        return [RecordTree(t) for t in self.trees.trees]

    def itemset_mining(self, decomposed_trees: List[RecordTree] = None) -> List[frozenset]:
        if decomposed_trees is None:
            decomposed_trees = self.generate_record_trees()
        dataset = []
        for tree in decomposed_trees:
            field_list = []
            for node, dist in tree:
                field_list.extend(node.strings)
            dataset.append(field_list)
        print(dataset)
        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        frequent_itemsets = apriori(df, min_support=self.threshold, use_colnames=True)
        return [fi for fi in frequent_itemsets["itemsets"].tolist() if len(fi) > 1]

    def scan_forest_for_patterns(self, frequent_itemsets: List[frozenset]):
        occourences = dict()
        for itemset in frequent_itemsets:
            if len(itemset) <= 3:
                list_set = list(itemset)
                ordered_sets = list(it.permutations(list_set))
                for set in ordered_sets:
                    set_string = ','.join(set)
                    sum = 0
                    for tree in self.trees.trees:
                        sum = sum + self.ordered_itemset_occourrences_in_tree(set, tree)
                    occourences[set_string] = sum
        for o, v in occourences.items():
            if v > 1:
                print("" + o + ": " + str(v))

    def ordered_itemset_occourrences_in_tree(self, frequent_itemset: List[str], tree: Tree, next_item_index: int = 0) -> int:
        values = []
        occourences = 0
        for field in list(tree.fields.keys()):
            if field not in ["tid", "rid", "parent"]:
                values.append(field + " = " + tree.fields[field])
        if frequent_itemset[next_item_index] in values:
            if next_item_index == len(frequent_itemset) - 1:
                next_item_index = -1
                occourences = occourences + 1
            next_item_index = next_item_index + 1
        else:
            next_item_index = 0
        for child in tree.children:
            occourences = occourences + ItemSetGenerator.ordered_itemset_occourrences_in_tree(self, frequent_itemset, child, next_item_index)
        return occourences