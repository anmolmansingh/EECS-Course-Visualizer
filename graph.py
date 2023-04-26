#%%
from class_definitions import Course
from constants import MAJORS
import json
import os
import pickle
import networkx as nx
import matplotlib.pyplot as plt

JSON_PATH = "data/cache/json"
COURSES_FALL_23 = 'courses_offered_fall_23.json'

course_object_list = []
#%%
# Graph containing all the course objects as it's vertices, and edges are mandatory_courses
class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
        # storing all edges for visualization
        self.visual = []

    def addVertex(self, course):
        self.numVertices = self.numVertices + 1
        newVertex = course
        self.vertList[course.getCourseCode()] = newVertex
        return newVertex

    def getVertex(self, course):
        if course.getCourseCode() in self.vertList:
            return self.vertList[course.getCourseCode()]
        else:
            return None

    def __contains__(self, course):
        return course in self.vertList

    def addEdge(self, course_1, course_2, weight=0):
        if course_1.getCourseCode() not in self.vertList.keys():
            self.addVertex(course_1)
        if course_2.getCourseCode() not in self.vertList.keys():
            self.addVertex(course_2)
        # for visualization purpose
        self.visual.append([course_1.getCourseCode(), course_2.getCourseCode()])
        self.vertList[course_1.getCourseCode()].add_adjacent_course(course_2.getCourseCode(), weight)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        pos = nx.spring_layout(G, seed=42)
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos, edgelist=self.visual)
        nx.draw_networkx_labels(G, pos)
        plt.show()
        # G = nx.Graph()
        # G.add_edges_from(self.visual)
        # nx.draw_networkx(G)
        # plt.show()

#%%
# 1. create the object list
# we have the combined course json we need for node creation.
# create the course object with all relevant details
with open(os.path.join(JSON_PATH, COURSES_FALL_23), 'r') as myfile:
    course_trimmed_list = json.load(myfile)

#%%
for course in course_trimmed_list:
    course_object_list.append( 
          Course(
                course_code=course.get("Course code", None), course_name=course.get("Course title", None), 
                credits=course.get("Course credits", None), course_link=course.get("Course link", None),
                mandatory_for=course.get("Mandatory for", None), advisor_approval_for=course.get("Advisor approval for", None)
                )
        )
print(len(course_object_list))
#%%     
# 2. add vertices to graph

#%%
# generate graphs for each major

# consolidated graph of all majors - for relations
g = Graph()
for course in course_object_list:
    g.addVertex(course)

for major in MAJORS.keys():
    # consolidating overall graph
    print(f"{MAJORS[major]}")
    
    # create new graph for each vertex
    for i, course1 in enumerate(course_object_list):
        for course2 in course_object_list[i+1:]:
            # if mandatory course
            if course1.getMandatoryCourses() is not None and course2.getMandatoryCourses() is not None:
                if major in course1.getMandatoryCourses() and major in course2.getMandatoryCourses():
                    g.addEdge(course1, course2, weight=2)
    # if advisory course;
    for i, course1 in enumerate(course_object_list):
        for course2 in course_object_list[i+1:]:
            if course1.getAdvisorApprovedCourses() is not None and course2.getAdvisorApprovedCourses() is not None:
                if major in course1.getAdvisorApprovedCourses() and major in course2.getAdvisorApprovedCourses():
                    g.addEdge(course1, course2, weight=1)

g.visualize()
## Find the most connected course
def most_connected_course():

# major specific detail
def 

# requirement_credits = 18 (max number of creds) 
# visualize the graph

        # save the undirected graph
        # with open(f"graph_major_{}.json", 'w') as f:
        #     f.write()
# %%
