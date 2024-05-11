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


iter_number = 1
# post_codes = post_code[random.randint(0, len(post_code))]
post_codes = 2000

url = f"https://www.architects.nsw.gov.au/component/arbregister/?view=architects&regSearchSuburb={post_codes}"
x = requests.get(url)
soup = BeautifulSoup(x.text, 'html.parser')
print(type(x))
print(type(soup))


def get_href(class_name) -> str :
    '''
        returns next link page if not returns ""
            Parameters:
                class_name: BeautifulSoup object

            Returns:
                next_link: str
    '''
    next_link:str = ""
    for a in class_name.find_all('a', title='Next', href=True):
        if a['href'] is None:
            next_link = ""
        else:
            next_link = a['href']
    return next_link


def write_rows(class_name):
    '''
        writes rows to csv file
            Parameters:
                class_name: BeautifulSoup object
    '''
    with open('output.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        for tr in class_name.find_all('tr'):
            row = []
            for td in tr.find_all('td'):
                row.append(td.get_text(strip=True))
            for links in tr.find_all('a'):
                row.append(links.get('href'))
            writer.writerow(row)        
            
def check_tr(class_name)-> bool:
    '''
        checks if there is any 'tr' in the class
            Parameters:
                class_name: BeautifulSoup object
    '''
    if class_name.find_all('tr') == []:
        return False
    else:
        return True




# function that grabs "td in tr.find_all('td')"
# then grabs "a" and "href"

if get_href(soup) is None:
    logger.info(f"Post code {post_codes} has only one page.")
else:
    print(url+get_href(soup))
    
write_rows(soup)
print(check_tr(soup))