# layout_timetable.py - PyQt5 Version

from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QFrame,
                             QSizePolicy, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt, QSize  
from PyQt5.QtGui import QFont, QPalette 
from SRC.ViewLayer.Logic.TimeTable import DAYS, HOURS

def get_lesson_type_color_class(lesson_type):
   # Dictionary mapping lesson types to their corresponding CSS class names
    type_classes = {
        "Lecture": "lectureCell",  
        "Lab": "labCell",         
        "Exercise": "exerciseCell", 
        "Reinforcement": "reinforcementCell", 
        "Training": "trainingCell",  
        "DepartmentHour": "departmentHourCell",  
        "default": "defaultCell"  
        
    }
    # Return the class for the given lesson_type, or "defaultCell" if not found
    return type_classes.get(lesson_type, "defaultCell")


def format_course_info(course_data):
    lines = []  # Initialize an empty list to store lines of text

    # Add course code if available (first line)
    if course_data.get("code"): 
        lines.append(course_data["code"])

    # Add course name if available (second line)
    if course_data.get("name"):
        name = course_data["name"]
        # Truncate long course names to fit in the cell
        if len(name) > 20:  # Check if the name is longer than 20 characters
            name = name[:17] + "..."  # Take the first 17 characters and add an ellipsis
        lines.append(name)

   
    if course_data.get("type") and not course_data.get("code", "").startswith("BLOCKED"):
        lines.append(course_data["type"])

    
    if course_data.get("location"):
        lines.append(course_data["location"])

    # Join the lines with newline characters to create a multi-line string
    return '\n'.join(lines)


def get_tooltip_text(course_data):
    """
    Generate a more detailed tooltip text with full course details.
    This text appears when the user hovers over a course cell.

    Args:
        course_data (dict): A dictionary containing course details.

    Returns:
        str: A formatted multi-line string for the tooltip.
    """
    tooltip_parts = []  # Initialize an empty list for tooltip lines

    # Add full course name if available
    if course_data.get("name"):
        tooltip_parts.append(f"Course: {course_data['name']}")

    # Add course code if available
    if course_data.get("code"):
        tooltip_parts.append(f"Code: {course_data['code']}")

    # Add lesson type if available
    if course_data.get("type"):
        tooltip_parts.append(f"Type: {course_data['type']}")

    # Add location if available
    if course_data.get("location"):
        tooltip_parts.append(f"Location: {course_data['location']}")
    if course_data.get("teacher"):
        if isinstance(course_data['teachers'], list):
            for teacher in course_data['teachers']:
                tooltip_parts.append(f"Teacher: {teacher}")

    # Join the parts with newline characters for a multi-line tooltip
    return '\n'.join(tooltip_parts)


class TimetableGridWidget(QWidget):
    """
    Custom QWidget for displaying the main timetable grid.
    This widget arranges course information in a grid of days and hours.
    """

    def __init__(self, slot_map, editing_mode=False, on_available_click=None, on_selected_lesson_click = None, parent=None):
        """
        Constructor for TimetableGridWidget.

        Args:
            slot_map (dict): A dictionary mapping (day, hour) tuples to
                             course data dictionaries.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)  
        self.slot_map = slot_map  # Store the course data
        self.editing_mode = editing_mode
        self.on_available_click = on_available_click  # Save callback for clicking available cell
        self.on_selected_lesson_click = on_selected_lesson_click # Save callback for clicking edited lesson
        # Set an object name for styling with Qt Style Sheets (QSS)
        self.setObjectName("timetableGrid")
        self.init_ui()  # Initialize the user interface components

    def init_ui(self):
        """
        Initialize the timetable grid UI.
        This involves creating the main layout and populating it with
        header cells and timetable cells.
        """
        # Create a QGridLayout to arrange cells in rows and columns
        # grid_layout = QGridLayout()
        # grid_layout.setSpacing(3)  
        # grid_layout.setContentsMargins(10, 10, 10, 10)
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(3)  
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        
        # Set size policies to allow the widget to expand and fill available space

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create the header row 
        self.create_header_row(self.grid_layout)

        # Create the time column and the main timetable cells
        self.create_timetable_cells(self.grid_layout)

        # Set the grid_layout as the main layout for this widget
        self.setLayout(self.grid_layout)


    def create_header_row(self, grid_layout):
        """
        Create the header row of the timetable, which displays the day names.

        Args:
            grid_layout (QGridLayout): The layout to which header cells will be added.
        """
        # Create an empty cell for the top-left corner of the grid (above time column)
        empty_cell = self.create_empty_header_cell()
        # Add the empty cell to the grid at position (0, 0)
        grid_layout.addWidget(empty_cell, 0, 0)

        # Iterate over the DAYS constant (e.g., ["Sunday", "Monday", ...])
        # 'start=1' because column 0 is for the time labels
        for col, day in enumerate(DAYS, start=1):
            # Create a QFrame styled as a day header cell
            day_cell = self.create_day_header_cell(day)
            # Add the day header cell to the grid at row 0 and the current column
            grid_layout.addWidget(day_cell, 0, col)

    def create_timetable_cells(self, grid_layout):
        """
        Create the time column cells and the main content cells for courses.

        Args:
            grid_layout (QGridLayout): The layout to which cells will be added.
        """
        # Iterate over the HOURS constant (e.g., [8, 9, 10, ...])
        # 'start=1' because row 0 is for the day headers
        for row, hour in enumerate(HOURS, start=1):
            # Create a QFrame styled as a time cell (e.g., "8:00")
            time_cell = self.create_time_cell(f"{hour}:00")
            # Add the time cell to the grid at the current row and column 0
            grid_layout.addWidget(time_cell, row, 0)

            # For each hour, iterate over the DAYS to create course cells
            for col, day in enumerate(DAYS, start=1):
                # Retrieve course data for the current day and hour from slot_map
                # slot_map is expected to be a dict like {(day, hour): course_info_dict}
                course_data = self.slot_map.get((day, hour))
                # Create a course cell (either empty or with course info)
                cell = self.create_course_cell(course_data, day, hour)
                # Add the course cell to the grid at the current row and column
                grid_layout.addWidget(cell, row, col)

    def create_empty_header_cell(self):
        cell = QFrame()  
        cell.setObjectName("emptyCell")  
        cell.setFixedSize(150, 90)  
        return cell

    def create_day_header_cell(self, day):
        cell = QFrame()  
        cell.setObjectName("dayHeader")
        cell.setFixedSize(150, 90)

        # Use a QVBoxLayout to center the label within the frame
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)  
        layout.setAlignment(Qt.AlignCenter)    

        label = QLabel(day)  # Create a QLabel with the day's name
        label.setObjectName("dayHeaderLabel")  
        label.setAlignment(Qt.AlignCenter)   

        layout.addWidget(label)
        cell.setLayout(layout)  
        return cell

    def create_time_cell(self, time_text):
        """
        Create a QFrame that acts as a time indicator cell in the first column.
        It contains a QLabel with the time string.

        Args:
            time_text (str): The time to display (e.g., "08:00").

        Returns:
            QFrame: The configured time cell.
        """
        cell = QFrame() 
        cell.setObjectName("timeCell") 
        cell.setFixedSize(150, 90) 

        # Use a QVBoxLayout to center the label within the frame
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setAlignment(Qt.AlignCenter)  

        label = QLabel(time_text)  # Create a QLabel with the time text
        label.setObjectName("timeCellLabel")  
        label.setAlignment(Qt.AlignCenter) 

        layout.addWidget(label)  # Add the label to the layout
        cell.setLayout(layout)   # Set the layout for the frame
        return cell

    def create_course_cell(self, course_data, day=None, hour=None):
        cell = QFrame() 
        cell.setFixedSize(150, 90) 

        layout = QVBoxLayout() 
        layout.setContentsMargins(6, 6, 6, 6) # Margins inside the cell

        if course_data:  # If there is course data for this slot
            # Determine the CSS class for styling based on lesson type
            #lesson_type = course_data.get("type", "")  # Get lesson type, default to empty string
            #cell_class = get_lesson_type_color_class(lesson_type)
            # cell.setObjectName(cell_class)  # Apply the class name for styling

            lesson_type = course_data.get("type", "")
            is_blocked = course_data.get("code", "").startswith("BLOCKED")
            is_available = course_data.get("type") == "available"  # Check if the course type is "available"

            if is_blocked:
                cell.setObjectName("blockedCell")
            elif is_available:
                cell.setObjectName("availableCell")
            else:
                cell_class = get_lesson_type_color_class(lesson_type)
                cell.setObjectName(cell_class)
                
                if self.editing_mode and self.on_selected_lesson_click:
                    cell.setProperty("customTag", "manual_selected")
                    cell.setCursor(Qt.PointingHandCursor)
                    cell.mouseReleaseEvent = lambda event: self.on_selected_lesson_click(course_data.get("code", ""), course_data.get("lesson", ""))
    
            if self.editing_mode and course_data.get("matches requested lesson",""):
                if course_data.get("scheduled", ""):
                    cell.setProperty("customTag", "requested_and_scheduled")
                else:
                    cell.setObjectName("requestedCell")



            layout.setSpacing(2) 
            # Format the course information for display
            course_text = format_course_info(course_data)
            lines = course_text.split('\n')  

            # Display course code/name (f
            if lines:  # If there's at least one line of text
                name_label = QLabel(lines[0])  
                if is_blocked:
                    name_label.setObjectName("blockedLabel")
                else:
                    name_label.setObjectName("courseNameLabel")
                                                                
                name_label.setAlignment(Qt.AlignCenter)     
                name_label.setWordWrap(True)                 
                layout.addWidget(name_label)                 

                # Display other information (remaining lines)
                if len(lines) > 1 and not is_available:  # If there are more lines
                    info_text = '\n'.join(lines[1:])  
                    info_label = QLabel(info_text)    # Create label for additional info
                    info_label.setObjectName("courseCellLabel") 
                    info_label.setAlignment(Qt.AlignCenter) 
                    info_label.setWordWrap(True)             
                    layout.addWidget(info_label)             

            if not is_available:
                # Set a tooltip with more detailed information for the cell
                tooltip_text = get_tooltip_text(course_data)
                cell.setToolTip(tooltip_text)
            
            if is_available:
                tooltip_parts = []
                for lesson in course_data['lessons']:
                    tooltip_parts.append(f"{lesson['name']} ({lesson['code']}) - {lesson['type']} | {lesson['location']}")
                tooltip_text = '\n'.join(tooltip_parts)
                cell.setToolTip(tooltip_text)

            # add clickable behavior only for 'available' cells and only if a handler is provided
            if is_available and self.on_available_click:
                cell.setCursor(Qt.PointingHandCursor)
                cell.mouseReleaseEvent = lambda event: self.on_available_click(day, hour)

        else:  # If there is no course data for this slot (empty cell)
            cell.setObjectName("emptyCell")  # Style as an empty cell

        cell.setLayout(layout)  # Apply the layout to the cell
        return cell

    def update_timetable(self, new_slot_map):
        """
        Update the timetable with a new slot map.

        Args:
            new_slot_map (dict): A new dictionary mapping (day, hour) tuples to course data.
        """
        self.slot_map = new_slot_map
        
        # Clean existing course cells (but leave header row and time column)
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            position = self.grid_layout.getItemPosition(i)
            row, col = position[0], position[1]
            if row != 0 and col != 0:  # Don't delete headers
                widget.setParent(None)

        # Re-create only the timetable cells (not headers)
        self.create_timetable_cells(self.grid_layout)