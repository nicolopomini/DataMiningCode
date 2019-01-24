from __future__ import absolute_import

from typing import List
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

from models.itemset import RecordTree
from models.tree import TreeList


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
