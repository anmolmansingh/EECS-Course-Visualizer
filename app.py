from flask import Flask, render_template, request
import pickle
import json

from constants import MAJORS

app = Flask(__name__)


# Set the TEMPLATES_AUTO_RELOAD configuration variable to True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def home():
    return render_template("index.html", majors = MAJORS)

@app.route("/major", methods=["POST"])
def major():
    if request.method == "POST":
        selections = request.form.getlist('selectMultipleMajors')
        for major in selections:
            print(major)

    # if user selects home, go to index.html
    return render_template("major.html", major = selections)
            

# show the table for major
@app.route("/major/table")
def major_table():
    return render_template("graph.html")
    # show smallest paths
    # show most connected elements

# show the graph visualized for the majors
@app.route("/major/graph")
def major_graph():
    return render_template("tables.html")


if __name__ == "__main__":
    app.run()
