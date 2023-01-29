import json
import requests

from abc import ABC, abstractmethod
from loguru import logger
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List
from googletrans import Translator


@dataclass
class Review:
    id: str
    date: str
    title: str
    rating: str
    location: str
    verified: str
    content: str


class ReviewParser(ABC):
    def __init__(self):
        self.translator = Translator()

    @abstractmethod
    def parse_reviews(self, response: requests.Response) -> List[Review]:
        raise NotImplementedError


class AmazonReviewParser(ReviewParser):
    def parse_reviews(self, response: requests.Response) -> List[Review]:
        html_response = BeautifulSoup(response.text, "html.parser")
        reviews = html_response.find_all("div", {"data-hook": "review"})
        parsed_reviews: List[Review] = []

        for review in reviews:
            is_international_review = False
            review_id = review.attrs["id"]
            review_title = review.find("a", {"data-hook": "review-title"})
            review_rating = review.find("i", {"data-hook": "review-star-rating"})
            review_content = review.find("span", {"data-hook": "review-body"})
            review_date = review.find("span", {"data-hook": "review-date"})
            review_verified = review.find("span", {"data-hook": "avp-badge"})

            if not review_title:
                review_title = review.find("span", {"data-hook": "review-title"})
                is_international_review = True
            if not review_rating:
                review_rating = review.find(
                    "i", {"data-hook": "cmps-review-star-rating"}
                )

            if not all([review_title, review_rating, review_content, review_date]):
                continue

            if review_id == "R3VJODDHGUE5HO":
                print("")

            review_date = review_date.text.strip().replace("Reviewed in", "")
            review_location, review_date = review_date.split("on")
            review_location = review_location.replace("the", "")
            review_location = (
                str(review_location.encode("utf-8"))
                .split("\\")[0]
                .replace("b'", "")
                .strip()
            )
            review_content = review_content.text.strip()

            if is_international_review and review_content:
                try:
                    review_content = self.translator.translate(review_content).text
                except Exception as e:
                    logger.error("Unable to translate review")
                    logger.error(e)

            review_obj = Review(
                id=review_id,
                date=review_date.strip(),
                title=review_title.text.strip(),
                rating=str(
                    float(review_rating.text.replace("out of 5 stars", "").strip())
                ),
                content=review_content,
                location=review_location,
                verified="TRUE" if review_verified else "FALSE",
            )
            parsed_reviews.append(review_obj)

        return parsed_reviews


class JohnLewisParser(ReviewParser):
    def parse_reviews(self, response: requests.Response) -> List[Review]:
        json_response = json.loads(response.text)
        reviews = json_response["reviews"]
        parsed_reviews: List[Review] = []

        for review in reviews:
            is_verified = "isVerifiedBuyer" in review["tags"]
            review_obj = Review(
                id=review["id"],
                date=review["date"],
                title=review["title"],
                rating=review["overallRating"]["value"],
                content=review["text"],
                location=review["reviewer"]["location"],
                verified="TRUE" if is_verified else "FALSE",
            )
            parsed_reviews.append(review_obj)
        return parsed_reviews


class BuyBuyBabyParser(ReviewParser):
    def parse_reviews(self, response: requests.Response) -> List[Review]:
        json_response = json.loads(response.text)
        row_count = json_response["TotalResults"]
        url = response.request.url
        url = url.replace("rows=8", f"rows={row_count}")
        updated_response = requests.get(url, headers=response.request.headers)
        json_response = json.loads(updated_response.text)
        reviews = json_response["Results"]
        parsed_reviews: List[Review] = []

        for review in reviews:
            is_verified = review["VerifiedPurchaser"]
            review_date = review["SubmissionTime"].split("T")[0].strip()
            review_obj = Review(
                id=review["id"],
                date=review_date,
                title=review.get("Title", " "),
                rating=review["Rating"],
                content=review["ReviewText"],
                location="",
                verified="TRUE" if is_verified else "FALSE",
            )
            parsed_reviews.append(review_obj)
        return parsed_reviews
