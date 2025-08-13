import csv
import random
import os

class CsvRead:

    def __init__(self, file):
        if not os.path.exists(file):
            raise FileNotFoundError(f"CSV file not found: {file}")

        with open(file, newline='', encoding='utf-8') as f:
            self.rows = list(csv.DictReader(f))

        if not self.rows:
            raise ValueError(f"No rows found in CSV: {file}")

    def read(self):
        return random.choice(self.rows)
