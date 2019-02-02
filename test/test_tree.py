from __future__ import absolute_import

from unittest import TestCase

from models.tree import Tree, PNode


class TestTree(TestCase):
    def test_tree(self):
        root = Tree("root", {})
        child1 = Tree("1", {})
        child1.parent = root
        root.add_child(child1)
        child2 = Tree("2", {})
        child2.parent = root
        root.add_child(child2)
        child3 = Tree("3", {})
        child3.parent = root
        root.add_child(child3)
        self.assertEqual(len(root.children), 3)
        self.assertEqual(len(root.get_subtree()), 4)


class TestPNode(TestCase):
    def test_comparison(self):
        n11 = PNode(["a"])
        n12 = PNode(["b"])
        n13 = PNode(["c"])
        n14 = PNode(["d"])
        n11.add_child(n12)
        n11.add_child(n13)
        n12.add_child(n14)

        n21 = PNode(["a"])
        n22 = PNode(["c"])
        n23 = PNode(["b"])
        n24 = PNode(["d"])
        n21.add_child(n22)
        n21.add_child(n23)
        n23.add_child(n24)

        self.assertEqual(n11, n21)
        self.assertEqual(hash(n11), hash(n21))
