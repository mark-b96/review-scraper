import csv
import json

import pandas as pd
from loguru import logger
from pathlib import Path

from typing import List

CSV_HEADER_COLUMNS = [
    "id",
    "date",
    "title",
    "rating",
    "location",
    "verified",
    "content",
]


class DataHandler:
    def __init__(self):
        self.config = None
        self.input_data = None
        self.csv_writer, self.csv_file = None, None

    def load_json_config(self, file_path: str) -> None:
        with open(file_path) as f:
            self.config = json.load(f)

    def load_input_csv(self, file_path: str) -> None:
        input_xlsx = pd.read_csv(file_path)
        filtered_input_xlsx = input_xlsx[input_xlsx["Process"] == True]
        self.input_data = {
            "product_id": filtered_input_xlsx["Product ID"].tolist(),
            "website": filtered_input_xlsx["Website"].tolist(),
            "output_dir": filtered_input_xlsx["Output directory"].tolist(),
        }

    def init_output_csv(self, output_dir: str, file_name: str) -> None:
        output_path = Path(output_dir, f"{file_name}.csv")
        logger.info(f"Saving data to {output_path}")
        self.csv_file = open(output_path, "w")
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(CSV_HEADER_COLUMNS)

    def reviews_to_csv(self, parsed_reviews: List[str]) -> None:
        self.csv_writer.writerows(parsed_reviews)
        self.csv_file.flush()

    def close_csv_file(self):
        self.csv_file.close()
