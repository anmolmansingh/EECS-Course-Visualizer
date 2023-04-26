#%%
# 1. import and basic setup
from email import header
from bs4 import BeautifulSoup

import json
import os
import requests
import constants

#%%
# 2. scrape course info website 
headers = {
    'User-Agent': 'UMSI 507 Course Project - Python Web Scraping',
    'From': 'anmolmsg@umich.edu',
    'Faculty-Info': 'https://cse.engin.umich.edu/people/faculty/'
}
response = requests.get(constants.BULLETIN_URL, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
course_list = []

# get the course numbers and other things

course_details_parent = soup.find('div', class_='entry-content')

# exclude the first entry which is not a course
course_para = course_details_parent.find_all('p')[1:]
# print(course_para[0])

for course in course_para:
    code_title = course.find('strong').text.split('.')
    code = code_title[0]
    title = code_title[1].strip()
    prereqs = course.find('em').text.strip()
    link = course.find('a').get('href')
    course_list.append({"Course code": code, "Course title": title, "Course Prerequisites": prereqs, "Course link": link})
#%%

# store the course details in a CSV & save in cache csv
with open(os.path.join(constants.CSV_PATH, "course_details.csv"), 'w') as f2:
    for row in course_list:
        f2.write(','.join(map(str, row.values())))
        f2.write('\n')

with open(os.path.join(constants.JSON_PATH, "course_details.json"), 'w') as f3:
    f3.write(json.dumps(course_list, indent = 4))


# %%
