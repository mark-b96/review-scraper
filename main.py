import argparse

from review_scraper.review_scraper import ReviewScraper
from review_scraper.data_handler import DataHandler


def parse_arguments():
    a = argparse.ArgumentParser()
    a.add_argument(
        "-i",
        type=str,
        help="Input csv file",
        default="data/input/john_lewis_iphone_asins.csv",
    )
    a.add_argument(
        "-o",
        type=str,
        help="Output file path",
        default="data/output"
    )
    a.add_argument(
        "-w",
        type=str,
        help="Website to scrape",
        default="john_lewis"
    )
    a.add_argument(
        "-s",
        type=str,
        help="Search term",
        default="iphone"
    )
    return a.parse_args()


def main():
    args = parse_arguments()

    output_file_path = args.o
    website = args.w
    search_term = args.s

    data_handler_obj = DataHandler()
    review_scraper_obj = ReviewScraper(
        website=website, reviews_per_page=10, data_handler_obj=data_handler_obj
    )

    if search_term:
        search_term = search_term.strip().replace(" ", "+")
        review_scraper_obj.search(search_term=search_term)
    else:
        product_ids = data_handler_obj.read_product_asins(file_path=args.i)
        review_scraper_obj.scrape(
            product_ids=product_ids, output_file_path=output_file_path
        )


if __name__ == "__main__":
    main()