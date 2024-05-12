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

url = f"https://www.architects.nsw.gov.au/component/arbregister/?view=architects&regSearchSuburb={post_codes}"
x = requests.get(url)
soup = BeautifulSoup(x.text, 'html.parser')


def get_next(class_name) -> str :
    '''
        returns next page url if exists, otherwise returns ""
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

#TODO: write_rows() may need to be modified to a different function
# It needs to get links from each architect
# then go into it an grab the information

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
    

# create while equence:
# 1. run write_rows()
# 2. change url to url+get_next(soup)
# 3. if check_tr(soup) is False, break 

while get_next(soup) != "":
    write_rows(soup)
    print(url+get_next(soup))
    x = requests.get(url+get_next(soup))
    soup = BeautifulSoup(x.text, 'html.parser')
    time.sleep(random.randint(1, 5))
    #iter_number += 1
    if check_tr(soup) == False:
        break



if get_next(soup) is None:
    logger.info(f"Post code {post_codes} has only one page.")
else:
    print(url+get_next(soup))

write_rows(soup)
print(check_tr(soup))