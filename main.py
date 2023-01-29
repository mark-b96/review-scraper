import argparse

from fake_useragent import FakeUserAgent

from review_scraper.review_scraper import ReviewScraper
from review_scraper.data_handler import DataHandler


def parse_arguments():
    a = argparse.ArgumentParser()
    a.add_argument("-i", type=str, required=True, help="Input csv file")
    return a.parse_args()


def main():
    args = parse_arguments()
    input_xlsx_file_path = args.i

    data_handler_obj = DataHandler()
    data_handler_obj.load_input_csv(file_path=input_xlsx_file_path)
    data_handler_obj.load_json_config(file_path="config/config.json")

    user_agent_obj = FakeUserAgent()

    review_scraper_obj = ReviewScraper(
        data_handler_obj=data_handler_obj, user_agent_obj=user_agent_obj
    )
    review_scraper_obj.scrape()


if __name__ == "__main__":
    main()
