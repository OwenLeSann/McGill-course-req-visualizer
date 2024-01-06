
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
        
    def get_prerequisites(self):
        prerequisites = []
        for prerequisite in self.prerequisites:
            prerequisites.append(str(prerequisite))
        return prerequisites
    
    def get_corequisites(self):
        corequisites = []
        for corequisite in self.corequisites:
            corequisites.append(str(corequisite))
        return corequisites
                    
    def __str__(self):
        return self.course_code


def build_course_tree(course_code, url=None):
    connection = sqlite3.connect("mcgill_courses.db")
    c = connection.cursor()

    try:
        c.execute(f'''
                    SELECT Prerequisites.prerequisite, Prerequisites.prerequisite_url 
                    FROM Prerequisites 
                    LEFT JOIN Courses ON Prerequisites.course_code = Courses.course_code 
                    WHERE Prerequisites.course_code = ?
                    ''', (course_code,))

        prerequisite_data = c.fetchall()
        
        c.execute(f'''
                    SELECT Corequisites.corequisite, Corequisites.corequisite_url 
                    FROM Corequisites 
                    LEFT JOIN Courses ON Corequisites.course_code = Courses.course_code 
                    WHERE Corequisites.course_code = ?
                    ''', (course_code,))
        
        corequisite_data = c.fetchall()

    except sqlite3.Error as e:
        print(f"Error querying {course_code} requisite data: {e}")
    finally:
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
def generate_dict_to_plot(course, vertices_to_plot, edges_to_plot):
    if not course.prerequisites and not course.corequisites:
        vertices_to_plot[str(course)] = []
        return
    
    edges_to_plot["".join(course.get_corequisites())] = ""
    vertices_to_plot[str(course)] = course.get_prerequisites()
    
    for prerequisite in course.prerequisites:
        generate_dict_to_plot(prerequisite, vertices_to_plot, edges_to_plot)

course_to_plot = build_course_tree("COMP 551", url=None)
vertices_to_plot = {}
edges_to_plot = {}
generate_dict_to_plot(course_to_plot, vertices_to_plot, edges_to_plot)

#print(" ".join(course_to_plot.get_corequisites()))
#print(f"vtp: {vertices_to_plot}, etp: {edges_to_plot}")

graph = Graph(vertices_to_plot, directed=False, edges=None)
# fill color baby blue, shape square, orientation top-to-bottom
graph.plot(orientation="TB", shape="square", fill_color="#c3e7eb", output_path="./course_tree.png")