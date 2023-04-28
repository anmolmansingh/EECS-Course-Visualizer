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

    def getWeight(self, course):
        return self.adjacent_courses[course]

    def getAdjacentCourses(self):
        return self.adjacent_courses
    
    def getCredits(self):
        try:
            credits_ = int(self.credits)
        except ValueError:
            credits_ = int(self.credits[0])
        return credits_

    def __str__(self):
        #return str(self.id) + 'is connected to ' + str((x.id, x.weight) for x in self.connectedTo)
        return str(self.course_code) + ' has prerequisities ' + str(self)
        # return str(self.course_code) + ' is connected to ' + str([(x, self.connectedTo[x]) for x in self.connectedTo])

