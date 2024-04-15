import requests
from bs4 import BeautifulSoup
import random
import time
import csv

trial = 1

id_test = 8576
# id = random.randint(1000, 999999)
# x = requests.get(f"https://www.architects.nsw.gov.au/architects-register/{id}?view=architect")

while True:
    x = requests.get(f"https://www.architects.nsw.gov.au/architects-register/{id}?view=architect")
    if x.status_code == 200:
        break
    else:
        print(f"trial {trial}, id: {id} failed. Trying again...")
        time.sleep(0.25)
        id = random.randint(1000, 999999)
        trial += 1

soup = BeautifulSoup(x.text, 'html.parser')

# write to csv

name = soup.h2.string
print(name)