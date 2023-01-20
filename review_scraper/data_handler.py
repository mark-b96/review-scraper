import pandas as pd
from loguru import logger
from typing import List, Dict
from pathlib import Path


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

    @staticmethod
    def read_product_asins(file_path: str) -> List[str]:
        return pd.read_csv(file_path, header=None)[0].to_list()
