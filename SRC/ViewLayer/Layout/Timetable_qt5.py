# layout_timetable.py - PyQt5 Version

# Import necessary PyQt5 modules for creating the GUI
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QFrame,
                             QSizePolicy, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt, QSize  # Qt for alignment and other core functionalities, QSize for size definitions
from PyQt5.QtGui import QFont, QPalette # QFont for text styling, QPalette for widget colors (though not directly used here, good to have for potential theming)

# Import constants (DAYS, HOURS) from your application's logic file
# This helps in separating the UI from the data/logic
from SRC.ViewLayer.Logic.TimeTable import DAYS, HOURS

#מקביל  לשורה 102
def get_lesson_type_color_class(lesson_type):
   # Dictionary mapping lesson types to their corresponding CSS class names
    type_classes = {
        "Lecture": "lectureCell",  # Class for lecture cells
        "Lab": "labCell",          # Class for lab cells
        "Exercise": "exerciseCell", # Class for exercise cells
        "Reinforcement": "reinforcementCell",  # Class for reinforcement cells
        "Training": "trainingCell",  # Class for training cells
        "DepartmentHour": "departmentHourCell",  # Class for department hour cells
        "default": "defaultCell"   # Default class for any other type or if not specified
        
    }
    # Return the class for the given lesson_type, or "defaultCell" if not found
    return type_classes.get(lesson_type, "defaultCell")

#מקביל לשורה 109
def format_course_info(course_data):
    lines = []  # Initialize an empty list to store lines of text

    # Add course code if available (first line)
    if course_data.get("code"):  # Safely get "code", returns None if key doesn't exist
        lines.append(course_data["code"])

    # Add course name if available (second line)
    if course_data.get("name"):
        name = course_data["name"]
        # Truncate long course names to fit in the cell
        if len(name) > 20:  # Check if the name is longer than 20 characters
            name = name[:17] + "..."  # Take the first 17 characters and add an ellipsis
        lines.append(name)

    # Add lesson type if available (third line)
    if course_data.get("type") and not course_data.get("code", "").startswith("BLOCKED_"):
        lines.append(course_data["type"])

    # Add location if available (fourth line)
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

    # Join the parts with newline characters for a multi-line tooltip
    return '\n'.join(tooltip_parts)


class TimetableGridWidget(QWidget):
    """
    Custom QWidget for displaying the main timetable grid.
    This widget arranges course information in a grid of days and hours.
    """

    def __init__(self, slot_map, parent=None):
        """
        Constructor for TimetableGridWidget.

        Args:
            slot_map (dict): A dictionary mapping (day, hour) tuples to
                             course data dictionaries.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)  # Call the QWidget constructor
        self.slot_map = slot_map  # Store the course data
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
        grid_layout = QGridLayout()
        grid_layout.setSpacing(3)  # Set spacing between cells to 3 pixels
        # Set margins around the grid layout (left, top, right, bottom)
        grid_layout.setContentsMargins(10, 10, 10, 10)

        # Set size policies to allow the widget to expand and fill available space
        # QSizePolicy.Expanding means the widget can grow if space is available.
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create the header row (displaying days of the week)
        self.create_header_row(grid_layout)

        # Create the time column (displaying hours) and the main timetable cells
        self.create_timetable_cells(grid_layout)

        # Set the grid_layout as the main layout for this widget
        self.setLayout(grid_layout)

#מקביל לשוה 64
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
                course_data = self.slot_map.get((day, hour)) # Returns None if no course at this slot
                # Create a course cell (either empty or with course info)
                cell = self.create_course_cell(course_data)
                # Add the course cell to the grid at the current row and column
                grid_layout.addWidget(cell, row, col)

    def create_empty_header_cell(self):
        cell = QFrame()  # Create a new QFrame
        cell.setObjectName("emptyCell")  # Set object name for QSS styling
        cell.setFixedSize(150, 90)  # Set a fixed size for this cell
        return cell

    def create_day_header_cell(self, day):
        cell = QFrame()  # Create a new QFrame
        cell.setObjectName("dayHeader")  # Set object name for QSS styling
        cell.setFixedSize(150, 90)  # Set a fixed size

        # Use a QVBoxLayout to center the label within the frame
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)  # Margins inside the cell
        layout.setAlignment(Qt.AlignCenter)    # Align content to the center

        label = QLabel(day)  # Create a QLabel with the day's name
        label.setObjectName("dayHeaderLabel")  # Set object name for QSS styling of the label
        label.setAlignment(Qt.AlignCenter)     # Center the text within the label

        layout.addWidget(label)  # Add the label to the layout
        cell.setLayout(layout)   # Set the layout for the frame
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
        cell = QFrame()  # Create a new QFrame
        cell.setObjectName("timeCell")  # Set object name for QSS styling
        cell.setFixedSize(150, 90)  # Set a fixed size

        # Use a QVBoxLayout to center the label within the frame
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)  # Margins inside the cell
        layout.setAlignment(Qt.AlignCenter)    # Align content to the center

        label = QLabel(time_text)  # Create a QLabel with the time text
        label.setObjectName("timeCellLabel")  # Set object name for QSS styling of the label
        label.setAlignment(Qt.AlignCenter)    # Center the text within the label

        layout.addWidget(label)  # Add the label to the layout
        cell.setLayout(layout)   # Set the layout for the frame
        return cell

    def create_course_cell(self, course_data):
        cell = QFrame()  # Create a new QFrame
        cell.setFixedSize(150, 90)  # Set a fixed size for the cell

        layout = QVBoxLayout()  # Layout for the cell's content
        layout.setContentsMargins(6, 6, 6, 6) # Margins inside the cell

        if course_data:  # If there is course data for this slot
            # Determine the CSS class for styling based on lesson type
            #lesson_type = course_data.get("type", "")  # Get lesson type, default to empty string
            #cell_class = get_lesson_type_color_class(lesson_type)
            # cell.setObjectName(cell_class)  # Apply the class name for styling

            lesson_type = course_data.get("type", "")
            is_blocked = course_data.get("code", "").startswith("BLOCKED_")

            if is_blocked:
                cell.setObjectName("blockedCell")
            else:
                cell_class = get_lesson_type_color_class(lesson_type)
                cell.setObjectName(cell_class)


            layout.setSpacing(2)  # Set spacing between widgets in the layout

            # Format the course information for display
            course_text = format_course_info(course_data)
            lines = course_text.split('\n')  # Split into lines for separate labels if needed

            # Display course code/name (first line, potentially styled differently)
            if lines:  # If there's at least one line of text
                name_label = QLabel(lines[0])  # Create label for the first line (code or name)
                if is_blocked:
                    name_label.setObjectName("blockedLabel")
                else:
                    name_label.setObjectName("courseNameLabel")# Style for primary info
                                                                
                name_label.setAlignment(Qt.AlignCenter)       # Center text
                name_label.setWordWrap(True)                 # Allow text to wrap if it's too long
                layout.addWidget(name_label)                 # Add to cell layout

                # Display other information (remaining lines)
                if len(lines) > 1:  # If there are more lines
                    info_text = '\n'.join(lines[1:])  # Join remaining lines
                    info_label = QLabel(info_text)    # Create label for additional info
                    info_label.setObjectName("courseCellLabel") # Style for secondary info
                    info_label.setAlignment(Qt.AlignCenter)    # Center text
                    info_label.setWordWrap(True)              # Allow text to wrap
                    layout.addWidget(info_label)              # Add to cell layout

            # Set a tooltip with more detailed information for the cell
            tooltip_text = get_tooltip_text(course_data)
            cell.setToolTip(tooltip_text)

        else:  # If there is no course data for this slot (empty cell)
            cell.setObjectName("emptyCell")  # Style as an empty cell

        cell.setLayout(layout)  # Apply the layout to the cell
        return cell
