# class definitions live here

from constants import MAJORS


#  Vertex of all graphs to be presented
class Course:
    '''
    - course_code (str): the course code
    - course_name (str): the course name
    - course_link (str): the course link
    - credit_hours (str): the credit hours for the course
    - instructor (list): a list of instructors teaching the course
    - mandatory_for (list): a list of majors for which the course is mandatory
    - prereqs (list): a list of prerequisites for the course
    '''
    def __init__(self, course_code="No number", course_name="No name", credits="No info", course_link="No link", mandatory_for=[], advisor_approval_for=[]):
        self.course_code = course_code
        self.course_name = course_name
        self.credits = credits
        self.course_link = course_link
        self.mandatory_for = mandatory_for
        self.advisor_approval_for = advisor_approval_for
        self.adjacent_courses = {}

    def add_adjacent_course(self, course, weight):
        self.adjacent_courses[course] = weight

    def getCourseCode(self):
        return self.course_code
    
    def getMandatoryCourses(self):
        return self.mandatory_for
        
    def getAdvisorApprovedCourses(self):
        return self.advisor_approval_for

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def getAdjacentCourses(self):
        return self.adjacent_courses.keys()

    def __str__(self):
        #return str(self.id) + 'is connected to ' + str((x.id, x.weight) for x in self.connectedTo)
        return str(self.course_code) + ' has prerequisities ' + str(self)
        # return str(self.course_code) + ' is connected to ' + str([(x, self.connectedTo[x]) for x in self.connectedTo])

class Instructor:
    '''
    A class representing an instructor.
    Attributes:
    - uniqname (str): the instructor's uniqname
    - full_name (str): the instructor's full name
    - email (str): the instructor's email address
    - department (str): the instructor's department
    - courses_taught (list): a list of courses taught by the instructor
    '''
    def __init__(self, uniqname="No uniqname", full_name="No name", email="No email", department="No department", courses_taught="No courses taught", json=None):
        self.uniqname = uniqname
        self.full_name = full_name
        self.email = email
        self.courses_taught = courses_taught
        self.department = department
        self.json = json
        
    def add_course_taught(self, course):
        self.courses_taught.append(course)

    def info(self):
        print(f"The instructor is: {self.full_name} and the description is: \n {self.course_description}")

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, course_code):
        self.numVertices = self.numVertices + 1
        newVertex = Course(course_code)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,weight=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], weight)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())


# def minimum_spanning_tree():

