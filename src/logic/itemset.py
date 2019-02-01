from __future__ import absolute_import

from typing import List, Tuple
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import itertools as it

from models.itemset import RecordTree
from models.tree import TreeList
from models.tree import Tree
from models.tree import PNode
import copy


class ItemSetGenerator:
    """
    Incapsulation of the logic to create a list of item sets from a list of trees
    """
    def __init__(self, trees: TreeList, threshold: float = 0.6) -> None:
        self.trees = trees
        self.threshold = threshold

    def generate_record_trees(self) -> List[RecordTree]:
        i = 0
        for tree in self.trees.trees:
            for node in tree.get_subtree():
                for attribute in node.fields:
                    if "79138240b5924fd194a9cdea47754f7f" == node.fields[attribute]:
                        i = i + 1
        print("79138240b5924fd194a9cdea47754f7f  " + str(i))
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
        print(str(len(dataset)))
        i = 0
        for set in dataset:
            if "f74355ecb7ab46dcb554a87c32b0fe9c = 5318b1f2bc5e402f8a1c71396d2f1fe8" in set:
                i = i + 1
        print("f74355ecb7ab46dcb554a87c32b0fe9c = 5318b1f2bc5e402f8a1c71396d2f1fe8  " + str(i))
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
                ordered_sets: List[Tuple[str]] = list(it.permutations(list_set))
                for s in ordered_sets:
                    set_string = ','.join(s)
                    total = 0
                    for tree in self.trees.trees:
                        total += self.ordered_itemset_occourrences_in_tree(s, tree)
                    occourences[set_string] = total
        for o, v in occourences.items():
            if v > 1:
                print("" + o + ": " + str(v))

    def compute_patterns_by_node(self, node: Tree, original_nodes: List[Tree], global_patterns: List[PNode], patterns_to_expand: List[PNode] = []):
        parent = None
        for node_to_check in original_nodes:
            if node.parent == node_to_check.key:
                parent = node_to_check
        n_fields = len(node.fields)
        n_children = len(node.children)
        new_patterns = []
        new_nodes = []
        complete_patterns = []
        if n_fields != 0:
            if len(patterns_to_expand) > 0:
                node.patterns.append(patterns_to_expand)
            node.calls = node.calls + 1
            if node.calls >= n_children:
                for i in range(0, n_fields):
                    attributes_combinations = list(it.combinations(node.fields, i + 1))
                    for combination in attributes_combinations:
                        attributes = []
                        for value in combination:
                            attributes.append(value)
                        new_nodes.append(PNode(attributes))
                new_nodes.append(PNode([]))
                for single_node in new_nodes:
                    new_patterns.append(single_node)
                for i in range(0, n_children):
                    child_patterns_combinations = list(it.combinations(node.patterns, i + 1))
                    for child_combination in child_patterns_combinations:
                        if len(child_combination) >= 3:
                            print()
                        last_child_index = len(child_combination) - 1
                        child_combinator_index = []
                        child_combinator_size = []
                        for k in range(0, last_child_index + 1):
                            child_combinator_index.append(0)
                            child_combinator_size.append(len(child_combination[k]))
                        while child_combinator_index[0] < child_combinator_size[0]:
                            to_combine = []
                            for j in range(0, last_child_index + 1):
                                to_combine.append(child_combination[j][child_combinator_index[j]])
                            for to_attach in new_nodes:
                                to_attach_copy = copy.deepcopy(to_attach)
                                for z in range(0, last_child_index + 1):
                                    tree_copy = copy.deepcopy(to_combine[z])
                                    to_attach_copy.add_child(tree_copy)
                                    new_patterns.append(to_attach_copy)
                            child_combinator_index[last_child_index] = child_combinator_index[last_child_index] + 1
                            for z in range(last_child_index, 0, -1):
                                if (child_combinator_size[z] - child_combinator_index[z]) == 0:
                                    child_combinator_index[z] = 0
                                    child_combinator_index[z - 1] = child_combinator_index[z - 1] + 1
                complete_patterns.extend(new_patterns)
                for new_pattern in complete_patterns:
                    if len(new_pattern.children) >= 1:
                        global_patterns.append(copy.deepcopy(new_pattern))
                node.patterns = []
                if parent is not None:
                    self.compute_patterns_by_node(parent, original_nodes, global_patterns, complete_patterns)
        else:
            complete_patterns.append(PNode([]))
            if parent is not None:
                if len(patterns_to_expand) > 0:
                    for p in patterns_to_expand:
                        new_pattern = copy.deepcopy(p)
                        new_empty_node = PNode([])
                        new_empty_node.add_child(new_pattern)
                        complete_patterns.append(new_empty_node)
                patterns_to_expand.extend(complete_patterns)
                self.compute_patterns_by_node(parent, original_nodes, global_patterns, patterns_to_expand)