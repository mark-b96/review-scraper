import argparse

from review_scraper.review_scraper import ReviewScraper
from review_scraper.data_handler import DataHandler


def parse_arguments():
    a = argparse.ArgumentParser()
    a.add_argument(
        "-i",
        type=str,
        help="Input csv file",
        default="/home/mark/Documents/product_reviews/input/john_lewis_iphone_asins.csv",
    )
    a.add_argument(
        "-o",
        type=str,
        help="Output directory path",
        default="/home/mark/Documents/product_reviews/output",
    )
    a.add_argument("-w", type=str, help="Website to scrape", default="john_lewis")
    a.add_argument("-s", type=str, help="Search term", default="")
    return a.parse_args()


def main():
    args = parse_arguments()

    output_dir = args.o
    website = args.w
    search_term = args.s

    data_handler_obj = DataHandler(output_dir=output_dir)
    review_scraper_obj = ReviewScraper(
        website=website, reviews_per_page=10, data_handler_obj=data_handler_obj
    )

    if search_term:
        search_term = search_term.strip().replace(" ", "+")
        review_scraper_obj.search(search_term=search_term)
    else:
        product_ids = data_handler_obj.read_product_asins(file_path=args.i)
        review_scraper_obj.scrape(product_ids=product_ids)


if __name__ == "__main__":
    main()
