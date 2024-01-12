
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
        
    def add_corequisite(self, corequisite):
        self.corequisites.append(corequisite)
        
    def get_prerequisites(self):
        prerequisites = []
        for prerequisite in self.prerequisites:
            prerequisites.append(str(prerequisite))
        return prerequisites
                    
    def __str__(self):
        return self.course_code


def build_course_tree(course_code, url=None, visited=None):
    if visited is None:
        visited = set()
    
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

    visited.add(course_code)
    current_course = CourseTree(course_code, url)
    
    for prerequisite, prerequisite_url in prerequisite_data:
        if prerequisite not in visited:
            prerequisite_node = build_course_tree(prerequisite, prerequisite_url, visited)
            current_course.add_prerequisite(prerequisite_node)
                
    for corequisite, corequisite_url in corequisite_data:
        if corequisite not in visited:
            corequisite_node = build_course_tree(corequisite, corequisite_url, visited)
            current_course.add_corequisite(corequisite_node)

    visited.remove(course_code)
    return current_course

# preorder tree traversal
def generate_dict_to_plot(course, vertices_to_plot, edges_to_plot):
    if not course.prerequisites and not course.corequisites:
        vertices_to_plot[str(course)] = []
        return
      
    vertices_to_plot[str(course)] = course.get_prerequisites()
    
    for prerequisite in course.prerequisites:
        generate_dict_to_plot(prerequisite, vertices_to_plot, edges_to_plot)
        
    for corequisite in course.corequisites:
        generate_dict_to_plot(corequisite, vertices_to_plot, edges_to_plot)
        vertices_to_plot[str(course)].append(str(corequisite))
        edges_to_plot[str(course) + str(corequisite)] = "corequisites"


course_to_plot = build_course_tree("COMP 421", url=None)
vertices_to_plot = {}
edges_to_plot = {}
generate_dict_to_plot(course_to_plot, vertices_to_plot, edges_to_plot)

graph = Graph(vertices_to_plot, directed=False, edges=edges_to_plot)
# fill color baby blue, shape square, orientation top-to-bottom
graph.plot(orientation="TB", shape="square", fill_color="#c3e7eb", output_path="./course_tree.png")