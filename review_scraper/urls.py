from string import Template

product_reviews = {
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
