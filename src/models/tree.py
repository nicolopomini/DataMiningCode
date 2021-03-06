from __future__ import absolute_import

from typing import List


class PNode:

    def __init__(self, fields: List[str]):
        self.parent = None
        self.children = []
        self.fields = fields

    def add_child(self, child) -> None:
        self.children.append(child)
        child.parent = self

    def print_tree(self, tabs: int = 0) -> None:
        print(self.__repr__())
        for child in self.children:
            for _ in range(tabs + 1):
                print("\t", end="")
            child.print_tree(tabs + 1)

    def get_string(self, tab: int = 0) -> str:
        node = ""
        for _ in range(tab):
            node += "\t"
        node += "Node" + str(self.fields)
        for n in self.children:
            node += "\n" + n.get_string(tab=tab + 1)
        return node

    def __repr__(self) -> str:
        return "values: %s" % self.fields

    def __eq__(self, o: object) -> bool:
        if o is None or not isinstance(o, PNode):
            return False
        return set(self.fields) == set(o.fields) and set(self.children) == set(o.children) and len(self.get_subtree()) == len(o.get_subtree())

    def __hash__(self) -> int:
        return hash((frozenset(self.fields), frozenset(self.children), len(self.get_subtree())))

    def is_empty(self) -> bool:
        empty = True
        if len(self.fields) < 1:
            for child in self.children:
                empty = empty and child.is_empty()
        else:
            empty = False
        return empty

    def get_subtree(self) -> []:
        subtree = [self]
        for tree in self.children:
            subtree.extend(tree.get_subtree())
        return subtree


class Tree:

    def __init__(self, key: str, fields: dict) -> None:
        self.key: str = key
        self.parent = None
        self.children = []
        self.fields = fields
        self.calls = 0
        self.patterns = []
        self.stop = False

    def add_child(self, child) -> None:
        self.children.append(child)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Tree):
            return False
        return self.key == o.key

    def __repr__(self) -> str:
        return "Tree(key: %s, parent: %s, #children: %d, values: %s)" % (self.key, self.parent, len(self.children), self.fields)

    def get_subtree(self) -> []:
        subtree = [self]
        for tree in self.children:
            subtree.extend(tree.get_subtree())
        return subtree

    def print_tree(self, tabs: int = 0) -> None:
        print(self.__repr__())
        for child in self.children:
            for _ in range(tabs+1):
                print("\t", end="")
            child.print_tree(tabs + 1)

    def filter_attributes(self, attributes: List[frozenset]):
        self.filter_node_info()
        attributes_list = []
        for att in attributes:
            attributes_list.extend(list(att))
        attributes_complete_set = frozenset(attributes_list)
        for node in self.get_subtree():
            field_value_list = []
            for field in node.fields:
                field_value_list.append(str(field) + " = " + str(node.fields[field]))
            field_value_set = frozenset(field_value_list).intersection(attributes_complete_set)
            node.fields = list(field_value_set)

    def filter_node_info(self):
        for node in self.get_subtree():
            node.fields.pop("transaction_id")
            node.fields.pop("record_id")
            node.fields.pop("parent_id")

    def filter_baseline_node_info(self):
        for node in self.get_subtree():
            node.fields.pop("transaction_id")
            node.fields.pop("record_id")
            node.fields.pop("parent_id")
            field_value_list = []
            for field in node.fields:
                field_value_list.append(str(field) + " = " + str(node.fields[field]))
            node.fields = list(frozenset(field_value_list))


class TreeList:
    def __init__(self, trees: List[Tree]) -> None:
        self.trees: List[Tree] = trees

    @staticmethod
    def empty():
        return TreeList([])

    def add_tree(self, tree: Tree):
        self.trees.append(tree)

    def filter_attributes(self, attributes: List[frozenset]):
        for tree in self.trees:
            tree.filter_attributes(attributes)

    def filter_baseline_node_info(self):
        for tree in self.trees:
            tree.filter_baseline_node_info()

    def __repr__(self) -> str:
        return "TreeList %s" % str(self.trees)
