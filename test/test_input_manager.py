from __future__ import absolute_import

from unittest import TestCase

from input import InputManager


class TestInputManager(TestCase):
    def test_input_read(self):
        manager = InputManager()
        manager.read_input("test_input_file.csv")
        self.assertEqual(len(manager.records), 2)
        self.assertEqual(len(manager.field_positions), len(manager.position_field))

    def test_trees_builder(self):
        manager = InputManager()
        manager.read_input("test_input_file.csv")
        trees = manager.build_tree()
        self.assertEqual(len(trees.trees), 1)
        self.assertEqual(len(trees.trees[0].children), 1)
