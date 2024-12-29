from websracperClass import WebScraper  # Import WebScraper class from web_scraper.py
from databaseClass import Database  # Import Database class from database.py

# Initialize Database
db = Database()

# Initialize WebScraper with the database object
scraper = WebScraper(db)

# Example list of websites with their categories
websites = [
    {
        "base_url": "https://silayipret.com", 
        "categories": [
            "https://silayipret.com/collections/new-arrivals",
            "https://silayipret.com/collections/fusion",
            "https://silayipret.com/collections/2pc-stitched-printed-khaddar",
            "https://silayipret.com/collections/winter-unstitched",
            "",
            ""
        ]
    },
    # {
    #     "base_url": "https://example.com", 
    #     "categories": [
    #         "/products/dresses",
    #         "/products/tops",
    #         "/products/skirts"
    #     ]
    # }
]

# Loop through each website and scrape the categories
for website in websites:
    base_url = website["base_url"]
    categories = website["categories"]
    print(f"Scraping website: {base_url}")
    
    # Scrape product links for all categories of the current website
    product_links = scraper.scrape_multiple_categories(base_url, categories)
    
    # Optionally print the links that were stored in the database
    print(f"Saved Product Links for {base_url}:")
    saved_links = db.get_all_product_links()
    for link in saved_links:
        print(link)

# Close the database connection when done
db.close()
