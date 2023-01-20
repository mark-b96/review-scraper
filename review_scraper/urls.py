from string import Template

websites = {
    "amazon": {
        "scrape": Template(
            "https://www.amazon.co.uk/product-reviews/$product_id/"
            "ref=cm_cr_getr_d_paging_btm_next_$page_num"
            "?ie=UTF8&reviewerType=all_reviews&pageNumber=$page_num"
        ),
        "search": {
            "url": "https://www.amazon.co.uk/s?k=",
            "parser": [
                ["div", "data-component-type", "s-search-result"],
                ["data-asin"],
            ],
        },
    },
    "john_lewis": {
        "scrape": Template(
            "https://api.johnlewis.com/ratings-reviews/v1/"
            "reviews?productId=$product_id&pageNumber=$page_num&pageSize=25"
            "&sort=newest&api_key=AIzaSyD0XVOmTWbXYigofMbhS9cSeG76BwQisO8"
        ),
        "search": {
            "url": "https://www.johnlewis.com/search?search-term=",
            "parser": [["article", "data-test", "product-card"], ["data-product-id"]],
        },
    },
}

headers = {
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/"
              "*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-dest": "document",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
}