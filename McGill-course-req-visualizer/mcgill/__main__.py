import sys
from course_tree import is_mcgill_course ,build_course_tree, generate_dict_to_plot
from dsplot.graph import Graph


"""(None) -> NoneType
The application's main method receives the course to plot's course code (str) from the terminal, 
checks to see if only one course was entered and if the course is a McGill course (by checking if it's in the database), 
builds the course's CourseTree, and uses that to generate vertices_to_plot and edges_to_plot dictionaries 
that are usable by the dsplot module's Graph methods.

dsplot is a simple, open-source Pythonic interface for Graphviz, an open-source graph visualization software.

The course-requisite-visualization graph below has fill color baby blue, shape square, orientation top-to-bottom.
"""
def main():
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Error: Application only accepts one course as argument.")
        
    course = args[0]
    if not is_mcgill_course(course):
        exit("Error: The course entered is not a McGill course.")
    
    vertices_to_plot = {}
    edges_to_plot = {}
    course_tree = build_course_tree(course, url=None)
    generate_dict_to_plot(course_tree, vertices_to_plot, edges_to_plot)

    graph = Graph(vertices_to_plot, directed=False, edges=edges_to_plot)
    graph.plot(orientation="TB", shape="square", fill_color="#c3e7eb", output_path="../course_tree.png")
    
if __name__ == "__main__":
    main()
