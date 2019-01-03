from __future__ import absolute_import

from unittest import TestCase

from tree import Tree


class TestTree(TestCase):
    def test_tree(self):
        root = Tree("root")
        child1 = Tree("1")
        child1.parent = root
        root.add_child(child1)
        child2 = Tree("2")
        child2.parent = root
        root.add_child(child2)
        child3 = Tree("3")
        child3.parent = root
        root.add_child(child3)
        self.assertEqual(len(root.children), 3)
