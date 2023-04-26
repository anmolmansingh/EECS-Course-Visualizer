#%%
# 1. import and basic setup
from bs4 import BeautifulSoup
import json
import requests
import os

CSE_FACULTY_URL = "https://cse.engin.umich.edu/people/faculty/"
ECE_FACULTY_URL = "https://ece.engin.umich.edu/people/directory/faculty/"
CSV_PATH = "../cache/csv"
JSON_PATH = "../cache/json"

# access with scraper
# TODO: scrape atlas for correct prerequisite info for each course


# %%
# 2. scrape ECE faculty website
headers = {
    'User-Agent': 'UMSI 507 Course Project - Python Web Scraping',
    'From': 'anmolmsg@umich.edu',
    'Faculty-Info': 'https://ece.engin.umich.edu/people/directory/faculty/'
}
response = requests.get(ECE_FACULTY_URL, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

print(soup.prettify())
# %%
# crawler for instructor detail
faculty_detail = []

ece_faculty_parent = soup.find('div', class_ = 'people_lists')

ece_faculty_wrapper = ece_faculty_parent.find_all('div', class_ = "eecs_person_wrapper")

for wrapper in ece_faculty_wrapper:
    # fetch faculty name
    faculty_copy = wrapper.find(
        'div', class_ = 'eecs_person_copy')
    faculty_name = faculty_copy.find('h4').text.strip()
    script_contents = faculty_copy.find('script').string.strip()
    uniqname = script_contents.split('var one = \'')[1].split('\';')[0]
    extension = script_contents.split('var two = \'')[1].split('\';')[0]
    faculty_detail.append({"Faculty name": faculty_name, "Email": f"{uniqname}@{extension}", "Uniqname": uniqname, "Department": "ECE"})

# %%
# 2. scrape CSE faculty website
headers = {
    'User-Agent': 'UMSI 507 Course Project - Python Web Scraping',
    'From': 'anmolmsg@umich.edu',
    'Faculty-Info': 'https://cse.engin.umich.edu/people/faculty/'
}
response = requests.get(CSE_FACULTY_URL, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# %%
# scraping the data
cse_faculty_parent = soup.find('div', class_ = 'people_lists')

cse_faculty_wrapper = cse_faculty_parent.find_all('div', class_ = "eecs_person_wrapper")

for wrapper in cse_faculty_wrapper:
    # fetch faculty name
    faculty_copy = wrapper.find(
        'div', class_ = 'eecs_person_copy')
    faculty_name = faculty_copy.find('h4').text.strip()
    script_contents = faculty_copy.find('script').string.strip()
    uniqname = script_contents.split('var one = \'')[1].split('\';')[0]
    extension = script_contents.split('var two = \'')[1].split('\';')[0]
    faculty_detail.append({"Faculty name": faculty_name, "Email": f"{uniqname}@{extension}", "Uniqname": uniqname, "Department": "CSE"})
# %%
# saving into csv and json

# sort alphabetically before writing in json
faculty_detail = sorted(faculty_detail, key = lambda x: x["Faculty name"])

# remove duplicates by uniqname
unique_faculty_set = set()
unique_faculty_detail = [d for d in faculty_detail if d['Uniqname'] not in unique_faculty_set and not unique_faculty_set.add(d['Uniqname'])]

# store in cache & json
with open(os.path.join(CSV_PATH, "faculty_info_list.csv"), 'w') as f2:
    for row in unique_faculty_detail:
        f2.write(','.join(map(str, row.values())))
        f2.write('\n')

with open(os.path.join(JSON_PATH, "faculty_info_list.json"), 'w') as f3:
    f3.write(json.dumps(unique_faculty_detail, indent = 4))
