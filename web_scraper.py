# WEBSCRAPER FOR VACANCYMAIL.CO.ZW
# THIS SCRIPT SCRAPES JOB LISTINGS FROM THE VACANCYMAIL WEBSITE AND SAVES THEM TO A CSV FILE.

import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from datetime import datetime
import schedule
from requests.exceptions import RequestException

# LOGGER CONFIGURATION
logging.basicConfig(
    filename='web_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

BASE_URL = "https://vacancymail.co.zw/jobs/"

# SET UP LOGGING
logger = logging.getLogger('web_scraper')
logger.setLevel(logging.INFO)
logger.info('Web scraper started.')

# FUNCTION TO CHECK IF THE URL IS ACCESSIBLE
def fetch_job_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info(f'Successfully fetched URL: {url}')
        return response.text
    except RequestException as e:
        logger.error(f'Error accessing URL {url}: {e}')
        return None

# FUNCTION TO SCRAPE JOB DATA
def scrape_job_data():
    url = "https://vacancymail.co.zw/jobs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # LOCATE THE JOB POSTINGS CONTAINER
    job_listings = soup.find_all("div", class_="job-listing-details")
    print(f"Found {len(job_listings)} total listings.")
    job_listings = job_listings[:10]  # Get only the top 10

    jobs = []

    for i, job in enumerate(job_listings):
        try:
            title_tag = job.find('h3', class_='job-listing-title')
            company_tag = job.find('h4', class_='job-listing-company')
            desc_tag = job.find('p', class_='job-listing-text')

            # Get location and expiry date from list items
            list_items = job.find_all('li')
            location = list_items[0].text.strip() if len(list_items) > 0 else "N/A"
            expiry_date = list_items[1].text.strip() if len(list_items) > 1 else "N/A"

            jobs.append({
                'Job Title': title_tag.text.strip() if title_tag else "N/A",
                'Company': company_tag.text.strip() if company_tag else "N/A",
                'Location': location,
                'Expiry Date': expiry_date,
                'Description': desc_tag.text.strip() if desc_tag else "N/A"
            })
        except Exception as e:
            logger.warning(f'Error extracting job listing #{i+1}: {e}')
            continue

    # CONVERT TO DATAFRAME
    df = pd.DataFrame(jobs)

    # SAVE TO CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    df.to_csv(f'scraped_data_{timestamp}.csv', index=False)
    print(f'Successfully saved {len(jobs)} job listings to CSV.')

# FUNCTION TO SCHEDULE THE SCRAPING TASK
def schedule_scraping(interval=60):
    schedule.every(interval).minutes.do(scrape_job_data)
    print(f'Scheduled job scraping every {interval} minutes.')
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    scrape_job_data()



