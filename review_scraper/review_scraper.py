import time
import random
import requests

from loguru import logger
from typing import Dict
from string import Template
from review_scraper.review import AmazonReviewParser, JohnLewisParser, BuyBuyBabyParser

PARSER_FACTORY = {
    "amazon": AmazonReviewParser(),
    "johnlewis": JohnLewisParser(),
    "buybuybaby": BuyBuyBabyParser(),
}


class ReviewScraper:
    def __init__(self, data_handler_obj, user_agent_obj):
        self.data_handler_obj = data_handler_obj
        self.user_agent_obj = user_agent_obj
        self.headers: Dict[str, str] = self.data_handler_obj.config["headers"]
        self.max_review_pages: int = self.data_handler_obj.config["max_review_pages"]
        self.min_delay, self.max_delay = self.data_handler_obj.config[
            "delay_between_requests"
        ]

    def get(self, url: str) -> requests.Response:
        try:
            return requests.get(url=url, headers=self.headers)
        except Exception as e:
            logger.debug(e)
            self.delay(120.0, 130.0)
            logger.info("Attempting to access server after delay")
            return requests.get(url=url, headers=self.headers)

    @staticmethod
    def delay(min_delay: float, max_delay: float) -> None:
        sleep_seconds = random.uniform(min_delay, max_delay)
        logger.info(sleep_seconds)
        time.sleep(sleep_seconds)

    def parse_product_reviews(
        self, product_id: str, website: str, output_dir: str
    ) -> None:
        website_config = self.data_handler_obj.config["websites"][website]["scrape"]
        self.data_handler_obj.init_output_csv(
            output_dir=output_dir, file_name=product_id
        )
        review_parser_obj = PARSER_FACTORY[website]
        reviews_per_page = website_config["reviews_per_page"]
        website_url = website_config["url"]
        self.headers["user-agent"] = self.user_agent_obj.random

        for page_num in range(1, self.max_review_pages):
            logger.info(f"Parsing page {page_num} of product id: {product_id}...")

            url = Template(website_url).substitute(
                page_num=page_num,
                product_id=product_id,
                reviews_per_page=reviews_per_page,
            )

            self.delay(min_delay=self.min_delay, max_delay=self.max_delay)
            response = self.get(url=url)

            if response.status_code != 200:
                logger.info(f"Invalid response {response.status_code}")
                continue

            parsed_reviews = review_parser_obj.parse_reviews(response)
            review_count = len(parsed_reviews)
            parsed_reviews = [
                list(review.__dict__.values()) for review in parsed_reviews
            ]

            self.data_handler_obj.reviews_to_csv(parsed_reviews=parsed_reviews)

            if review_count != reviews_per_page:
                break

    def scrape(self) -> None:
        product_ids = self.data_handler_obj.input_data["product_id"]
        websites = self.data_handler_obj.input_data["website"]
        output_dirs = self.data_handler_obj.input_data["output_dir"]

        for product_id, website, output_dir in zip(product_ids, websites, output_dirs):
            self.parse_product_reviews(
                product_id=product_id, website=website, output_dir=output_dir
            )
            self.data_handler_obj.close_csv_file()
