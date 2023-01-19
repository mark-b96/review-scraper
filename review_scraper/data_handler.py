import pandas as pd
from loguru import logger
from typing import List, Dict


class DataHandler:
    @staticmethod
    def save_to_excel(save_path: str, data: Dict[str, List]) -> None:
        logger.info(f"Saving data to {save_path}.xlsx")
        df = pd.DataFrame(data)
        df.to_excel(f"{save_path}.xlsx", index=False)

    @staticmethod
    def save_to_csv(save_path: str, data: List) -> None:
        logger.info(f"Saving data to {save_path}.csv")
        df = pd.DataFrame(data)
        file_path = f"{save_path}.csv"
        df.to_csv(file_path, index=False, header=False)

    @staticmethod
    def read_product_asins(file_path: str) -> List[str]:
        return pd.read_csv(file_path, header=None)[0].to_list()
