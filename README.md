# JOB SCRAPER FOR VACANCYMAIL ZIMBABWE

-This is a Python script that scrapes the 10 most recently posted job listings from the vacancymail website.
-It extracts key information such as job title, company name, location of the job role, expiry date of applications and the job description. 
-It also saves the data into a structured CSV file.

## FEATURES

-Scrapes the 10 latest jobs from the VacancyMail website.
-It extracts and saves relevant job information.
-Includes logging to 'web_scraper.log' to log events and errors.
-Handles network and parsing errors gracefully.
-Optionally supports daily scheduling using the schedule module.

## REQUIREMENTS

- Pandas library for data storage and formatting.
- BeautifulSoup for parsing HTML.
- Schedule to automate scraping.
- Requests for making HTTP requests.

## INSTALL DEPENDENCIES 
- pip install requests beautifulSoup4 pandas schedule

## USAGE
- The script should be run once which will then enable daily scheduled scraping. This will scrape new jobs every 60 minutes. 