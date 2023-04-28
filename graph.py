#%%
from class_definitions import Course
from constants import MAJORS
import json
import os
import pickle
import matplotlib.pyplot as plt
import networkx as nx


JSON_PATH = "data/cache/json"
PICKLE_PATH = "data/cache/pickle"
COURSES_FALL_23 = 'courses_offered_fall_23.json'
COURSE_GRAPH = 'course_graph.pickle'

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

    def getVertex(self, course_code):
        if course_code in self.vertList.keys():
            return self.vertList[course_code]
        else:
            return None

    def __contains__(self, course):
        return course in self.vertList

    def addEdge(self, course_1, course_2, weight=0):
        if course_1.getCourseCode() not in self.vertList.keys():
            self.addVertex(course_1)
        if course_2.getCourseCode() not in self.vertList.keys():
            self.addVertex(course_2)
        # for visualizations
        self.visual.append([course_1.getCourseCode(), course_2.getCourseCode()])
        # add adjacent courses to course object itself
        self.vertList[course_1.getCourseCode()].add_adjacent_course(course_2, weight)

    def getVertices(self):
        return self.vertList.values()

    def __iter__(self):
        return iter(self.vertList.values())
    
    def remove_duplicates(self, list_of_lists):
        unique_lists = []
        for sublist in list_of_lists:
            # Convert sublist to set to ignore order and duplicates
            subset = set(sublist)
            # Check if subset is already in unique_lists
            if not any(subset == set(ul) for ul in unique_lists):
                unique_lists.append(sublist)
        return unique_lists

    def dfs(self, course, major, credits, path, all_paths):
    # Base case: if credits reached to 0, add path to all_paths
        if credits <= 0:
            all_paths.append(path)
            return
        # If credits not reached 0, explore adjacent courses
        for neighbor in list(course.getAdjacentCourses().keys()):
            if neighbor.getMandatoryCourses() is not None and neighbor.getAdvisorApprovedCourses() is not None:
                if major not in neighbor.getMandatoryCourses() and major not in neighbor.getAdvisorApprovedCourses():
                    continue
            if neighbor not in path: # prevent cycles
                new_credits = credits - neighbor.getCredits()
                if new_credits > 0: # course fits credit requirement
                    self.dfs(neighbor, major, new_credits, path + [neighbor], all_paths)
                else:
                    all_paths.append(path)
                    return

    # DFS to get course suggestions
    # returns list of lists
    def top_course_suggestions(self, major, credit_requirement):
        # choose a course from major at random as start course
        mandatory_courses = []
        for vertex in list(self.getVertices()):
            if vertex.getMandatoryCourses() is not None:
                if major in vertex.getMandatoryCourses():
                    mandatory_courses.append(vertex)  

        all_paths = []
        paths_course_codes = []
        for course in mandatory_courses:
            self.dfs(course, major, credit_requirement, [course], all_paths)
        for path in all_paths:
            if sum(course.getCredits() for course in path) >= credit_requirement:
                paths_course_codes.append([str(course.getCourseCode()) for course in path])
        unique_paths = self.remove_duplicates(paths_course_codes)
        return unique_paths
        # for path in unique_paths:     
        #     print("Path with sufficient credits:", path)

    def visualize(self, num):
        # G = nx.Graph()
        # G.add_edges_from(self.visual)
        # pos = nx.spring_layout(G, seed=42)
        # nx.draw_networkx_nodes(G, pos)
        # nx.draw_networkx_edges(G, pos, edgelist=self.visual)
        # nx.draw_networkx_labels(G, pos)
        # plt.savefig(f'individual_graph_{num}')
        # plt.show()

        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.savefig(f'individual_graph_{num}')
        plt.clf()

#%%
# 1. create the object list
# we have the combined course json we need for node creation.
# create the course object with all relevant details
def load_course_objects():
    course_objects = []
    # TODO: change this for semester choice in future
    with open(os.path.join(JSON_PATH, COURSES_FALL_23), 'r') as myfile:
        course_trimmed_list = json.load(myfile)

    #%%
    for course in course_trimmed_list:
        course_objects.append( 
            Course(
                    course_code=course.get("Course code", None), course_name=course.get("Course title", None), 
                    credits=course.get("Course credits", None), course_link=course.get("Course link", None),
                    mandatory_for=course.get("Mandatory for", None), advisor_approval_for=course.get("Advisor approval for", None)
                    )
            )
    return course_objects
#%%     
# 2. add vertices to graph

#%%
# generate graphs for each major

# consolidated graph of all majors - for relations


# storing the graph in JSON
class course_graph:
    def data_courses_graph():
        # combined_graph = Graph()
        course_objects = load_course_objects()
        consolidated_graph = Graph()

        for course in course_objects:
            consolidated_graph.addVertex(course)

        # print(len(g.getVertices()))
    
        for j, val in enumerate(MAJORS.keys()):
            # individual graphs
            individual_graph = Graph()
            for course in course_objects:
                individual_graph.addVertex(course)

            # graph builds for each major
            for i, course1 in enumerate(course_objects):
                for course2 in course_objects[i+1:]:
                    # if mandatory course
                    if course1.getMandatoryCourses() is not None and course2.getMandatoryCourses() is not None:
                        if val in course1.getMandatoryCourses() and val in course2.getMandatoryCourses():
                            consolidated_graph.addEdge(course1, course2, weight=1)
                            individual_graph.addEdge(course1, course2, weight=1)

            # if mandatory/advisory connection, assign intermediate weight
            for i, course1 in enumerate(course_objects):
                for course2 in course_objects[i+1:]:
                    # if mandatory course
                    if course1.getAdvisorApprovedCourses() is not None and course2.getMandatoryCourses() is not None:
                        if (val in course1.getAdvisorApprovedCourses() and val in course2.getMandatoryCourses()) or (val in course1.getMandatoryCourses() and val in course2.getAdvisorApprovedCourses()):
                            consolidated_graph.addEdge(course1, course2, weight=2)
                            individual_graph.addEdge(course1, course2, weight=2)
                    if course1.getMandatoryCourses() is not None and course2.getAdvisorApprovedCourses() is not None:
                        if (val in course1.getMandatoryCourses() and val in course2.getAdvisorApprovedCourses()) or (val in course1.getMandatoryCourses() and val in course2.getAdvisorApprovedCourses()):
                            consolidated_graph.addEdge(course1, course2, weight=2)
                            individual_graph.addEdge(course1, course2, weight=2)

            # if advisory courses only, assign lesser weight
            for i, course1 in enumerate(course_objects):
                for course2 in course_objects[i+1:]:
                    if course1.getAdvisorApprovedCourses() is not None and course2.getAdvisorApprovedCourses() is not None:
                        if val in course1.getAdvisorApprovedCourses() and val in course2.getAdvisorApprovedCourses():
                            consolidated_graph.addEdge(course1, course2, weight=3)
                            individual_graph.addEdge(course1, course2, weight=3)

            individual_graph.visualize(j)

            with open(os.path.join(PICKLE_PATH, f'individual_graph_{j}.pickle'), 'wb') as myfile:
                pickle.dump(individual_graph, myfile)
    
            
        with open(os.path.join(PICKLE_PATH, COURSE_GRAPH), 'wb') as myfile2:
            pickle.dump(consolidated_graph, myfile2)

        # visualize graph for all courses
        # consolidated_graph.visualize()
    # data_courses_graph()
        # save graph
        


if __name__ == "__main__":
    course_graph.data_courses_graph()
