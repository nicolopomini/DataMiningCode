from __future__ import absolute_import

import random
from typing import Dict, List


class TreePattern:
    def __init__(self, field: str, value: str) -> None:
        """
        Create a node that is part of a pattern
        :param field: name of the field included in the pattern
        :param value: value of the field included in the pattern
        Es: field: 'color', value: 'blue' means that the node contains a field 'color' = 'blue'
        """
        self.field: str = field
        self.value: str = value
        self.parent = None
        self.children = []

    def add_child(self, child) -> None:
        self.children.append(child)

    def __repr__(self) -> str:
        return "Node('%s' = %s)" % (self.field, self.value)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TreePattern):
            return False
        return self.field == o.field and self.value == o.value


class Pattern:
    @staticmethod
    def generate_pattern(length: int, fields: List[str], values: Dict[str, List[str]]) -> TreePattern:
        """
        Create a pattern, which is a tree
        :param length: length of the pattern, at least 1. It is the number of edges. Number of nodes: 1 + length
        :param fields: list of the field names
        :param values: list of values: {field_name => list of possible values}
        :return: the TreePattern, route of the pattern
        """
        if length < 1:
            raise ValueError("The length must be at least 1. Given %d" % length)
        # first, create all nodes
        nodes = []
        for i in range(1 + length):
            field_name = fields[random.randint(0, len(fields) - 1)]
            field_value = values[field_name][random.randint(0, len(values[field_name]) - 1)]
            node = TreePattern(field_name, field_value)
            nodes.append(node)
        # second, build the tree, choosing randomly where to append
        root: TreePattern = nodes[random.randint(0, len(nodes) - 1)]
        included = [root]
        nodes.remove(root)
        for _ in range(length):
            parent = included[random.randint(0, len(included) - 1)]
            child = nodes[random.randint(0, len(nodes) - 1)]
            parent.add_child(child)
            child.parent = parent
            included.append(child)
            nodes.remove(child)
        return root
