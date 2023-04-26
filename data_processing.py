#%%
import json
import os
import re

JSON_PATH = "data/cache/json"
COURSE_PREREQS = 'course_prereqs.json'
COURSE_COMBINED = 'course_combined.json'
INSTRUCTOR_COMBINED = 'instructor_combined.json'
COURSES_FALL_23 = 'courses_offered_fall_23.json'
# open all json files

def return_courses_json():
    with open(os.path.join(JSON_PATH, "course_details.json"),'r') as f1:  
        data = json.load(f1) 
    return data

def return_instructor_details_json():
    with open(os.path.join(JSON_PATH, "faculty_info_list.json"),'r') as f2:  
        data = json.load(f2)
    return data

def return_instructor_courses_json():
    with open(os.path.join(JSON_PATH, "faculty_courses_taught_fall_2023.json"), 'r') as f3:
        data = json.load(f3)
    return data    

def return_mandatory_courses_json():
    with open(os.path.join(JSON_PATH, "mandatory_course_list.json"),'r') as f4:  
        data = json.load(f4)
    return data

courses = return_courses_json()
instructors = return_instructor_details_json()
instructor_courses = return_instructor_courses_json()
mandatory_for = return_mandatory_courses_json()

course_consolidated = {}
instructors_consolidated = {}

#%%
# getting course-prereq relations
course_prereqs = []
for course in courses:
    # extract prereq courses
    prereqs_for_course = []
    prereq_str = course['Course Prerequisites']
    if 'Prerequisite:' in prereq_str:
        if "none" in prereq_str.lower():
            continue
        else:
            prerequisites = prereq_str.split("Prerequisite:")
            if len(prerequisites) == 1:
                prereqs_for_course = re.findall(r"[A-Z]+ \d{3}", prerequisites[0])
            else:
                prereqs_for_course = re.findall(r"[A-Z]+ \d{3}", prerequisites[1])
    course_prereqs.append({"Course code" : course['Course code'], "Prerequisite code": prereqs_for_course})

if os.path.isfile(JSON_PATH + '/'+ COURSE_PREREQS):
    print(f'The file {COURSE_PREREQS} already exists')
else:
    with open(os.path.join(JSON_PATH, "course_prereqs.json"), 'w') as f:
        f.write(json.dumps(course_prereqs, indent=4))
# %%
# cleaning the data
# for course in courses:
#     if len(course['Course code']) > 8:
#         print(course['Course code'])

# for course in course_prereqs:
#     if len(course['Course code']) > 8:
#         print(course['Course code'])

# for course in mandatory_for:
#     if len(course['Course code']) > 8:
#         print(course['Course code'])

# %%
# first, combine the JSONs


# Iterate through the items in course and add them to the combined dictionary
for course in courses:
    key = course["Course code"]
    course_consolidated[key] = course

# Iterate through the items in mandatory_for and course_prereqs and add them to the combined dictionary
for course in mandatory_for:
    key = course["Course code"]
    if key in course_consolidated:
        course_consolidated[key].update(course)
    else:
        course_consolidated[key] = course

for course in course_prereqs:
    key = course["Course code"]
    if key in course_consolidated:
        course_consolidated[key].update(course)
    else:
        course_consolidated[key] = course
# Convert the combined dictionary back to a list of dictionaries
course_consolidated_list = list(course_consolidated.values())

# Convert the combined list back to JSON
if os.path.isfile(JSON_PATH + '/'+ COURSE_COMBINED):
    print(f'The file {COURSE_COMBINED} already exists')
else:
    with open(os.path.join(JSON_PATH, COURSE_COMBINED), 'w') as myfile:
        myfile.write(json.dumps(course_consolidated_list, indent=4))
# %% for instructors
# Iterate through the items in the two instructor jsons add them to the combined dictionary
for instructor in instructors:
    key = instructor["Uniqname"]
    instructors_consolidated[key] = instructor

for instructor in instructor_courses:
    key = instructor["Uniqname"]
    if key in instructors_consolidated:
        instructors_consolidated[key].update(instructor)
    else:
        instructors_consolidated[key] = instructor

# Convert the combined dictionary back to a list of dictionaries
instructor_consolidated_list = list(instructors_consolidated.values())

#%%
# Convert the combined list back to JSON
if os.path.isfile(JSON_PATH + '/'+ INSTRUCTOR_COMBINED):
    print(f'The file {INSTRUCTOR_COMBINED} already exists')
else:
    with open(os.path.join(JSON_PATH, INSTRUCTOR_COMBINED), 'w') as myfile:
        myfile.write(json.dumps(instructor_consolidated_list, indent=4))



# %%
# get only the courses taught in fall 2023
course_trimmed_list = []
for instructor in instructor_consolidated_list:
    for course in instructor.get('Courses taught', []):
        for course_dict in course_consolidated_list:
            if course_dict['Course code'] == course:
                course_trimmed_list.append(course_dict)
                break


# print(course_trimmed_list[:10])

# %%
# Convert the fall 2023 list back to JSON
if os.path.isfile(JSON_PATH + '/'+ COURSES_FALL_23):
    print(f'The file {COURSES_FALL_23} already exists')
else:
    with open(os.path.join(JSON_PATH, COURSES_FALL_23), 'w') as myfile2:
        myfile2.write(json.dumps(course_trimmed_list, indent=4))