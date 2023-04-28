# pylint: disable=import-error
from flask import Flask, render_template, request, session, jsonify
from flask_paginate import Pagination, get_page_parameter

import pickle
import json
import os

from graph import Graph, course_graph, load_course_objects
# List of all courses
from constants import MAJORS
JSON_PATH = "data/cache/json"
PICKLE_PATH = "data/cache/pickle"

app = Flask(__name__)
app.secret_key = "x19f7uSyUKfsdKCkuyd3a1S90ZG957e1QvPXuClGqwFYdmMXs"

# Set the TEMPLATES_AUTO_RELOAD configuration variable to True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# creating the pickle
# course_graph.data_courses_graph()

@app.route('/')
def home():
    return render_template("index.html", majors = MAJORS)

@app.route("/major", methods=["GET","POST"])
def major(page=1):
    if request.method == "GET" or request.method == "POST":
        selections = request.form.getlist('selectMultipleMajors') # list of selected majors
        session['EECSCS'] = selections

        with open(os.path.join(JSON_PATH, "courses_offered_fall_23.json"),'r') as f1:  
            courses_detail = json.load(f1)
        
        key_list = list(MAJORS.keys())
        val_list = list(MAJORS.values())
        
        courses_selected = []
        major_codes = []

        for selection in selections:
            position = val_list.index(selection)
            major_codes.append(key_list[position])

        for val in major_codes:
            for course in courses_detail:
                if val in course.get("Mandatory for", []):
                    courses_selected.append(course)

        # pagination
        page = int(request.args.get(get_page_parameter(), 1))
        per_page = 10
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_list = courses_selected[start_idx:end_idx]
        pagination = Pagination(page=page, total=len(courses_selected), per_page=per_page, css_framework='bootstrap4')
         # if user selects home, go to index.html
        return render_template("major.html", my_list=paginated_list, pagination=pagination, major = selections, all_majors = MAJORS)


   
@app.route("/major/shortest",  methods=['GET', 'POST'])
def major_shortest_paths():
    if request.method == "POST":
        credits = int(request.form.get('points', 0))
        selections = session.get('EECSCS', None)
        # load the graph
        with open(os.path.join(PICKLE_PATH, "course_graph.pickle"), 'rb') as f2:
            all_course_graph = pickle.load(f2)

        all_suggestions = {}
        # get values from key
        major_codes = [key for key, value in MAJORS.items() if value in selections]
        # get top course suggestions, returns list of list
        for major in major_codes:
            all_suggestions[major] = all_course_graph.top_course_suggestions(major, credits)

    return render_template("shortest.html", majors = major_codes, suggestions = all_suggestions, all_majors = MAJORS)

# show the graph visualized for the majors
@app.route("/major/graph", methods=["GET", "POST"])
def major_graph():
    if request.method == "POST" or request.method == "GET":
        selections = session.get('EECSCS', None)
        major_codes = [key for key, value in MAJORS.items() if value in selections]
        return render_template("graph.html", majors = major_codes, all_majors = MAJORS)


if __name__ == "__main__":
    app.run(debug=True)
