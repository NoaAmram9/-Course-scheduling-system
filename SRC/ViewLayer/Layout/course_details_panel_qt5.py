
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

class CourseDetailsPanelQt5(QWidget):
    add_course_requested = pyqtSignal(str)  # Emits course code

    def __init__(self):
        super().__init__()
        self.current_course = None
        self.details_popup = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Title
        title_label = QLabel("Course Details")
        title_label.setObjectName("panelTitle")
        layout.addWidget(title_label)

        # Content frame with orange border
        content_frame = QFrame()
        content_frame.setObjectName("detailsFrame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(0)

        # General course info (compact)
        general_info_fields = [
            ('code_label', "Code: "),
            ('name_label', "Name: "),
            ('semester_label', "Semester: "),
            ('total_credits_label', "Total Credits: "),
            ('total_groups_label', "Groups: ")
        ]

        for attr, text in general_info_fields:
            self.create_detail_row(content_layout, attr, text)

        # Lesson types summary
        # self.create_lesson_summary_section(content_layout)

        layout.addWidget(content_frame)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Details button
        self.details_button = ModernUIQt5.create_button("📋 Additional Details")
        self.details_button.setObjectName("DetailsButton")
        self.details_button.clicked.connect(self.show_details_popup)
        # Remove hover events that caused auto-closing
        buttons_layout.addWidget(self.details_button)

        # Add course button
        self.add_button = ModernUIQt5.create_button("Add Course")
        self.add_button.setObjectName("UploadButton")
        self.add_button.clicked.connect(self.add_course)
        buttons_layout.addWidget(self.add_button)

        layout.addLayout(buttons_layout)

        self.setStyleSheet(ModernUIQt5.get_main_stylesheet() + """
            QPushButton#DetailsButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton#DetailsButton:hover {
                background-color: #45a049;
            }
        """)

    # def create_lesson_summary_section(self, parent_layout):
    #     """Create compact summary of lesson types"""
    #     # Section title
    #     section_title = QLabel("📚 Course Components")
    #     section_title.setObjectName("sectionTitle")
    #     section_title.setStyleSheet("font-weight: bold; font-size: 13px; color: #FFA500; padding: 8px 0px;")
    #     parent_layout.addWidget(section_title)
    #     self.add_separator(parent_layout)

    #     # Summary labels for each lesson type
    #     lesson_types = [
    #         ('lectures', 'Lectures', '🎓'),
    #         ('exercises', 'Exercises', '📝'),
    #         ('labs', 'Labs', '🔬'),
    #         ('departmentHours', 'Department Hours', '🏢'),
    #         ('reinforcement', 'Reinforcement', '💪'),
    #         ('training', 'Training', '🏋️')
    #     ]

    #     for attr_name, display_name, icon in lesson_types:
    #         summary_text = f"{icon} {display_name}: "
    #         attr_label_name = f"{attr_name}_summary_label"
    #         self.create_detail_row(parent_layout, attr_label_name, summary_text)

    def create_detail_row(self, parent_layout, attr_name, label_text):
        """Create a detail row with label"""
        label = QLabel(label_text)
        label.setObjectName("detailLabel")
        label.setWordWrap(True)

        wrapper = QFrame()
        wrapper.setObjectName("detailRowFrame")
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 8, 0, 8)
        wrapper_layout.addWidget(label)

        setattr(self, attr_name, label)
        parent_layout.addWidget(wrapper)
        self.add_separator(parent_layout)

    def add_separator(self, layout):
        """Add orange separator line"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #FFA500; background-color: #FFA500; max-height: 1px;")
        layout.addWidget(line)

    def update_details(self, course):
        """Update the panel with course details"""
        self.current_course = course

        if course:
            self.update_general_info(course)
            self.update_lesson_summaries(course)
        else:
            self.clear_all_details()

    def update_general_info(self, course):
        """Update general course information"""
        self.code_label.setText(f"Code: {course._code}")
        self.name_label.setText(f"Name: {course._name}")
        self.semester_label.setText(f"Semester: {course._semester}")
        
        total_credits = self._calculate_total_credits(course)
        self.total_credits_label.setText(f"Total Credits: {total_credits}")
        
        total_groups = self._count_total_groups(course)
        self.total_groups_label.setText(f"Groups: {total_groups}")

    def update_lesson_summaries(self, course):
        """Update lesson type summaries"""
        lesson_types = [
            ('lectures', 'Lectures', '🎓'),
            ('exercises', 'Exercises', '📝'),
            ('labs', 'Labs', '🔬'),
            ('departmentHours', 'Department Hours', '🏢'),
            ('reinforcement', 'Reinforcement', '💪'),
            ('training', 'Training', '🏋️')
        ]

        for attr_name, display_name, icon in lesson_types:
            lessons = getattr(course, attr_name, [])
            count = len(lessons)
            
            if count > 0:
                # Get unique groups and instructors for summary
                groups = set()
                instructors = set()
                for lesson in lessons:
                    if hasattr(lesson, 'groupCode') and lesson.groupCode:
                        groups.add(lesson.groupCode)
                    if hasattr(lesson, 'instructors') and lesson.instructors:
                        instructors.update(lesson.instructors)
                
                summary = f"{icon} {display_name}: {count} sessions"
                if groups:
                    summary += f" | Groups: {', '.join(map(str, sorted(groups)))}"
                if instructors:
                    instructors_short = ', '.join(list(instructors)[:2])
                    if len(instructors) > 2:
                        instructors_short += f" +{len(instructors)-2} more"
                    summary += f" | Prof: {instructors_short}"
            else:
                summary = f"{icon} {display_name}: No sessions"
            
            # summary_label = getattr(self, f"{attr_name}_summary_label")
            # summary_label.setText(summary)

    def on_details_hover(self, event):
        """Show details on hover - only for quick preview"""
        pass  # Disabled hover popup to avoid conflicts

    def on_details_leave(self, event):
        """Hide details when leaving hover"""
        pass  # Disabled to prevent auto-closing

    def show_details_tooltip(self):
        """Show details as tooltip"""
        if not self.current_course:
            return

        # Create or update tooltip
        if not self.details_popup:
            self.details_popup = self.create_details_popup()
        
        self.update_details_popup()
        
        # Position tooltip near the button
        button_pos = self.details_button.mapToGlobal(self.details_button.rect().bottomLeft())
        self.details_popup.move(button_pos.x(), button_pos.y() + 5)
        self.details_popup.show()

    def show_details_popup(self):
        """Show details popup on click"""
        if not self.current_course:
            return

        if not self.details_popup:
            self.details_popup = self.create_details_popup()
        
        self.update_details_popup()
        
        # Position popup better - not blocking the main window
        parent_pos = self.mapToGlobal(self.pos())
        parent_rect = self.rect()
        
        # Try to position to the right of parent, or left if no space
        screen = QApplication.desktop().screenGeometry()
        popup_width = self.details_popup.width()
        
        if parent_pos.x() + parent_rect.width() + popup_width < screen.width():
            # Position to the right
            x = parent_pos.x() + parent_rect.width() + 10
        else:
            # Position to the left
            x = parent_pos.x() - popup_width - 10
        
        y = max(parent_pos.y(), 50)  # Don't go above screen
        
        self.details_popup.move(x, y)
        self.details_popup.show()
        self.details_popup.raise_()
        self.details_popup.activateWindow()

    def create_details_popup(self):
        """Create the detailed popup window"""
        popup = QDialog(self)
        popup.setWindowTitle("Course Details")
        popup.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        popup.setModal(False)  # Allow interaction with parent
        popup.resize(650, 550)
        
        layout = QVBoxLayout(popup)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("📋 Detailed Course Information")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFA500; padding: 10px 0px;")
        layout.addWidget(title)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Content widget
        self.popup_content_widget = QWidget()
        self.popup_main_layout = QVBoxLayout(self.popup_content_widget)
        self.popup_main_layout.setSpacing(15)
        
        scroll_area.setWidget(self.popup_content_widget)
        layout.addWidget(scroll_area)

        # Close button layout
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
                background-color: #d32f2f;
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
        # Clear existing content
        self.clear_layout(self.popup_main_layout)
        
        if not self.current_course:
            return

        course = self.current_course

        # Notes section
        if hasattr(course, 'notes') and course.notes:
            notes_frame = QFrame()
            notes_frame.setObjectName("detailsFrame")
            notes_layout = QVBoxLayout(notes_frame)
            notes_layout.setContentsMargins(15, 15, 15, 15)
            
            notes_title = QLabel("📝 Notes")
            notes_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #FFA500;")
            notes_layout.addWidget(notes_title)
            
            notes_text = QLabel(course.notes)
            notes_text.setWordWrap(True)
            notes_text.setStyleSheet("padding: 10px; background-color: #f9f9f9; border-radius: 5px;")
            notes_layout.addWidget(notes_text)
            
            self.popup_main_layout.addWidget(notes_frame)

        # Detailed lesson sections
        lesson_types = [
            ('lectures', 'Lectures', '🎓'),
            ('exercises', 'Exercises', '📝'),
            ('labs', 'Labs', '🔬'),
            ('departmentHours', 'Department Hours', '🏢'),
            ('reinforcement', 'Reinforcement', '💪'),
            ('training', 'Training', '🏋️')
        ]

        for attr_name, display_name, icon in lesson_types:
            lessons = getattr(course, attr_name, [])
            if lessons:  # Only show sections that have lessons
                section_widget = self.create_detailed_lesson_section(attr_name, display_name, icon, lessons)
                self.popup_main_layout.addWidget(section_widget)

    def create_detailed_lesson_section(self, attr_name, display_name, icon, lessons):
        """Create detailed section for lesson type"""
        frame = QFrame()
        frame.setObjectName("detailsFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Section header
        header_layout = QHBoxLayout()
        title_label = QLabel(f"{icon} {display_name}")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #FFA500;")
        
        count_label = QLabel(f"({len(lessons)} sessions)")
        count_label.setStyleSheet("color: #888; font-size: 12px;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(count_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #FFA500; background-color: #FFA500;")
        layout.addWidget(separator)

        # Individual lessons
        for i, lesson in enumerate(lessons):
            lesson_widget = self.create_detailed_lesson_widget(lesson, i + 1)
            layout.addWidget(lesson_widget)

        return frame

    def create_detailed_lesson_widget(self, lesson, lesson_number):
        """Create detailed widget for individual lesson"""
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

        # Lesson header
        header_text = f"Session {lesson_number} - Group {getattr(lesson, 'groupCode', 'N/A')}"
        if hasattr(lesson, 'lesson_type') and lesson.lesson_type:
            header_text += f" ({lesson.lesson_type})"
        
        header_label = QLabel(header_text)
        header_label.setStyleSheet("font-weight: bold; color: #333; font-size: 12px;")
        layout.addWidget(header_label)

        # Create details grid
        details_widget = QWidget()
        details_layout = QGridLayout(details_widget)
        details_layout.setSpacing(8)
        details_layout.setContentsMargins(5, 5, 5, 5)

        row = 0
        
        # Time
        if hasattr(lesson, 'time') and lesson.time:
            time_label = QLabel("🕐 Time:")
            
            # גרסה פשוטה יותר - רק שעות
            time_display = f"{lesson.time.start_hour:02d}:00 - {lesson.time.end_hour:02d}:00"
            time_value = QLabel(time_display)
            
            time_label.setStyleSheet("font-weight: bold; color: #555;")
            details_layout.addWidget(time_label, row, 0)
            details_layout.addWidget(time_value, row, 1)
            row += 1

        # Location
        if hasattr(lesson, 'building') and hasattr(lesson, 'room') and lesson.building and lesson.room:
            location_label = QLabel("📍 Location:")
            location_value = QLabel(f"Building {lesson.building}, Room {lesson.room}")
            location_label.setStyleSheet("font-weight: bold; color: #555;")
            details_layout.addWidget(location_label, row, 0)
            details_layout.addWidget(location_value, row, 1)
            row += 1

        # Instructors
        if hasattr(lesson, 'instructors') and lesson.instructors:
            instructors_label = QLabel("👨‍🏫 Instructors:")
            instructors_value = QLabel(", ".join(lesson.instructors))
            instructors_label.setStyleSheet("font-weight: bold; color: #555;")
            instructors_value.setWordWrap(True)
            details_layout.addWidget(instructors_label, row, 0)
            details_layout.addWidget(instructors_value, row, 1)
            row += 1

        # Credits
        if hasattr(lesson, 'creditPoints') and lesson.creditPoints:
            credits_label = QLabel("🎯 Credits:")
            credits_value = QLabel(str(lesson.creditPoints))
            credits_label.setStyleSheet("font-weight: bold; color: #555;")
            details_layout.addWidget(credits_label, row, 0)
            details_layout.addWidget(credits_value, row, 1)
            row += 1

        # Weekly Hours
        if hasattr(lesson, 'weeklyHours') and lesson.weeklyHours:
            hours_label = QLabel("⏰ Weekly Hours:")
            hours_value = QLabel(str(lesson.weeklyHours))
            hours_label.setStyleSheet("font-weight: bold; color: #555;")
            details_layout.addWidget(hours_label, row, 0)
            details_layout.addWidget(hours_value, row, 1)
            row += 1

        layout.addWidget(details_widget)
        return widget

    def clear_layout(self, layout):
        """Clear all widgets from layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def clear_all_details(self):
        """Clear all course details"""
        self.code_label.setText("Code: ")
        self.name_label.setText("Name: ")
        self.semester_label.setText("Semester: ")
        self.total_credits_label.setText("Total Credits: ")
        self.total_groups_label.setText("Groups: ")
        
        # # Clear lesson summaries
        # lesson_types = ['lectures', 'exercises', 'labs', 'departmentHours', 'reinforcement', 'training']
        # for lesson_type in lesson_types:
        #     summary_label = getattr(self, f"{lesson_type}_summary_label", None)
        #     if summary_label:
        #         icon_map = {
        #             'lectures': '🎓', 'exercises': '📝', 'labs': '🔬',
        #             'departmentHours': '🏢', 'reinforcement': '💪', 'training': '🏋️'
        #         }
        #         display_name = lesson_type.replace('departmentHours', 'Department Hours').replace('reinforcement', 'Reinforcement').replace('training', 'Training').capitalize()
        #         summary_label.setText(f"{icon_map.get(lesson_type, '📚')} {display_name}: No sessions")

    def _calculate_total_credits(self, course):
        """Calculate total credit points from all lessons"""
        total = 0
        lesson_types = ['lectures', 'exercises', 'labs', 'departmentHours', 'reinforcement', 'training']
        
        for lesson_type in lesson_types:
            lessons = getattr(course, lesson_type, [])
            for lesson in lessons:
                total += getattr(lesson, 'creditPoints', 0)
        
        return total if total > 0 else 'N/A'

    def _count_total_groups(self, course):
        """Count total unique groups across all lesson types"""
        groups = set()
        lesson_types = ['lectures', 'exercises', 'labs', 'departmentHours', 'reinforcement', 'training']
        
        for lesson_type in lesson_types:
            lessons = getattr(course, lesson_type, [])
            for lesson in lessons:
                if hasattr(lesson, 'groupCode') and lesson.groupCode:
                    groups.add(lesson.groupCode)
        
        return len(groups)

    def add_course(self):
        if self.current_course:
            self.add_course_requested.emit(self.current_course._code)