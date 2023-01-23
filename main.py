import argparse

from review_scraper.review_scraper import ReviewScraper
from review_scraper.data_handler import DataHandler


def parse_arguments():
    a = argparse.ArgumentParser()
    a.add_argument("-i", type=str, help="Input csv file")
    a.add_argument("-o", type=str, required=True, help="Output directory path")
    a.add_argument("-w", type=str, required=True, help="Website to scrape")
    a.add_argument("-s", type=str, help="Search term")
    return a.parse_args()


def main():
    args = parse_arguments()

    output_dir = args.o
    website = args.w
    search_term = args.s

    data_handler_obj = DataHandler(output_dir=output_dir)
    data_handler_obj.load_config(file_path="config/config.json")
    review_scraper_obj = ReviewScraper(
        website=website, data_handler_obj=data_handler_obj
    )

    if search_term:
        review_scraper_obj.search(search_term=search_term)
    else:
        product_ids = data_handler_obj.read_product_asins(file_path=args.i)
        review_scraper_obj.scrape(product_ids=product_ids)


if __name__ == "__main__":
    main()
