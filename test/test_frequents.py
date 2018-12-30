from __future__ import absolute_import

from unittest import TestCase

from src.frequents import FrequentCounter
from src.input import InputManager


class TestFrequents(TestCase):
    def test_single_appearances(self):
        manager = InputManager()
        manager.read_input("test_input_file.csv")
        frequent_counter = FrequentCounter(manager, threshold=1)
        single_counters = frequent_counter.count_single_appearances()
        print(single_counters)
        self.assertEqual(len(single_counters), 1)
