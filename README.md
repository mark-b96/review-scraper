# review-scraper
Python script capable of obtaining product reviews from retailer websites.

## Requirements
* Python3.5+

## Installation
1. Clone the repository: `git clone git@github.com:mark-b96/review-scraper.git`
2. `cd review-scraper`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate virtual environment: `source venv/bin/activate`
5. Install requirements: `pip install -r requirements.txt`

## Usage
### Search
`python3 main.py -s iphone`

Product asins will be output to a csv in `data/input/`
### Scrape
`python3 main.py -i data/input/john_lewis_iphone_asins.csv -o data/output -w john_lewis`

| Argument | Description |
| :----:| :------: |
| -i | Input csv product asin file | 
| -o | Output directory            |
| -w | Website to scrape (Must be in [this](https://github.com/mark-b96/review-scraper/blob/main/review_scraper/urls.py) file) |

## Supported websites
* amazon.co.uk
* johnlewis.com