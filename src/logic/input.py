from __future__ import absolute_import
import csv
from typing import Dict, List

from models.tree import TreeList, Tree


class RecordDetails:
    TRANSACTION_ID = "transaction_id"
    PARENT_ID = "parent_id"
    RECORD_ID = "record_id"


class InputManager:
    def __init__(self) -> None:
        self.records: Dict[str, Dict] = {}   # dict with rid -> whole record
        self.fields: Dict[str, List] = {}    # dict with name of the field -> list of all possible values
        self.field_positions: Dict[str, int] = {}  # dict with field name -> position
        self.position_field: Dict[int, str] = {}    # dict with position -> name of the field

    def read_input(self, input_file: str) -> None:
        with open(input_file) as input_cvs:
            read_csv = csv.reader(input_cvs)
            i = 0
            for row in read_csv:
                if i == 0:
                    j = 0
                    for field in row:
                        # prepare the dictionaries
                        self.field_positions[field] = j
                        self.position_field[j] = field
                        self.fields[field] = []
                        j += 1
                else:
                    record_key = row[self.field_positions[RecordDetails.RECORD_ID]]
                    record_dict = {}
                    for position in self.position_field:
                        key = self.position_field[position]
                        value = row[position] if row[position] != "None" else None  # just for root records
                        record_dict[key] = value
                        if value is not None and value not in self.fields[key]:
                            self.fields[key].append(value)
                    self.records[record_key] = record_dict
                i += 1

    def build_tree(self) -> TreeList:
        tree_list: TreeList = TreeList.empty()
        trees: Dict[str, Tree] = {}
        for rid in self.records:
            trees[rid] = Tree(rid, self.records[rid])
        for rid in self.records:
            if self.records[rid][RecordDetails.PARENT_ID] is None:
                tree_list.add_tree(trees[rid])
            else:
                parent_id = self.records[rid][RecordDetails.PARENT_ID]
                # set parent
                trees[rid].parent = parent_id
                # set child
                trees[parent_id].add_child(trees[rid])
        return tree_list
