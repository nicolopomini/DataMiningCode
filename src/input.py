from __future__ import absolute_import
import csv


class InputManager:
    TRANSACTION_ID = "tid"
    PARENT_ID = "parent"
    RECORD_ID = "rid"

    def __init__(self) -> None:
        self.records = {}   # dict with rid -> whole record
        self.fields = {}    # dict with name of the field -> list of all possible values
        self.field_positions = {}  # dict with field name -> position
        self.position_field = {}    # dict with position -> name of the field

    def read_input(self, input_file):
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
                    record_key = row[self.field_positions[InputManager.RECORD_ID]]
                    record_dict = {}
                    for position in self.position_field:
                        key = self.position_field[position]
                        value = row[position] if row[position] != "" else None  # just for root records
                        record_dict[key] = value
                        if value is not None and value not in self.fields[key]:
                            self.fields[key].append(value)
                    self.records[record_key] = record_dict
                i += 1
