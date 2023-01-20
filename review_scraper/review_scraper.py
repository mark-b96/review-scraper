import time
import random
import requests
import json
from bs4 import BeautifulSoup
from loguru import logger
from typing import List, Dict


from review_scraper.urls import product_reviews

MAX_REVIEW_PAGES = 50
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}


class ReviewScraper:
    def __init__(self, website: str, reviews_per_page: int, data_handler_obj):
        self.website: str = website
        self.reviews_per_page: int = reviews_per_page
        self.data_handler_obj = data_handler_obj

    @staticmethod
    def get(url: str) -> requests.Response:
        return requests.get(url=url, headers=HEADERS)

    @staticmethod
    def delay(min_seconds: float = 1.3, max_seconds: float = 4.0) -> None:
        sleep_seconds = random.uniform(min_seconds, max_seconds)
        logger.info(sleep_seconds)
        time.sleep(sleep_seconds)

    def parse_json_reviews(
        self, review_dict: Dict[str, List], json_response: Dict
    ) -> bool:
        reviews = json_response["reviews"]
        is_last_page = False

        if len(reviews) < self.reviews_per_page:
            is_last_page = True

        for item in reviews:
            review_dict["title"].append(item["title"])
            review_dict["rating"].append(item["overallRating"]["value"])
            review_dict["content"].append(item["text"])
            review_dict["location"].append(item["reviewer"]["location"])

        return is_last_page

    def parse_html_reviews(
        self, response: requests.Response, review_dict: Dict[str, List]
    ) -> bool:
        html_response = BeautifulSoup(response.text, "html.parser")
        reviews = html_response.find_all("div", {"data-hook": "review"})
        is_last_page = False
        review_count = 0

        for item in reviews:

            item_title = item.find("a", {"data-hook": "review-title"})
            item_rating = item.find("i", {"data-hook": "review-star-rating"})
            item_text = item.find("span", {"data-hook": "review-body"})
            item_date = item.find("span", {"data-hook": "review-date"})

            if not item_title:
                item_title = item.find("span", {"data-hook": "review-title"})
            if not item_rating:
                item_rating = item.find("i", {"data-hook": "cmps-review-star-rating"})

            if not all([item_title, item_rating, item_text, item_date]):
                continue

            review_dict["title"].append(item_title.text.strip())
            review_dict["rating"].append(
                float(item_rating.text.replace("out of 5 stars", "").strip())
            )
            review_dict["content"].append(item_text.text.strip())
            review_dict["location"].append(item_date.text.strip())
            review_count += 1

        if review_count < self.reviews_per_page:
            is_last_page = True
        return is_last_page

    def parse_product_reviews(self, product_id: str) -> Dict[str, List]:
        review_dict = {"title": [], "location": [], "rating": [], "content": []}

        for page_num in range(1, MAX_REVIEW_PAGES):
            logger.info(f"Parsing page {page_num} of product id: {product_id}...")

            url = product_reviews[self.website]["scrape"].substitute(
                page_num=page_num, product_id=product_id
            )

            self.delay()
            response = self.get(url=url)

            if response.status_code != 200:
                logger.info(f"Invalid response {response.status_code}")
                continue

            response_type = response.headers.get("content-type")
            if "html" in response_type:
                is_last_page = self.parse_html_reviews(
                    response=response, review_dict=review_dict
                )
            elif "json" in response_type:
                json_response = json.loads(response.text)
                is_last_page = self.parse_json_reviews(
                    review_dict=review_dict, json_response=json_response
                )
            else:
                logger.error("Invalid response type")
                break

            if is_last_page:
                break
        return review_dict

    def scrape(self, product_ids: List[str]) -> None:
        assert self.website in product_reviews

        for product_id in product_ids:
            user_reviews_list = self.parse_product_reviews(product_id=product_id)
            self.data_handler_obj.save_to_excel(
                file_name=str(product_id), data=user_reviews_list
            )

    def search(self, search_term: str) -> None:
        assert self.website in product_reviews

        search_url = product_reviews[self.website]["search"]["url"]
        response = requests.get(f"{search_url}{search_term}", headers=HEADERS)
        html_response = BeautifulSoup(response.text, "html.parser")

        parsing_data = product_reviews[self.website]["search"]["parser"]
        find_all = parsing_data[0]
        selector, heading, name = find_all
        product_id_key = parsing_data[1][0]

        search_results = html_response.find_all(selector, {heading: name})
        product_asins = [result[product_id_key] for result in search_results]

        self.data_handler_obj.save_to_csv(
            file_name=f"{self.website}_{search_term}_asins",
            data=product_asins,
        )
