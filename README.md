# review-scraper
Python script capable of obtaining product reviews from retailer websites.

## Requirements
* Python3.5+

## Installation
1. Clone the repository: `git clone git@github.com:mark-b96/review-scraper.git` (or download the ZIP)
2. Navigate to the project folder: `cd review-scraper`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate virtual environment: `source venv/bin/activate`
5. Install requirements: `pip install -r requirements.txt`

## Usage
### Search
`python3 main.py -s iphone -o ~/Documents/product_reviews/input/ -w amazon`

Product asins will be output to a `csv` in `~/Documents/product_reviews/input/`
### Scrape
`python3 main.py -i ~/Documents/product_reviews/input/amazon_iphone_asins.csv -o ~/Documents/product_reviews/output -w amazon`

Reviews will be output to an `xlsx` in `~/Documents/product_reviews/output/`

| Argument | Description |
| :----:| :------: |
| -i | Input csv product asin file | 
| -o | Output directory            |
| -w | Website to scrape (Must be in `config/config.json` file) |

### Sample Input
```
6345513
```
### Sample Output
```
title	                location rating  content
A good looking product	Oxford	      5	 I only purchased a new phone because my old one has various problems.  I chose blue and love all the new features and the size and weight of my new phone.  And a good price for a fabulous product.  xx

```

## Supported websites
* amazon.co.uk
* johnlewis.com