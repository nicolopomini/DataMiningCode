from __future__ import absolute_import

from asyncio import Queue
from typing import List

from models.tree import Tree


class ItemSetNode:
    def __init__(self, node: Tree) -> None:
        self.strings: List[str] = []
        for field in node.fields:
            self.strings.append(str(field) + " = " + str(node.fields[field]))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, ItemSetNode):
            return False
        return set(self.strings) == set(o.strings)

    def __hash__(self) -> int:
        return hash(set(self.strings))

    def __repr__(self) -> str:
        return str(self.strings)


class ItemSetTree:
    def __init__(self, transaction: Tree) -> None:
        self.item_sets: List[ItemSetNode] = []
        self.distances: List[int] = []
        queue = Queue()
        queue.put_nowait((transaction, 0))
        while not queue.empty():
            node, length = queue.get_nowait()
            for child in node.children:
                queue.put_nowait((child, length + 1))
            self.item_sets.append(ItemSetNode(node))
            self.distances.append(length)

    def get_itemset(self, index: int) -> (ItemSetNode, int):
        if index < 0 or index >= len(self.item_sets):
            raise ValueError("Invalid index. Given %d, max %d" % (index, len(self.item_sets)))
        return self.item_sets[index], self.distances[index]

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        if self._i == len(self.item_sets):
            raise StopIteration
        else:
            item = (self.item_sets[self._i], self.distances[self._i])
            self._i += 1
            return item
