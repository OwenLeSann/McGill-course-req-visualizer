import sqlite3


""""A class representing a course prerequisite and corequisite tree, with prerequisites and corequisites as 
children of the course of interest root node.
"""
class CourseTree(object):
    """(self, str, str) -> NoneType
    "Constructor method for each node of the CourseTree. Currently, I've opted to keep the url attributes in case 
    they are needed in future versions of the application. Note that currently, they serve no purpose in visualizing 
    the courses and their respective corequisites/prerequisites.
    """
    def __init__(self, course_code, url=None):
        self.course_code = course_code
        self.url = url
        self.prerequisites = []
        self.corequisites = []
        self.corequisite_urls = []

    """(self, CourseTree) -> NoneType
    Adds a prerequisite (child) to the CourseTree.
    """
    def add_prerequisite(self, prerequisite):
        self.prerequisites.append(prerequisite)
    
    """(self, CourseTree) -> NoneType
    Adds a corequisite (child) to the CourseTree.
    """  
    def add_corequisite(self, corequisite):
        self.corequisites.append(corequisite)
    
    """(self) -> list[str]
    Returns a list of the course codes of the prerequisites associated with a given CourseTree node (course).
    """
    def get_prerequisites(self):
        prerequisites = []
        for prerequisite in self.prerequisites:
            prerequisites.append(str(prerequisite))
        return prerequisites
   
    """(self) -> str
    String method for CourseTree node.
    """                 
    def __str__(self):
        return self.course_code

"""(str, str) -> list[tup(str,)]
Helper function used to encapsulate all queries related to the course_code 
(which are all the queries necessary to graph the course requisite tree).
"""
def query_course(actions, course_code):
    connection = sqlite3.connect("./mcgill_courses.db")
    c = connection.cursor()
    
    try:
        c.execute(actions, (course_code,))
        data = c.fetchall()
    
    except sqlite3.Error as e:
        exit(f"Error querying {course_code} data: {e}")
    finally:
        connection.close()
        
    return data
    
"""(str) -> list[tup(str,)]
Checks if a given course_code is in the database and returns that course_code.
"""
def is_mcgill_course(course_code):
    course_data = query_course(f'''
                                SELECT course_code
                                FROM Courses
                                WHERE Courses.course_code = ?
                                ''', course_code)
    
    return course_data

"""(str, str, list) -> CourseTree
Recursively builds a CourseTree for a given course code with the prerequisites and corequisites queried from the database.
"""
def build_course_tree(course_code, url=None, visited=None):
    if visited is None:
        visited = set()
    
    prerequisite_data = query_course(f'''
                                    SELECT Prerequisites.prerequisite, Prerequisites.prerequisite_url 
                                    FROM Prerequisites 
                                    LEFT JOIN Courses ON Prerequisites.course_code = Courses.course_code 
                                    WHERE Prerequisites.course_code = ?
                                    ''', course_code)
    
    corequisite_data = query_course(f'''
                                    SELECT Corequisites.corequisite, Corequisites.corequisite_url 
                                    FROM Corequisites 
                                    LEFT JOIN Courses ON Corequisites.course_code = Courses.course_code 
                                    WHERE Corequisites.course_code = ?
                                    ''', course_code)

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

"""(CourseTree, dict{str: list[str]}, dict{str: str}) -> NoneType
A preorder tree traversal of the CourseTree that recursively lists each course and its prerequisites and 
corequisites into a dictionary of the format necessary for the plot functions of the dsplot module in 
the __main__.py file. The vertices_to_plot dictionary has the course_code as a key and a list of its 
prerequisites as its children. The edges_to_plot dictionary has the corequisite's pairwise relation (edge) 
concatenated into a string as the key, and the name of the edge (in this case, 'corequisites' for all edges) 
as the value.
"""
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
