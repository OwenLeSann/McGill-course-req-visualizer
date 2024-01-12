# McGill Course Requisite Visualizer
The McGill Course Requisite Visualizer is a tool intended to help McGill students visualize the necessary prerequistes' and complementary corerequisites' course streams for a given course. The application stores all McGill course information scraped off of the [McGill eCalendar](https://www.mcgill.ca/study/2023-2024/courses/search) into a [SQL database](https://github.com/OwenLeSann/McGill-course-req-visualizer/blob/main/McGill-course-req-visualizer/assets/db_schema.png) and uses that course information to graph a tree with the course of interest at the root and its respective prerequisites and corequisites as children. The graph is currently outputed as a PNG file: \
![ANAT 262.png](https://github.com/OwenLeSann/McGill-course-req-visualizer/blob/main/McGill-course-req-visualizer/assets/ANAT%20262.png) \
In the future I intend to implement a web-interface for the application, currently only terminal use is supported.

## Getting Started
### Prerequisites
The necessary software required to run the application includes:
- [Python](https://www.python.org) 
- [Scrapy](https://scrapy.org) 
- [Graphviz](https://www.graphviz.org) 
- [DSPlot](https://pypi.org/project/dsplot/)

Recomended software includes: 
- [Homebrew](https://brew.sh) 

For most of this project I used conda-forge to install these packages, however, I believe that Homebrew is more widely supported. More, notably, I could not install Graphviz with conda-forge despite it being listed as compatible.

### Installing
Software version and installation instructions linked below:
- [Python 3.11.5](https://www.python.org/downloads/release/python-3115/)
- [Scrapy 2.8.0](https://docs.scrapy.org/en/latest/intro/install.html)
- [Graphviz](https://www.graphviz.org/download/)
- [DSPlot 0.9.0](https://pypi.org/project/dsplot/)

Note that the application should work with the most recent versions of each software. I believe that there may be some incompatibility with certain versions of Python and Scrapy, if that is the case, download the version of python linked above and Scrapy 2.8.0 by executing `pip install Scrapy=2.8.0` in your UNIX terminal.

## Usage
**Step 1.** \
Copy the McGill-course-req-visualizer directory to your computer \
![step_1.png](https://github.com/OwenLeSann/McGill-course-req-visualizer/blob/main/McGill-course-req-visualizer/assets/step_1.png) 

**Step 2.** \
Make sure you are in the mcgill file directory. \
![step_2.png](https://github.com/OwenLeSann/McGill-course-req-visualizer/blob/main/McGill-course-req-visualizer/assets/step_2.png) 

**Step 3.** \
Run the main script. \
![step_3.png](https://github.com/OwenLeSann/McGill-course-req-visualizer/blob/main/McGill-course-req-visualizer/assets/step_3.png) 

**Step 4.** \
Enter the course that you would like to visualize. \
![step_4.png](https://github.com/OwenLeSann/McGill-course-req-visualizer/blob/main/McGill-course-req-visualizer/assets/step_4.png) 

**Step 5.** \
Your graph (named course_tree.png by default) should appear in the McGill-course-req-visualizer directory, click on it to view the prerequistes and corequisites associated with your course! \
![step_5.png](https://github.com/OwenLeSann/McGill-course-req-visualizer/blob/main/McGill-course-req-visualizer/assets/step_5.png)

## Gallery
![MATH 316.png](https://github.com/OwenLeSann/McGill-course-req-visualizer/blob/main/McGill-course-req-visualizer/assets/MATH%20316.png) 

![CHEM 502.png](https://github.com/OwenLeSann/McGill-course-req-visualizer/blob/main/McGill-course-req-visualizer/assets/CHEM%20502.png) 

![COMP 551.png](https://github.com/OwenLeSann/McGill-course-req-visualizer/blob/main/McGill-course-req-visualizer/assets/COMP%20551.png) 

## Author
Owen Le Sann

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/OwenLeSann/McGill-course-req-visualizer/blob/main/LICENSE) file for details.


