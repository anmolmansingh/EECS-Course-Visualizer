#%%
# 1. import and basic setup
from bs4 import BeautifulSoup
import json
import requests
import os

from constants import CSV_PATH, JSON_PATH, MANDATORY_URL

# access with scraper
# TODO: scrape atlas for correct prerequisite info for each course

#%%
# 2. scrape course info website
headers = {
    'User-Agent': 'UMSI 507 Course Project - Python Web Scraping',
    'From': 'anmolmsg@umich.edu',
    'Course-Info': 'https://ece.engin.umich.edu/academics/course-information/graduate-course-list/'
}
response = requests.get(MANDATORY_URL, headers=headers)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')

print(soup.prettify())
# %%
# extract majors (list of values)
majors = []
major_table = soup.find('table', class_='wp-block-advgb-table advgb-table-frontend')

# find majors for all courses
for entry in major_table.find('tbody'):
    major_row = entry.find_all('td')
    for row in major_row:
        major_value = row.text.strip()
        major_parts = major_value.split("=")
        majors.append({"Major code": major_parts[0].strip(), "Major title": major_parts[1].strip()})

# sort the majors alphabetically and add serial number
majors = sorted(majors, key=lambda x: x['Major code'])
for i, major in enumerate(majors):
    major['Serial number'] = i + 1

print(majors)

# %%
# extract mandatory course info
mandatory_courses = []

course_table = soup.find('table', id='table_1')

course_list = course_table.find('tbody').find_all('tr')

course_major = []

# create dictionary to look up majors by serial number
major_dict = {value["Serial number"] - 1: value['Major code'] for value in majors}

# for course in course_list:
#     course_break_down = course.find_all('td')
#     # majors marked M
#     mandatory_major_list = []
#     # majors marked E
#     advisor_major_list = []
#     # appending mandatory and advisor major details for each course
#     for j, major in enumerate(course_break_down[3:]):
#         if major.contents:
#             # major is M or E (record it)
#             major_m_or_e = major.text.strip()
#             if major_m_or_e == 'M':
#                 for value in majors:
#                     if value["Serial number"] - 1 == j:
#                         mandatory_major_list.append(value['Major code'])

#             else:
#                 for value in majors:
#                     if value["Serial number"] - 1== j:
#                         advisor_major_list.append(value['Major code'])
    
# optimized code
# iterate over courses and extract mandatory and advisor majors
for course in course_list:
    course_break_down = course.find_all('td')
    mandatory_major_list = [major_dict[j] for j, major in enumerate(course_break_down[3:]) if major.text.strip() == 'M']
    advisor_major_list = [major_dict[j] for j, major in enumerate(course_break_down[3:]) if major.text.strip() == 'E']

    # consolidating into dict
    course_major.append(
        {
            "Course code": course_break_down[1].text.strip().split('.')[0], 
            "Course credits": course_break_down[2].text.strip(),
            "Mandatory for": mandatory_major_list,
            "Advisor approval for": advisor_major_list
        }
    )
# for course in course_list:
#     # mandatory_for = add to this list when the course is value M for
# print(course_list)


# %%
# saving into csv and json
import json

with open(os.path.join(CSV_PATH, "mandatory_course_list.csv"), 'w') as f1:
    for row in course_major:
        f1.write(','.join(map(str, row.values())))
        f1.write('\n')

with open(os.path.join(JSON_PATH, "mandatory_course_list.json"), 'w') as f2:
    f2.write(json.dumps(course_major, indent = 4))

# %%
