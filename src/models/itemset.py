from __future__ import absolute_import

from asyncio import Queue
from typing import List

from models.tree import Tree
from logic.input import RecordDetails


class RecordTreeNode:
    def __init__(self, node: Tree) -> None:
        self.strings: List[str] = []
        for field in node.fields:
            if field not in [RecordDetails.RECORD_ID, RecordDetails.TRANSACTION_ID, RecordDetails.PARENT_ID]:
                self.strings.append(str(field) + " = " + str(node.fields[field]))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, RecordTreeNode):
            return False
        return set(self.strings) == set(o.strings)

    def __hash__(self) -> int:
        return hash(frozenset(self.strings))

    def __repr__(self) -> str:
        return str(self.strings)


class RecordTree:
    """
    Representation of a tree as a list of strings (the fields of each record) and a distance (from the root node)
    """
    def __init__(self, transaction: Tree) -> None:
        """
        Transform a transaction into a decomposed lists of string and distances
        :param transaction:
        """
        self.fields: List[RecordTreeNode] = []
        self.distances: List[int] = []
        queue = Queue()
        queue.put_nowait((transaction, 0))
        while not queue.empty():
            node, length = queue.get_nowait()
            for child in node.children:
                queue.put_nowait((child, length + 1))
            self.fields.append(RecordTreeNode(node))
            self.distances.append(length)

    def get_node(self, index: int) -> (RecordTreeNode, int):
        """
        Get the i-th node of the tree
        :param index: index of the node, ordered as a BFS visit
        :return: the couple <list of fields as strings, distance from the root>
        """
        if index < 0 or index >= len(self.fields):
            raise ValueError("Invalid index. Given %d, max %d" % (index, len(self.fields)))
        return self.fields[index], self.distances[index]

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        if self._i == len(self.fields):
            raise StopIteration
        else:
            item = (self.fields[self._i], self.distances[self._i])
            self._i += 1
            return item
