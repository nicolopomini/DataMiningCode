from __future__ import absolute_import

from typing import List


class Tree:

    def __init__(self, key: str, fields: dict) -> None:
        self.key: str = key
        self.parent = None
        self.children = []
        self.fields = fields

    def add_child(self, child) -> None:
        self.children.append(child)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Tree):
            return False
        return self.key == o.key

    def __repr__(self) -> str:
        return "Tree(key: %s, parent: %s, #children: %d)" % (self.key, self.parent, len(self.children))

    def get_subtree(self) -> []:
        subtree = [self]
        for tree in self.children:
            subtree.extend(tree.get_subtree())
        return subtree


class TreeList:
    def __init__(self, trees: List[Tree]) -> None:
        self.trees: List[Tree] = trees

    @staticmethod
    def empty():
        return TreeList([])

    def add_tree(self, tree: Tree):
        self.trees.append(tree)

    def __repr__(self) -> str:
        return "TreeList %s" % str(self.trees)
