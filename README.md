# review-scraper
Python script capable of obtaining product reviews from retailer websites.

## Requirements
* Python3.5+

## Installation
1. Clone the repository: `git clone repo.git`
2. `cd repo`
3. Create a virtual environment: `python3 -m venv .review_scraper`
4. Activate virtual environment: `source ./review_scraper/bin/activate`
5. Install requirements: `python3 -m pip install -r requirements.txt`

## Usage
###Search
`python3 main.py -s iphone`

Product asins will be output to a csv in `data/input/`
###Scrape
`python3 main.py -i john_lewis_iphone_asins.csv -o data/output -w john_lewis`

| Argument | Description |
| :----:| :-------: |
| -i | Input csv product asin file | 
| -o | Output directory            |
| -w | Website to scrape (Must be in `review_scraper/urls.py`) |