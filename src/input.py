from __future__ import absolute_import
import csv
from typing import Dict, List


class RecordDetails:
    TRANSACTION_ID = "tid"
    PARENT_ID = "parent"
    RECORD_ID = "rid"


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
                        value = row[position] if row[position] != "" else None  # just for root records
                        record_dict[key] = value
                        if value is not None and value not in self.fields[key]:
                            self.fields[key].append(value)
                    self.records[record_key] = record_dict
                i += 1
