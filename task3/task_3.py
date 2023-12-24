import hashlib
from bs4 import BeautifulSoup
import os
import csv
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

START_PAGE = 1
END_PAGE = 3
CACHE_PATH = os.path.join(os.getcwd(), 'cache_file')
DATA_FILE_NAME = 'bat_dong_san.csv'

options = Options()
options.add_argument('--headless=new')
options.add_argument('user-agent=fake-useragent')

def get_page_content(url):
    """
        Retrieve the content of a web page either from cache or by scraping.

        Parameters:
        - url (str): The URL of the web page.

        Returns:
        - str: The page content.
    """
    # Check if page is cached
    cache_filename = hashlib.md5(url.encode()).hexdigest() + '.json'
    cache_filepath = os.path.join(CACHE_PATH, cache_filename)
    if os.path.exists(cache_filepath):
        with open(cache_filepath, 'r') as cache_file:
            return json.load(cache_file)
        
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    page_content= driver.page_source
    driver.quit()
    
    # Cache the page content
    with open(cache_filepath, 'w') as cache_file:
        json.dump(page_content, cache_file)
    return page_content

def scrape_batdongsan():
    
    """
        Scrape real estate data from batdongsan.com.vn and write it to a CSV file.

        Returns:
        - None
    """
    
    base_url = 'https://www.batdongsan.com.vn'
    page_url = '/nha-dat-ban'
    
    # default URL
    url = f'{base_url}{page_url}/p1'
    
    datafile_path = os.path.join(os.getcwd(), DATA_FILE_NAME)
    
    # Open a CSV file for writing
    with open(datafile_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write header row
        csv_writer.writerow(['Name', 'Price', 'Area', 'Description', 'Location'])
    
        # Scrape multiple pages, adjust the range accordingly
        for page_number in range(START_PAGE, END_PAGE+1):
            url = f'{base_url}{page_url}/p{page_number}'
            page_content = get_page_content(url)
            soup = BeautifulSoup(page_content, 'html.parser')
            
            # Extract real estate details, adjust selectors based on the website structure
            property_listings = soup.select('.re__card-full')
            print(property_listings)
            for listing in property_listings:
                print(2)
                name = listing.select_one('.pr-title').text.strip()
                price = listing.select_one('.re__card-config-price').text.strip()
                area = listing.select_one('.re__card-config-area').text.strip()
                description = listing.select_one('.re__card-description').text.strip()
                location = listing.select_one('.re__card-location span:last-child').text.strip()
                
                # Write the data to the CSV file
                csv_writer.writerow([name, price, area, description, location])
    
                # Print or store the extracted data
                print(f'Name: {name} Price: {price} Area: {area} Description: {description} Location: {location} ')
                
            # time.sleep(1)

if __name__ == "__main__":
    scrape_batdongsan()