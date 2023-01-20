import pandas as pd
from loguru import logger
from typing import List, Dict
from pathlib import Path
from glob import glob


class DataHandler:
    def __init__(self, output_dir: str):
        self.output_dir: str = output_dir

    def save_to_excel(self, file_name: str, data: Dict[str, List]) -> None:
        file_path = Path(self.output_dir, f"{file_name}.xlsx")
        logger.info(f"Saving data to {file_path}")
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)

    def save_to_csv(self, file_name: str, data: List) -> None:
        file_path = Path(self.output_dir, f"{file_name}.csv")
        logger.info(f"Saving data to {file_path}")
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False, header=False)

    def read_product_asins(self, file_path: str) -> List[str]:
        processed_product_asins = [int(Path(asin).stem) for asin in glob(f"{self.output_dir}/*.xlsx")]
        input_product_asins = pd.read_csv(file_path, header=None)[0].to_list()
        return [asin for asin in input_product_asins if asin not in processed_product_asins]
