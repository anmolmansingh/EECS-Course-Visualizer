#%%
import json
import os
from constants import TERM_CODES
# this file is for fetching all jsons, preprocessing, adding to classes and objects for better handling

from data.api.instructor_api_call import instructor_courses, oauth_call

CSV_PATH = "data/cache/csv"
JSON_PATH = "data/cache/json"
# ignore directed study/dissertation courses
IGNORE_COURSES = {'EECS 399', 'EECS 499', 'EECS 599', 'EECS 699', 'EECS 990', 'EECS 995', 'SI 995', 'DESCI 990', 'DESCI 995', 'ROB 590', 'ROB 990', 'ROB 995'}

# 
# TODO: make it a drop down list for the user - interaction
instructor_list_with_courses = []

# open the scraped instructor file
with open(os.path.join(JSON_PATH, 'faculty_info_list.json')) as f:
    instructors_list = json.loads(f.read())

#%% 
# one-time: get oauth token   
access_token = oauth_call()

for instructor in instructors_list:
    # call instructor api for each instructor
    uniqname = instructor['Uniqname']
    instructor_courses_response = instructor_courses(access_token, uniqname, TERM_CODES['Fall 2023'])
    # if the professor has taught class
    if 'InstructedClass' in instructor_courses_response.keys():
        courses_taught = [f"{v['SubjectCode']} {v['CatalogNumber']}" for v in instructor_courses_response['InstructedClass']]
        instructor_list_with_courses.append({"Uniqname": uniqname, "Courses taught": courses_taught})
        print("Instructor course details added")
#%%   
# remove extra sections that add duplicate course codes
# remove out-of-scope courses (dissertations etc.)

for instructor in instructor_list_with_courses:
    instructor['Courses taught'] = list(set(instructor['Courses taught']))
    instructor['Courses taught'] = [course for course in instructor['Courses taught'] if course not in IGNORE_COURSES]

# store in cache & json
with open(os.path.join(CSV_PATH, f"faculty_courses_taught_fall_2023.csv"), 'w') as f2:
    for row in instructor_list_with_courses:
        f2.write(','.join(map(str, row.values())))
        f2.write('\n')

with open(os.path.join(JSON_PATH, f"faculty_courses_taught_fall_2023.json"), 'w') as f3:
    f3.write(json.dumps(instructor_list_with_courses, indent = 4))

with open(os.path.join(JSON_PATH, f"faculty_courses_taught_fall_2023.json"),'r') as f4:  
    data = json.load(f4) 


# TODO: ask the user to enter their major and take that value
# print("What's your major?")
