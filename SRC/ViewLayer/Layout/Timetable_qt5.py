# layout_timetable.py - PyQt5 Version
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QFrame, 
                             QSizePolicy, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette

# Import from your logic file
from SRC.ViewLayer.Logic.TimeTable import DAYS, HOURS


def get_lesson_type_color_class(lesson_type):
    """Return CSS class name based on lesson type"""
    type_classes = {
        "Lecture": "lectureCell",
        "Lab": "labCell", 
        "Exercise": "exerciseCell"
    }
    return type_classes.get(lesson_type, "defaultCell")


def format_course_info(course_data):
    """Format course information for display in cell"""
    lines = []
    
    # Course code (first line)
    if course_data.get("code"):
        lines.append(course_data["code"])
    
    # Course name (second line, truncated if too long)
    if course_data.get("name"):
        name = course_data["name"]
        if len(name) > 20:
            name = name[:17] + "..."
        lines.append(name)
    
    # Lesson type (third line)
    if course_data.get("type"):
        lines.append(course_data["type"])
    
    # Location (fourth line)
    if course_data.get("location"):
        lines.append(course_data["location"])
    
    return '\n'.join(lines)


def get_tooltip_text(course_data):
    """Generate tooltip text with full course details"""
    tooltip_parts = []
    
    if course_data.get("name"):
        tooltip_parts.append(f"Course: {course_data['name']}")
    
    if course_data.get("code"):
        tooltip_parts.append(f"Code: {course_data['code']}")
    
    if course_data.get("type"):
        tooltip_parts.append(f"Type: {course_data['type']}")
    
    if course_data.get("location"):
        tooltip_parts.append(f"Location: {course_data['location']}")
    
    return '\n'.join(tooltip_parts)


class TimetableGridWidget(QWidget):
    """Custom widget for displaying the timetable grid"""
    
    def __init__(self, slot_map, parent=None):
        super().__init__(parent)
        self.slot_map = slot_map
        self.setObjectName("timetableGrid")
        self.init_ui()
    
    def init_ui(self):
        """Initialize the timetable grid UI"""
        # Main grid layout
        grid_layout = QGridLayout()
        grid_layout.setSpacing(3)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        
        # Set size policies for responsive design
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Create header row (days)
        self.create_header_row(grid_layout)
        
        # Create time column and timetable cells
        self.create_timetable_cells(grid_layout)
        
        self.setLayout(grid_layout)
    
    def create_header_row(self, grid_layout):
        """Create the header row with day names"""
        # Empty cell in top-left corner
        empty_cell = self.create_empty_header_cell()
        grid_layout.addWidget(empty_cell, 0, 0)
        
        # Day headers
        for col, day in enumerate(DAYS, start=1):
            day_cell = self.create_day_header_cell(day)
            grid_layout.addWidget(day_cell, 0, col)
    
    def create_timetable_cells(self, grid_layout):
        """Create the time column and timetable content cells"""
        for row, hour in enumerate(HOURS, start=1):
            # Time cell (left column)
            time_cell = self.create_time_cell(f"{hour}:00")
            grid_layout.addWidget(time_cell, row, 0)
            
            # Content cells for each day
            for col, day in enumerate(DAYS, start=1):
                course_data = self.slot_map.get((day, hour))
                cell = self.create_course_cell(course_data)
                grid_layout.addWidget(cell, row, col)
    
    def create_empty_header_cell(self):
        """Create the empty cell in the top-left corner"""
        cell = QFrame()
        cell.setObjectName("emptyCell")
        cell.setFixedSize(180, 80)
        return cell
    
    def create_day_header_cell(self, day):
        """Create a day header cell"""
        cell = QFrame()
        cell.setObjectName("dayHeader")
        cell.setFixedSize(180, 80)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setAlignment(Qt.AlignCenter)
        
        label = QLabel(day)
        label.setObjectName("dayHeaderLabel")
        label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(label)
        cell.setLayout(layout)
        
        return cell
    
    def create_time_cell(self, time_text):
        """Create a time cell for the left column"""
        cell = QFrame()
        cell.setObjectName("timeCell")
        cell.setFixedSize(180, 80)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setAlignment(Qt.AlignCenter)
        
        label = QLabel(time_text)
        label.setObjectName("timeCellLabel")
        label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(label)
        cell.setLayout(layout)
        
        return cell
    
    def create_course_cell(self, course_data):
        """Create a course cell (either empty or with course information)"""
        cell = QFrame()
        cell.setFixedSize(180, 80)
        
        if course_data:
            # Set the appropriate style based on lesson type
            lesson_type = course_data.get("type", "")
            cell_class = get_lesson_type_color_class(lesson_type)
            cell.setObjectName(cell_class)
            
            # Create layout for course information
            layout = QVBoxLayout()
            layout.setContentsMargins(6, 6, 6, 6)
            layout.setSpacing(2)
            
            # Format and display course information
            course_text = format_course_info(course_data)
            lines = course_text.split('\n')
            
            # Course code/name (bold, slightly larger)
            if lines:
                name_label = QLabel(lines[0])
                name_label.setObjectName("courseNameLabel")
                name_label.setAlignment(Qt.AlignCenter)
                name_label.setWordWrap(True)
                layout.addWidget(name_label)
                
                # Other information
                if len(lines) > 1:
                    info_text = '\n'.join(lines[1:])
                    info_label = QLabel(info_text)
                    info_label.setObjectName("courseCellLabel")
                    info_label.setAlignment(Qt.AlignCenter)
                    info_label.setWordWrap(True)
                    layout.addWidget(info_label)
            
            # Set tooltip with detailed information
            tooltip_text = get_tooltip_text(course_data)
            cell.setToolTip(tooltip_text)
            
        else:
            # Empty cell
            cell.setObjectName("emptyCell")
            layout = QVBoxLayout()
            layout.setContentsMargins(6, 6, 6, 6)
        
        cell.setLayout(layout)
        return cell


class CompactTimetableWidget(QWidget):
    """A more compact version of the timetable for smaller displays"""
    
    def __init__(self, slot_map, parent=None):
        super().__init__(parent)
        self.slot_map = slot_map
        self.setObjectName("compactTimetableGrid")
        self.init_ui()
    
    def init_ui(self):
        """Initialize the compact timetable UI"""
        grid_layout = QGridLayout()
        grid_layout.setSpacing(2)
        grid_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create header row with smaller cells
        empty_cell = QFrame()
        empty_cell.setObjectName("emptyCell")
        empty_cell.setFixedSize(120, 50)
        grid_layout.addWidget(empty_cell, 0, 0)
        
        # Day headers (compact)
        for col, day in enumerate(DAYS, start=1):
            day_cell = QFrame()
            day_cell.setObjectName("dayHeader")
            day_cell.setFixedSize(120, 50)
            
            layout = QVBoxLayout()
            layout.setContentsMargins(4, 4, 4, 4)
            layout.setAlignment(Qt.AlignCenter)
            
            # Use abbreviated day names for compact view
            abbreviated_day = day[:3]
            label = QLabel(abbreviated_day)
            label.setObjectName("dayHeaderLabel")
            label.setAlignment(Qt.AlignCenter)
            
            layout.addWidget(label)
            day_cell.setLayout(layout)
            grid_layout.addWidget(day_cell, 0, col)
        
        # Create time column and cells (compact)
        for row, hour in enumerate(HOURS, start=1):
            # Time cell
            time_cell = QFrame()
            time_cell.setObjectName("timeCell")
            time_cell.setFixedSize(120, 50)
            
            layout = QVBoxLayout()
            layout.setContentsMargins(4, 4, 4, 4)
            layout.setAlignment(Qt.AlignCenter)
            
            label = QLabel(f"{hour}:00")
            label.setObjectName("timeCellLabel")
            label.setAlignment(Qt.AlignCenter)
            
            layout.addWidget(label)
            time_cell.setLayout(layout)
            grid_layout.addWidget(time_cell, row, 0)
            
            # Course cells (compact)
            for col, day in enumerate(DAYS, start=1):
                course_data = self.slot_map.get((day, hour))
                cell = self.create_compact_course_cell(course_data)
                grid_layout.addWidget(cell, row, col)
        
        self.setLayout(grid_layout)
    
    def create_compact_course_cell(self, course_data):
        """Create a compact course cell"""
        cell = QFrame()
        cell.setFixedSize(120, 50)
        
        if course_data:
            lesson_type = course_data.get("type", "")
            cell_class = get_lesson_type_color_class(lesson_type)
            cell.setObjectName(cell_class)
            
            layout = QVBoxLayout()
            layout.setContentsMargins(3, 3, 3, 3)
            layout.setSpacing(1)
            
            # Show only course code and type in compact view
            course_code = course_data.get("code", "")
            lesson_type = course_data.get("type", "")
            
            if course_code:
                code_label = QLabel(course_code)
                code_label.setObjectName("courseNameLabel")
                code_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(code_label)
            
            if lesson_type:
                # Abbreviate lesson types
                type_abbrev = {
                    "Lecture": "LEC",
                    "Lab": "LAB", 
                    "Exercise": "EX"
                }.get(lesson_type, lesson_type[:4])
                
                type_label = QLabel(type_abbrev)
                type_label.setObjectName("courseCellLabel")
                type_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(type_label)
            
            # Full tooltip for details
            tooltip_text = get_tooltip_text(course_data)
            cell.setToolTip(tooltip_text)
            
        else:
            cell.setObjectName("emptyCell")
            layout = QVBoxLayout()
            layout.setContentsMargins(3, 3, 3, 3)
        
        cell.setLayout(layout)
        return cell


# Helper function to choose the appropriate widget based on available space
def create_timetable_widget(slot_map, compact=False, parent=None):
    """Factory function to create appropriate timetable widget"""
    if compact:
        return CompactTimetableWidget(slot_map, parent)
    else:
        return TimetableGridWidget(slot_map, parent)