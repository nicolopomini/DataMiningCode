from __future__ import absolute_import

from typing import Dict

from logic.input import InputManager


class FrequentCounter:
    def __init__(self, input_manager: InputManager, threshold: int = 1) -> None:
        self.input_manager: InputManager = input_manager
        self.threshold: int = threshold

    def count_single_appearances(self) -> dict:
        # attr, value => counter
        single_counter: Dict[(str, str), int] = {}      # (name of the field, value of the field) => counter
        # first, all couples = 0
        for field in self.input_manager.fields:
            for value in self.input_manager.fields[field]:
                single_counter[(field, value)] = 0
        # count the occurrence of each couple
        for _, v in self.input_manager.records.items():
            for field in v:
                if v[field] is not None:
                    single_counter[(field, v[field])] += 1
        # pruning values that appear less than the threshold, saving the frequent value in a new dictionary
        # to avoid runtime error for dict resizing
        final_counters: Dict[(str, str), int] = {}
        for k in single_counter:
            if single_counter[k] > self.threshold:
                final_counters[k] = single_counter[k]
        return final_counters
