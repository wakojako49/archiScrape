import requests
from bs4 import BeautifulSoup
import random
import time
from post_code import post_code
import csv
import logging
import re
import datetime

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='archiScrape.log', level=logging.INFO)



codes = post_code[random.randint(0, len(post_code))]
iter_number = 1
x = requests.get(f"https://www.architects.nsw.gov.au/component/arbregister/?view=architects&regSearchSuburb={codes}&Itemid=144&start={iter_number}")
soup = BeautifulSoup(x.text, 'html.parser')
page_numbers = soup.find("p", class_="counter")

#should capture number of pages.
try:
    test = page_numbers.get_text(strip=True)
    page_iter = re.search(r'\d+$', test).group(0)
    logger.info(f"{datetime.datetime.now()}: Post code {codes} has only {page_iter} page.")

except:
    page_iter = 1
    logger.info(f"{datetime.datetime.now()}: Post code {codes} has only 1 page.")

print(page_iter)
print(len(soup.find_all('tr')))


with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # Find all 'tr' elements
    for tr in soup.find_all('tr'):
        row = []

        # For each 'tr', find all 'td' elements within it
        for td in tr.find_all('td'):
            # Extract the text from the 'td', remove any extra whitespace, and append it to the list
            row.append(td.get_text(strip=True))

        for links in tr.find_all('a'):
            row.append(links.get('href'))

        # Write the list to the CSV file
        writer.writerow(row)

        # for iter_codes, codes in enumerate(post_code):
#     logger.info(f"Searching for post code: {codes}")
#     iter_number = 1
#     x = requests.get(f"https://www.architects.nsw.gov.au/component/arbregister/?view=architects&regSearchSuburb={codes}&Itemid=144&start={iter_number}")
#     soup = BeautifulSoup(x.text, 'html.parser')
#     page_numbers = soup.find("p", class_="counter")