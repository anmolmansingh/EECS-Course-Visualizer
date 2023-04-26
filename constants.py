# U-M specific variables
TERM_CODES = {'Fall 2023': '2460', 
              'Winter 2024': '2470', 
              'Spring 2024': '2480', 
              'Spring/Summer 2024': '2490', 
              'Summer 2024': '2500'}

MAJORS = {"CM": "Network, Communication, and Information Systems",
          "CT": "Control Systems", 
          "CV": "Computer Vision",
          "EM": "Applied Electromagetics & RF Circuits",
          "ES": "Embedded Systems", 
          "IC": "Integrated Circuits & VLSI", 
          "MM": "MEMS & Microsystems", 
          "OP": "Optics & Photonics", 
          "PE": "Power & Energy", 
          "RO": "Robotics", 
          "SP": "Signal & Image Processing and Machine Learning",
          "SS": "Solid State & Nanotechnology"}

# courses that can be ignored
# EECS x99, dissertation, phd
IGNORE_COURSES = {'EECS 399', 'EECS 499', 'EECS 599', 'EECS 699', 'EECS 990', 'EECS 995', 'SI 995'}

# api variables
GRANT_TYPE = "client_credentials"
SCOPE = "instructors"

# cache constants
CSV_PATH = "../cache/csv"
JSON_PATH = "../cache/json"

# scrape urls
BULLETIN_URL = 'https://bulletin.engin.umich.edu/courses/eecs/'
ECE_FACULTY_URL = 'https://ece.engin.umich.edu/people/directory/faculty/'
CSE_FACULTY_URL = 'https://cse.engin.umich.edu/people/faculty/'
MANDATORY_URL = 'https://ece.engin.umich.edu/academics/course-information/graduate-course-list/'
