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
post_codes = 2121

url= f"https://www.architects.nsw.gov.au/component/arbregister/?view=architects&regSearchSuburb={post_codes}"
x = requests.get(url)
soup = BeautifulSoup(x.text, 'html.parser')


# next = soup.find_all('a', title='Next', href=True)
# print(next['href'])

def get_href(class_name):
    for a in class_name.find_all('a', title='Next', href=True):
        try:
            return(a['href'])
        except:
            raise Exception("No href found")

    
print(url+get_href(soup))
# print(get_href(soup))

# create for loop to iterate through pages
# grab href from <a> of any class="pagination-next"



# function that grabs "td in tr.find_all('td')"
# then grabs "a" and "href"