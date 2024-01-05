
import sqlite3
from dsplot.graph import Graph
# igraph must be installed as well as dsplot python library


class CourseTree(object):
    def __init__(self, course_code, url=None):
        self.course_code = course_code
        self.url = url
        self.prerequisites = []
        self.corequisites = []
        self.corequisite_urls = []

    def add_prerequisite(self, prerequisite):
        self.prerequisites.append(prerequisite)
        
    def __str__(self):
        return self.course_code


def build_course_tree(course_code, url=None):
    connection = sqlite3.connect("mcgill_courses.db")
    c = connection.cursor()

    c.execute(f"SELECT Prerequisites.prerequisite, Prerequisites.prerequisite_url \
                FROM Prerequisites \
                LEFT JOIN Courses ON Prerequisites.course_code = Courses.course_code \
                WHERE Prerequisites.course_code = ?", (course_code,))

    prerequisite_data = c.fetchall()
    
    c.execute(f"SELECT Corequisites.corequisite, Corequisites.corequisite_url \
                FROM Corequisites \
                LEFT JOIN Courses ON Corequisites.course_code = Courses.course_code \
                WHERE Corequisites.course_code = ?", (course_code,))
    
    corequisite_data = c.fetchall()

    connection.close()

    current_course = CourseTree(course_code, url)
    
    if corequisite_data:
        corequisites, corequisite_urls = zip(*corequisite_data)
        current_course.corequisites = corequisites
        current_course.corequisite_urls = corequisite_urls

    if prerequisite_data:
        for prerequisite, prerequisite_url in prerequisite_data:
            prerequisite_node = build_course_tree(prerequisite, prerequisite_url)
            current_course.add_prerequisite(prerequisite_node)

    return current_course

# preorder tree traversal
# This needs to be fixed
def generate_dict_to_plot(course, vertices_to_plot, edges_to_plot):
    if not course.prerequisites:
        return
    
    vertices_to_plot[str(course)] = course.prerequisites
    
    for corequisite in course.corequisites:
        edges_to_plot[(str(course), str(corequisite))] = "corequisites"
    
    for prerequisite in course.prerequisites:
        generate_dict_to_plot(prerequisite, vertices_to_plot, edges_to_plot)

course_to_plot = CourseTree("COMP 551")
vertices_to_plot = {}
edges_to_plot = {}
generate_dict_to_plot(course_to_plot, vertices_to_plot, edges_to_plot)

graph = Graph(vertices_to_plot, directed=False, edges=edges_to_plot)
graph.plot()
