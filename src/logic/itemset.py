from __future__ import absolute_import

from typing import List
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
    def __init__(self, trees: TreeList, threshold: float = 0.2) -> None:
        self.trees = trees
        self.threshold = threshold
        self.counter = 0

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
        print("Number of transactions: " + str(len(dataset)))
        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        frequent_itemsets = apriori(df, min_support=self.threshold, use_colnames=True)
        return [fi for fi in frequent_itemsets["itemsets"].tolist() if len(fi) > 1]

    def compute_tree_recursion_limit(self, node: Tree, parent: Tree = None):
        if len(node.fields) == 0:
            for child in node.children:
                self.compute_tree_recursion_limit(child, node)
        else:
            if parent is not None and len(parent.children) > 1:
                parent.stop = True
            else:
                node.stop = True

    def compute_patterns_by_node(self, node: Tree, original_nodes: List[Tree], global_patterns: List[PNode], patterns_to_expand: List[PNode] = None):
        if patterns_to_expand is None:
            patterns_to_expand = []
        parent = None
        if not node.stop:
            for node_to_check in original_nodes:
                if node.parent == node_to_check.key:
                    parent = node_to_check
        n_fields = len(node.fields)
        n_children = len(node.children)
        new_patterns = []
        new_nodes = []
        complete_patterns = []
        if len(patterns_to_expand) > 0:
            node.patterns.append(patterns_to_expand)
        node.calls = node.calls + 1
        if node.calls >= n_children:
            if n_fields != 0:
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
            else:
                new_patterns.append(PNode([]))
                new_nodes.append(PNode([]))
            for i in range(0, n_children):
                child_patterns_combinations = list(it.combinations(node.patterns, i + 1))
                for child_combination in child_patterns_combinations:
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
                if len(new_pattern.children) >= 1 or (len(new_pattern.children) == 0 and len(new_pattern.fields) >= 2):
                    global_patterns.append(copy.deepcopy(new_pattern))
            node.patterns = []
            if parent is not None:
                self.compute_patterns_by_node(parent, original_nodes, global_patterns, complete_patterns)


    def compute_simple_patterns_by_node(self, node: Tree, original_nodes: List[Tree], global_patterns: List[PNode], patterns_to_expand: List[PNode] = None):
        if patterns_to_expand is None:
            patterns_to_expand = []
        parent = None
        if not node.stop:
            for node_to_check in original_nodes:
                if node.parent == node_to_check.key:
                    parent = node_to_check
        n_fields = len(node.fields)
        n_children = len(node.children)
        new_patterns = []
        new_nodes = []
        complete_patterns = []
        if len(patterns_to_expand) > 0:
            node.patterns.append(patterns_to_expand)
        node.calls = node.calls + 1
        if node.calls >= n_children:
            if n_fields != 0:
                for i in range(0, n_fields):
                    attributes_combinations = list(it.combinations(node.fields, i + 1))
                    for combination in attributes_combinations:
                        attributes = []
                        for value in combination:
                            attributes.append(value)
                        new_nodes.append(PNode(attributes))
                for single_node in new_nodes:
                    new_patterns.append(single_node)
                for i in range(0, n_children):
                    child_patterns_combinations = list(it.combinations(node.patterns, i + 1))
                    for child_combination in child_patterns_combinations:
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
                    if len(new_pattern.fields) == 0:
                        print()
                    if len(new_pattern.children) >= 1 or (len(new_pattern.children) == 0 and len(new_pattern.fields) >= 2):
                        global_patterns.append(copy.deepcopy(new_pattern))
                node.patterns = []
                if parent is not None:
                    self.compute_simple_patterns_by_node(parent, original_nodes, global_patterns, complete_patterns)
            else:
                node.patterns = []
                if parent is not None:
                    self.compute_simple_patterns_by_node(parent, original_nodes, global_patterns, complete_patterns)