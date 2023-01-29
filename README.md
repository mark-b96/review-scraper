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
### Scrape
`python main.py -i <path to input csv file>`

#### Sample input csv file
```
Product ID	Website	 Output directory	                        Process
B08L5RD3KR	amazon	 /home/mark/Documents/product_reviews/output/   TRUE
```
#### Sample output csv file
```
id	        date	        title	        rating	location        verified content
RJ7ZBP2X6517B	18 January 2023	First new phone	5	United Kingdom	TRUE	 Nice phone, meets all my requirements
```

## Supported websites
* amazon.co.uk
* johnlewis.com