from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

class CourseDetailsPanelQt5(QWidget):
    # Signal emitted when the user requests to add the course (by its code)
    add_course_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_course = None         # Currently selected course
        self.details_popup = None          # The popup dialog for full details
        self.init_ui()                     # Initialize UI elements

    def init_ui(self):
        """Initialize the layout and widgets of the panel"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Panel title
        title_label = QLabel("Course Details")
        title_label.setObjectName("panelTitle")
        title_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(title_label)

        # Main content frame with custom border/style
        content_frame = QFrame()
        content_frame.setObjectName("detailsFrame")
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(8)
        content_layout.setAlignment(Qt.AlignTop)

        # General course info fields (static labels)
        general_info_fields = [
            ('code_label', "Code: "),
            ('name_label', "Name: "),
            ('semester_label', "Semester: "),
            ('total_credits_label', "Total Credits: "),
            ('total_groups_label', "Groups: ")
        ]

        # Add each info label as a styled row
        for attr, text in general_info_fields:
            self.create_detail_row(content_layout, attr, text)

        # Push content to top by stretching layout
        content_layout.addStretch()
        layout.addWidget(content_frame)

        # Buttons panel for user interaction
        buttons_layout = QHBoxLayout()

        # Button to show additional details popup
        self.details_button = ModernUIQt5.create_button("Additional Details")
        self.details_button.setObjectName("DetailsButton")
        self.details_button.clicked.connect(self.show_details_popup)
        buttons_layout.addWidget(self.details_button)

        # Button to trigger adding the course
        self.add_button = ModernUIQt5.create_button("Add Course")
        self.add_button.setObjectName("UploadButton")
        self.add_button.clicked.connect(self.add_course)
        buttons_layout.addWidget(self.add_button)

        layout.addLayout(buttons_layout)

        # Apply modern UI stylesheet
        self.setStyleSheet(ModernUIQt5.get_main_stylesheet())

    def create_detail_row(self, parent_layout, attr_name, label_text):
        """Create a styled row for a single piece of course info"""
        label = QLabel(label_text)
        label.setObjectName("detailLabel")
        label.setWordWrap(True)

        # Wrap in a frame for styling/margins
        wrapper = QFrame()
        wrapper.setObjectName("detailRowFrame")
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 8, 0, 8)
        wrapper_layout.addWidget(label)

        setattr(self, attr_name, label)  # Save label for future updates
        parent_layout.addWidget(wrapper)
        self.add_separator(parent_layout)

    def add_separator(self, layout):
        """Add a horizontal line separator between info rows"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #FFA500; background-color: #944e25; max-height: 1px;")
        layout.addWidget(line)

    def update_details(self, course):
        """Update the course detail panel with a specific course"""
        self.current_course = course

        if course:
            self.update_general_info(course)
            self.update_lesson_summaries(course)
        else:
            self.clear_all_details()

    def update_general_info(self, course):
        """Update the general labels with course data"""
        self.code_label.setText(f"Code: {course._code}")
        self.name_label.setText(f"Name: {course._name}")
        self.semester_label.setText(f"Semester: {course._semester}")

        total_credits = self._calculate_total_credits(course)
        self.total_credits_label.setText(f"Total Credits: {total_credits}")

        total_groups = self._count_total_groups(course)
        self.total_groups_label.setText(f"Groups: {total_groups}")

    def update_lesson_summaries(self, course):
        """Create summaries for different lesson types in the course"""
        lesson_types = [
            ('lectures', 'Lectures'),
            ('exercises', 'Exercises'),
            ('labs', 'Labs'),
            ('departmentHours', 'Department Hours'),
            ('reinforcement', 'Reinforcement'),
            ('training', 'Training')
        ]

        for attr_name, display_name in lesson_types:
            lessons = getattr(course, attr_name, [])
            count = len(lessons)
            
            if count > 0:
                groups = set()
                instructors = set()
                for lesson in lessons:
                    if hasattr(lesson, 'groupCode') and lesson.groupCode:
                        groups.add(lesson.groupCode)
                    if hasattr(lesson, 'instructors') and lesson.instructors:
                        instructors.update(lesson.instructors)
                
                summary = f"{display_name}: {count} sessions"
                if groups:
                    summary += f" | Groups: {', '.join(map(str, sorted(groups)))}"
                if instructors:
                    instructors_short = ', '.join(list(instructors)[:2])
                    if len(instructors) > 2:
                        instructors_short += f" +{len(instructors)-2} more"
                    summary += f" | Prof: {instructors_short}"
            else:
                summary = f"{display_name}: No sessions"
            

    def on_details_hover(self, event):
        """[DISABLED] Show quick preview on hover (not used)"""
        pass

    def on_details_leave(self, event):
        """[DISABLED] Hide preview when mouse leaves (not used)"""
        pass

    def show_details_tooltip(self):
        """[Not used] Show course details in a small tooltip window"""
        if not self.current_course:
            return

        if not self.details_popup:
            self.details_popup = self.create_details_popup()
        
        self.update_details_popup()
        button_pos = self.details_button.mapToGlobal(self.details_button.rect().bottomLeft())
        self.details_popup.move(button_pos.x(), button_pos.y() + 5)
        self.details_popup.show()

    def show_details_popup(self):
        """Show the full details popup window when clicked"""
        if not self.current_course:
            return

        if not self.details_popup:
            self.details_popup = self.create_details_popup()
        
        self.update_details_popup()

        # Position the popup smartly relative to parent widget
        parent_pos = self.mapToGlobal(self.pos())
        parent_rect = self.rect()
        screen = QApplication.desktop().screenGeometry()
        popup_width = self.details_popup.width()

        if parent_pos.x() + parent_rect.width() + popup_width < screen.width():
            x = parent_pos.x() + parent_rect.width() + 10
        else:
            x = parent_pos.x() - popup_width - 10
        
        y = max(parent_pos.y(), 50)
        self.details_popup.move(x, y)
        self.details_popup.show()
        self.details_popup.raise_()
        self.details_popup.activateWindow()

    def create_details_popup(self):
        """Build and return the detailed QDialog popup window"""
        popup = QDialog(self)
        popup.setWindowTitle("Course Details")
        popup.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        popup.setModal(False)
        popup.resize(650, 550)

        layout = QVBoxLayout(popup)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title inside the popup
        title = QLabel("Detailed Course Information")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #944e25; padding: 10px 0px;")
        layout.addWidget(title)

        # Scroll area for long course details
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Inner content widget inside scroll area
        self.popup_content_widget = QWidget()
        self.popup_main_layout = QVBoxLayout(self.popup_content_widget)
        self.popup_main_layout.setSpacing(15)

        scroll_area.setWidget(self.popup_content_widget)
        layout.addWidget(scroll_area)

        # Close button at the bottom
        close_layout = QHBoxLayout()
        close_layout.addStretch()

        close_btn = ModernUIQt5.create_button("✖ Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #944e25;
            }
        """)
        close_btn.clicked.connect(popup.close)
        close_layout.addWidget(close_btn)
        close_layout.addStretch()

        layout.addLayout(close_layout)
        popup.setStyleSheet(ModernUIQt5.get_main_stylesheet())
        return popup

    def update_details_popup(self):
        """Update the popup with detailed information"""
        # Clear the existing content in the popup layout
        self.clear_layout(self.popup_main_layout)
        
        if not self.current_course:
            return

        course = self.current_course

        # Display notes if available
        if hasattr(course, 'notes') and course.notes:
            notes_frame = QFrame()
            notes_frame.setObjectName("detailsFrame")
            notes_layout = QVBoxLayout(notes_frame)
            notes_layout.setContentsMargins(15, 15, 15, 15)

            # Notes section title
            notes_title = QLabel("Notes")
            notes_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #FFA500;")
            notes_layout.addWidget(notes_title)

            # Notes text content
            notes_text = QLabel(course.notes)
            notes_text.setWordWrap(True)
            notes_text.setStyleSheet("padding: 10px; background-color: #f9f9f9; border-radius: 5px;")
            notes_layout.addWidget(notes_text)

            # Add notes frame to popup layout
            self.popup_main_layout.addWidget(notes_frame)

        # Display each lesson type section with its lessons
        lesson_types = [
            ('lectures', 'Lectures'),
            ('exercises', 'Exercises'),
            ('labs', 'Labs'),
            ('departmentHours', 'Department Hours'),
            ('reinforcement', 'Reinforcement'),
            ('training', 'Training')
        ]

        for attr_name, display_name in lesson_types:
            lessons = getattr(course, attr_name, [])
            if lessons:  # Only include section if it has lessons
                section_widget = self.create_detailed_lesson_section(attr_name, display_name, lessons)
                self.popup_main_layout.addWidget(section_widget)

    def create_detailed_lesson_section(self, attr_name, display_name, lessons):
        """Create a section for a specific type of lesson"""
        frame = QFrame()
        frame.setObjectName("detailsFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Header: lesson type + number of sessions
        header_layout = QHBoxLayout()
        title_label = QLabel(f" {display_name}")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #FFA500;")
        count_label = QLabel(f"({len(lessons)} sessions)")
        count_label.setStyleSheet("color: #888; font-size: 12px;")

        header_layout.addWidget(title_label)
        header_layout.addWidget(count_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Add horizontal separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #FFA500; background-color: #FFA500;")
        layout.addWidget(separator)

        # Add each lesson as a widget
        for i, lesson in enumerate(lessons):
            lesson_widget = self.create_detailed_lesson_widget(lesson, i + 1)
            layout.addWidget(lesson_widget)

        return frame

    def create_detailed_lesson_widget(self, lesson, lesson_number):
        """Create a widget with details for a single lesson"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin: 3px 0px;
            }
        """)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        # Header: session number, group, and lesson type
        header_text = f"Session {lesson_number} - Group {getattr(lesson, 'groupCode', 'N/A')}"
        if hasattr(lesson, 'lesson_type') and lesson.lesson_type:
            header_text += f" ({lesson.lesson_type})"

        header_label = QLabel(header_text)
        header_label.setStyleSheet("font-weight: bold; color: #333; font-size: 12px;")
        layout.addWidget(header_label)

        # Create a grid layout for lesson attributes
        details_widget = QWidget()
        details_layout = QGridLayout(details_widget)
        details_layout.setSpacing(8)
        details_layout.setContentsMargins(5, 5, 5, 5)

        row = 0

        # Time (day and hours)
        if hasattr(lesson, 'time') and lesson.time:
            time_label = QLabel("Time:")
            start_time = f"{lesson.time.start_hour:02d}:00"
            end_time = f"{lesson.time.end_hour:02d}:00"

            # Translate day numbers to Hebrew day names
            days = {
                1: "ראשון", 2: "שני", 3: "שלישי",
                4: "רביעי", 5: "חמישי", 6: "שישי", 7: "שבת"
            }
            day_name = days.get(lesson.time.day, f"יום {lesson.time.day}")
            time_display = f"{day_name}: {start_time} - {end_time}"

            time_value = QLabel(time_display)
            time_label.setStyleSheet("font-weight: bold; color: #555;")
            details_layout.addWidget(time_label, row, 0)
            details_layout.addWidget(time_value, row, 1)
            row += 1

        # Location (building and room)
        if hasattr(lesson, 'building') and hasattr(lesson, 'room') and lesson.building and lesson.room:
            location_label = QLabel("Location:")
            location_value = QLabel(f"בניין:  {lesson.building}, חדר: {lesson.room}")
            location_label.setStyleSheet("font-weight: bold; color: #555;")
            details_layout.addWidget(location_label, row, 0)
            details_layout.addWidget(location_value, row, 1)
            row += 1

        # Instructors
        if hasattr(lesson, 'instructors') and lesson.instructors:
            instructors_label = QLabel("Instructors:")
            instructors_value = QLabel(", ".join(lesson.instructors))
            instructors_label.setStyleSheet("font-weight: bold; color: #555;")
            instructors_value.setWordWrap(True)
            details_layout.addWidget(instructors_label, row, 0)
            details_layout.addWidget(instructors_value, row, 1)
            row += 1

        # Credit Points
        if hasattr(lesson, 'creditPoints') and lesson.creditPoints:
            credits_label = QLabel("Credits:")
            credits_value = QLabel(str(lesson.creditPoints))
            credits_label.setStyleSheet("font-weight: bold; color: #555;")
            details_layout.addWidget(credits_label, row, 0)
            details_layout.addWidget(credits_value, row, 1)
            row += 1

        # Weekly Hours
        if hasattr(lesson, 'weeklyHours') and lesson.weeklyHours:
            hours_label = QLabel("Weekly Hours:")
            hours_value = QLabel(str(lesson.weeklyHours))
            hours_label.setStyleSheet("font-weight: bold; color: #555;")
            details_layout.addWidget(hours_label, row, 0)
            details_layout.addWidget(hours_value, row, 1)
            row += 1

        layout.addWidget(details_widget)
        return widget

    def clear_layout(self, layout):
        """Remove all widgets from the given layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def clear_all_details(self):
        """Clear the main course detail labels"""
        self.code_label.setText("Code: ")
        self.name_label.setText("Name: ")
        self.semester_label.setText("Semester: ")
        self.total_credits_label.setText("Total Credits: ")
        self.total_groups_label.setText("Groups: ")

    def _calculate_total_credits(self, course):
        """Calculate the total credit points from all lesson types"""
        total = 0
        lesson_types = ['lectures', 'exercises', 'labs', 'departmentHours', 'reinforcement', 'training']
        
        for lesson_type in lesson_types:
            lessons = getattr(course, lesson_type, [])
            for lesson in lessons:
                total += getattr(lesson, 'creditPoints', 0)
        
        return total if total > 0 else 'N/A'

    def _count_total_groups(self, course):
        """Count total unique group codes across all lessons"""
        groups = set()
        lesson_types = ['lectures', 'exercises', 'labs', 'departmentHours', 'reinforcement', 'training']
        
        for lesson_type in lesson_types:
            lessons = getattr(course, lesson_type, [])
            for lesson in lessons:
                if hasattr(lesson, 'groupCode') and lesson.groupCode:
                    groups.add(lesson.groupCode)
        
        return len(groups)

    def add_course(self):
        """Emit signal to add the selected course"""
        if self.current_course:
            self.add_course_requested.emit(self.current_course._code)
