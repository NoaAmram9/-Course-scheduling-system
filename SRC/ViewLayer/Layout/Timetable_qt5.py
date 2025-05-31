# layout_timetable.py - PyQt5 Version

# Import necessary PyQt5 modules for creating the GUI
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QFrame,
                             QSizePolicy, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt, QSize  # Qt for alignment and other core functionalities, QSize for size definitions
from PyQt5.QtGui import QFont, QPalette # QFont for text styling, QPalette for widget colors (though not directly used here, good to have for potential theming)

# Import constants (DAYS, HOURS) from your application's logic file
# This helps in separating the UI from the data/logic
from SRC.ViewLayer.Logic.TimeTable import DAYS, HOURS


def get_lesson_type_color_class(lesson_type):
    """
    Return a CSS-like class name based on the lesson type.
    These class names can be used in stylesheets to apply specific styling
    (e.g., background colors) to different types of lessons.

    Args:
        lesson_type (str): The type of the lesson (e.g., "Lecture", "Lab").

    Returns:
        str: The CSS class name corresponding to the lesson type,
             or "defaultCell" if the type is not recognized.
    """
    # Dictionary mapping lesson types to their corresponding CSS class names
    type_classes = {
        "Lecture": "lectureCell",  # Class for lecture cells
        "Lab": "labCell",          # Class for lab cells
        "Exercise": "exerciseCell" # Class for exercise cells
    }
    # Return the class for the given lesson_type, or "defaultCell" if not found
    return type_classes.get(lesson_type, "defaultCell")


def format_course_info(course_data):
    """
    Format course information for display within a timetable cell.
    This function takes a dictionary of course data and prepares a
    multi-line string suitable for a QLabel.

    Args:
        course_data (dict): A dictionary containing course details like
                            "code", "name", "type", and "location".

    Returns:
        str: A formatted multi-line string with course information.
    """
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
    if course_data.get("type"):
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
        """
        Create the empty QFrame for the top-left corner of the timetable.
        This cell has a fixed size and an object name for styling.

        Returns:
            QFrame: The configured empty header cell.
        """
        cell = QFrame()  # Create a new QFrame
        cell.setObjectName("emptyCell")  # Set object name for QSS styling
        cell.setFixedSize(180, 80)  # Set a fixed size for this cell
        return cell

    def create_day_header_cell(self, day):
        """
        Create a QFrame that acts as a header cell for a specific day.
        It contains a QLabel with the day's name.

        Args:
            day (str): The name of the day (e.g., "Monday").

        Returns:
            QFrame: The configured day header cell.
        """
        cell = QFrame()  # Create a new QFrame
        cell.setObjectName("dayHeader")  # Set object name for QSS styling
        cell.setFixedSize(180, 80)  # Set a fixed size

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
        cell.setFixedSize(180, 80)  # Set a fixed size

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
        """
        Create a QFrame representing a single course slot in the timetable.
        If course_data is provided, it displays formatted course information.
        Otherwise, it's an empty styled cell.

        Args:
            course_data (dict or None): A dictionary with course details,
                                        or None if the slot is empty.

        Returns:
            QFrame: The configured course cell.
        """
        cell = QFrame()  # Create a new QFrame
        cell.setFixedSize(180, 80)  # Set a fixed size for the cell

        layout = QVBoxLayout()  # Layout for the cell's content
        layout.setContentsMargins(6, 6, 6, 6) # Margins inside the cell

        if course_data:  # If there is course data for this slot
            # Determine the CSS class for styling based on lesson type
            lesson_type = course_data.get("type", "")  # Get lesson type, default to empty string
            cell_class = get_lesson_type_color_class(lesson_type)
            cell.setObjectName(cell_class)  # Apply the class name for styling

            layout.setSpacing(2)  # Set spacing between widgets in the layout

            # Format the course information for display
            course_text = format_course_info(course_data)
            lines = course_text.split('\n')  # Split into lines for separate labels if needed

            # Display course code/name (first line, potentially styled differently)
            if lines:  # If there's at least one line of text
                name_label = QLabel(lines[0])  # Create label for the first line (code or name)
                name_label.setObjectName("courseNameLabel")  # Style for primary info
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


class CompactTimetableWidget(QWidget):
    """
    A more compact version of the timetable, suitable for smaller displays
    or when a less detailed overview is needed. Cells are smaller, and
    information is more condensed.
    """

    def __init__(self, slot_map, parent=None):
        """
        Constructor for CompactTimetableWidget.

        Args:
            slot_map (dict): A dictionary mapping (day, hour) tuples to
                             course data dictionaries.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)  # Call the QWidget constructor
        self.slot_map = slot_map  # Store the course data
        # Set an object name for styling with Qt Style Sheets (QSS)
        self.setObjectName("compactTimetableGrid")
        self.init_ui()  # Initialize the user interface components

    def init_ui(self):
        """
        Initialize the compact timetable UI.
        This involves creating a grid layout and populating it with
        smaller header and course cells.
        """
        grid_layout = QGridLayout()  # Main layout for the compact grid
        grid_layout.setSpacing(2)    # Reduced spacing for a compact look
        grid_layout.setContentsMargins(5, 5, 5, 5)  # Reduced margins

        # Create header row with smaller cells
        # Empty cell in top-left corner (smaller)
        empty_cell = QFrame()
        empty_cell.setObjectName("emptyCell") # For styling
        empty_cell.setFixedSize(120, 50)      # Smaller fixed size
        grid_layout.addWidget(empty_cell, 0, 0) # Add to grid (0,0)

        # Day headers (compact version)
        for col, day in enumerate(DAYS, start=1): # Iterate through days, starting column 1
            day_cell = QFrame()
            day_cell.setObjectName("dayHeader") # For styling
            day_cell.setFixedSize(120, 50)      # Smaller fixed size

            layout = QVBoxLayout()             # Layout for the day cell content
            layout.setContentsMargins(4, 4, 4, 4) # Smaller margins
            layout.setAlignment(Qt.AlignCenter)   # Center content

            # Use abbreviated day names (e.g., "Mon" instead of "Monday")
            abbreviated_day = day[:3] # Take the first 3 characters of the day name
            label = QLabel(abbreviated_day)
            label.setObjectName("dayHeaderLabel") # For styling the label
            label.setAlignment(Qt.AlignCenter)    # Center text in label

            layout.addWidget(label)
            day_cell.setLayout(layout)
            grid_layout.addWidget(day_cell, 0, col) # Add to header row

        # Create time column and course cells (compact version)
        for row, hour in enumerate(HOURS, start=1): # Iterate through hours, starting row 1
            # Time cell (left column, smaller)
            time_cell = QFrame()
            time_cell.setObjectName("timeCell") # For styling
            time_cell.setFixedSize(120, 50)     # Smaller fixed size

            layout = QVBoxLayout()             # Layout for the time cell content
            layout.setContentsMargins(4, 4, 4, 4) # Smaller margins
            layout.setAlignment(Qt.AlignCenter)   # Center content

            label = QLabel(f"{hour}:00")      # Display hour (e.g., "8:00")
            label.setObjectName("timeCellLabel") # For styling the label
            label.setAlignment(Qt.AlignCenter)    # Center text

            layout.addWidget(label)
            time_cell.setLayout(layout)
            grid_layout.addWidget(time_cell, row, 0) # Add to the first column

            # Course cells (compact version)
            for col, day in enumerate(DAYS, start=1): # Iterate through days for each hour
                course_data = self.slot_map.get((day, hour)) # Get course data for this slot
                # Create a compact course cell
                cell = self.create_compact_course_cell(course_data)
                grid_layout.addWidget(cell, row, col) # Add to the grid

        self.setLayout(grid_layout) # Set the main layout for this widget

    def create_compact_course_cell(self, course_data):
        """
        Create a compact QFrame for displaying course information.
        Shows only essential details like course code and abbreviated lesson type.

        Args:
            course_data (dict or None): Course details or None for empty slot.

        Returns:
            QFrame: The configured compact course cell.
        """
        cell = QFrame()
        cell.setFixedSize(120, 50) # Smaller fixed size for compact cells

        layout = QVBoxLayout() # Layout for cell content
        layout.setContentsMargins(3, 3, 3, 3) # Even smaller margins
        layout.setSpacing(1)                  # Minimal spacing

        if course_data: # If there's data for this course slot
            lesson_type = course_data.get("type", "") # Get lesson type
            # Get the CSS class for styling based on lesson type
            cell_class = get_lesson_type_color_class(lesson_type)
            cell.setObjectName(cell_class) # Apply styling

            # In compact view, show only course code and lesson type (abbreviated)
            course_code = course_data.get("code", "") # Get course code
            # lesson_type is already fetched above

            if course_code: # If course code exists
                code_label = QLabel(course_code)
                code_label.setObjectName("courseNameLabel") # Use a consistent name for primary info, styling might make it smaller
                code_label.setAlignment(Qt.AlignCenter)    # Center text
                layout.addWidget(code_label)              # Add to layout

            if lesson_type: # If lesson type exists
                # Abbreviate lesson types for compact view
                type_abbrev = {
                    "Lecture": "LEC",
                    "Lab": "LAB",
                    "Exercise": "EX"
                }.get(lesson_type, lesson_type[:4]) # Get abbreviation or first 4 chars

                type_label = QLabel(type_abbrev)
                type_label.setObjectName("courseCellLabel") # Use a consistent name for secondary info
                type_label.setAlignment(Qt.AlignCenter)     # Center text
                layout.addWidget(type_label)                # Add to layout

            # Tooltip should still show full details, even in compact view
            tooltip_text = get_tooltip_text(course_data)
            cell.setToolTip(tooltip_text)

        else: # If it's an empty slot
            cell.setObjectName("emptyCell") # Style as an empty cell
            # The layout is already created, no content needed for empty cell

        cell.setLayout(layout) # Apply the layout to the cell
        return cell


# Helper function (Factory pattern) to choose and create the appropriate timetable widget
def create_timetable_widget(slot_map, compact=False, parent=None):
    """
    Factory function to create either a standard or a compact timetable widget.
    This allows easy switching between timetable views based on preference or
    available screen space.

    Args:
        slot_map (dict): The course data map {(day, hour): course_info}.
        compact (bool, optional): If True, creates a CompactTimetableWidget.
                                  Otherwise, creates a TimetableGridWidget.
                                  Defaults to False.
        parent (QWidget, optional): The parent widget. Defaults to None.

    Returns:
        QWidget: An instance of either TimetableGridWidget or CompactTimetableWidget.
    """
    if compact:
        # If compact mode is requested, return an instance of CompactTimetableWidget
        return CompactTimetableWidget(slot_map, parent)
    else:
        # Otherwise, return an instance of the standard TimetableGridWidget
        return TimetableGridWidget(slot_map, parent)