from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5
from .CourseFormValidator import CourseFormValidator
from SRC.Models.Course import Course
from .LessonDialog import LessonDialog

class AddCourseDialog(QDialog):
    """Dialog window for registering/adding new courses"""
    
    # Signal emitted when a course is successfully added
    course_added = pyqtSignal(Course)  # Emits Course object instead of dict
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.form_fields = {}
        self.lessons_list = []  # Store lessons temporarily
        self.init_ui()        
        self.validator = CourseFormValidator(self.form_fields, parent=self)

    def init_ui(self):
        """Initialize the add course dialog"""
        self.setWindowTitle("Add New Course")
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setModal(True)
        self.resize(700, 800)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header
        self._create_header(main_layout)
        
        # Form content in scroll area
        self._create_form_scroll_area(main_layout)
        
        # Buttons
        self._create_buttons(main_layout)
        
        # Apply styling
        self.setStyleSheet(ModernUIQt5.get_main_stylesheet())

    def _create_header(self, parent_layout):
        """Create the dialog header"""
        header_frame = QFrame()
        header_frame.setObjectName("detailsFrame")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 15, 15, 10)

        title = QLabel("Register New Course")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #944e25; padding: 5px 0px;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Fill in the course details below")
        subtitle.setStyleSheet("font-size: 12px; color: #666; padding: 0px 0px 5px 0px;")
        subtitle.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        parent_layout.addWidget(header_frame)

    def _create_form_scroll_area(self, parent_layout):
        """Create scrollable form area"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Form widget
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(10, 10, 10, 10)

        # Basic Information Section
        self._create_basic_info_section(form_layout)
        
        # Course Details Section
        self._create_course_details_section(form_layout)
        
        # Lessons Section
        self._create_lessons_section(form_layout)
        
        # Additional Information Section
        # self._create_additional_info_section(form_layout)

        form_layout.addStretch()
        scroll_area.setWidget(form_widget)
        parent_layout.addWidget(scroll_area)

    def _create_basic_info_section(self, parent_layout):
        """Create basic information section"""
        section_frame = self._create_section_frame("Basic Information")
        section_layout = section_frame.layout()

        # Course Code (Required) - 5 digit format
        self.form_fields['code'] = self._create_form_field(
            section_layout, "Course Code (5 digits) *", "e.g., 12345", required=True
        )

        # Course Name (Required)
        self.form_fields['name'] = self._create_form_field(
            section_layout, "Course Name *", "e.g., Introduction to Computer Science", required=True
        )

        # Semester
        self.form_fields['semester'] = self._create_combo_field(
            section_layout, "Semester", 
            ["Semester A", "Semester B"]
        )
           # Notes
        self.form_fields['notes'] = self._create_text_area_field(
            section_layout, "Course Notes", "Any additional course information"
        )

        parent_layout.addWidget(section_frame)


    def _create_lessons_section(self, parent_layout):
        """Create lessons management section"""
        section_frame = self._create_section_frame("Lessons")
        section_layout = section_frame.layout()

        # Lessons list
        self.lessons_list_widget = QListWidget()
        self.lessons_list_widget.setMaximumHeight(150)
        self.lessons_list_widget.setStyleSheet("""
            QListWidget {
                border: 2px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        section_layout.addWidget(QLabel("Current Lessons:"))
        section_layout.addWidget(self.lessons_list_widget)

        # Add lesson button
        add_lesson_btn = ModernUIQt5.create_button("Add Lesson")
        # add_lesson_btn.setStyleSheet("""
        #     QPushButton {
        #         background-color: #17a2b8;
        #         color: white;
        #         border: none;
        #         padding: 8px 16px;
        #         border-radius: 4px;
        #         font-weight: bold;
        #     }
        #     QPushButton:hover {
        #         background-color: #138496;
        #     }
        # """)
        add_lesson_btn.clicked.connect(self._add_lesson)
        section_layout.addWidget(add_lesson_btn)

        # Remove lesson button
        remove_lesson_btn = ModernUIQt5.create_button("Remove Selected Lesson")
        remove_lesson_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        remove_lesson_btn.clicked.connect(self._remove_lesson)
        section_layout.addWidget(remove_lesson_btn)

        parent_layout.addWidget(section_frame)

    # def _create_additional_info_section(self, parent_layout):
    #     """Create additional information section"""
    #     section_frame = self._create_section_frame("Additional Information")
    #     section_layout = section_frame.layout()

    #     # # Main Instructor
    #     # self.form_fields['instructor'] = self._create_form_field(
    #     #     section_layout, "Main Instructor", "e.g., Dr. Smith"
    #     # )

    #     parent_layout.addWidget(section_frame)

    def _create_section_frame(self, title):
        """Create a styled section frame with title"""
        frame = QFrame()
        frame.setObjectName("detailsFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        # Section title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #FFA500; padding: 0px 0px 5px 0px;")
        layout.addWidget(title_label)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #FFA500; background-color: #FFA500; margin: 0px 0px 10px 0px;")
        layout.addWidget(separator)

        return frame

    def _create_form_field(self, parent_layout, label_text, placeholder, required=False):
        """Create a standard form input field"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Label
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; color: #333;")
        layout.addWidget(label)

        # Input field
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #FFA500;
            }
        """)
        
        if required:
            line_edit.setObjectName("required")
        
        layout.addWidget(line_edit)
        parent_layout.addWidget(container)

        return line_edit

    def _create_combo_field(self, parent_layout, label_text, options):
        """Create a combo box field"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Label
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; color: #333;")
        layout.addWidget(label)

        # Combo box
        combo = QComboBox()
        combo.addItems(["Select..."] + options)
        combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QComboBox:focus {
                border-color: #FFA500;
            }
        """)
        
        layout.addWidget(combo)
        parent_layout.addWidget(container)

        return combo

    def _create_spinbox_field(self, parent_layout, label_text, min_val, max_val, default_val):
        """Create a spin box field"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Label
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; color: #333;")
        layout.addWidget(label)

        # Spin box
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default_val)
        spinbox.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QSpinBox:focus {
                border-color: #FFA500;
            }
        """)
        
        layout.addWidget(spinbox)
        parent_layout.addWidget(container)

        return spinbox

    def _create_text_area_field(self, parent_layout, label_text, placeholder):
        """Create a text area field"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Label
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; color: #333;")
        layout.addWidget(label)

        # Text area
        text_edit = QTextEdit()
        text_edit.setPlaceholderText(placeholder)
        text_edit.setMaximumHeight(80)
        text_edit.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QTextEdit:focus {
                border-color: #FFA500;
            }
        """)
        
        layout.addWidget(text_edit)
        parent_layout.addWidget(container)

        return text_edit

    def _add_lesson(self):
        """Open dialog to add a new lesson"""
        dialog = LessonDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            lesson = dialog.get_lesson()
            self.lessons_list.append(lesson)
            self._update_lessons_display()

    def _remove_lesson(self):
        """Remove selected lesson"""
        current_row = self.lessons_list_widget.currentRow()
        if current_row >= 0:
            del self.lessons_list[current_row]
            self._update_lessons_display()

    def _update_lessons_display(self):
        """Update the lessons list display"""
        self.lessons_list_widget.clear()
        for lesson in self.lessons_list:
            lesson_text = f"{lesson.lesson_type.title()} - Day {lesson.time.day}, {lesson.time.start_hour:02d}:00-{lesson.time.end_hour:02d}:00"
            if lesson.building or lesson.room:
                lesson_text += f" ({lesson.building}-{lesson.room})"
            self.lessons_list_widget.addItem(lesson_text)

    def _create_buttons(self, parent_layout):
        """Create dialog buttons"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Cancel button
        cancel_btn = ModernUIQt5.create_button("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        # Add course button
        add_btn = ModernUIQt5.create_button("Add Course")
        
        add_btn.clicked.connect(self.add_course)

        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_btn)

        parent_layout.addLayout(button_layout)

    def add_course(self):
        """Handle adding the course"""
        if not self.validator.validate():
          return
        # Create Course object
        course = self._create_course_object()
        
        # Emit signal with course object
        self.course_added.emit(course)
        
        # Show success message
        QMessageBox.information(self, "Success", f"Course '{course.name}' has been added successfully!")
        
        # Close dialog
        self.accept()


    def _create_course_object(self):
        """Create a Course object from form data"""
        # Get basic data
        code = self.form_fields['code'].text().strip()
        name = self.form_fields['name'].text().strip()
        
        # Convert semester
        semester_text = self.form_fields['semester'].currentText()
        if semester_text == "Semester A":
            semester = 1
        elif semester_text == "Semester B":
            semester = 2
        else:
            semester = 0
            
        notes = self.form_fields['notes'].toPlainText().strip()

        # Create course object
        course = Course(name=name, code=code, semester=semester)
        
        # Add lessons to appropriate lists
        for lesson in self.lessons_list:
            if lesson.lesson_type == "lecture":
                course.lectures.append(lesson)
            elif lesson.lesson_type == "exercise":
                course.exercises.append(lesson)
            elif lesson.lesson_type == "lab":
                course.labs.append(lesson)
            elif lesson.lesson_type == "reinforcement":
                course.reinforcement.append(lesson)
            elif lesson.lesson_type == "training":
                course.training.append(lesson)
            elif lesson.lesson_type == "departmentHours":
                course.departmentHours.append(lesson)
            else:
                course.departmentHours.append(lesson)
        
        course.notes = notes


        return course

    def clear_form(self):
        """Clear all form fields"""
        self.form_fields['code'].clear()
        self.form_fields['name'].clear()
        self.form_fields['semester'].setCurrentIndex(0)
        # self.form_fields['credit_points'].setValue(3)
        # self.form_fields['weekly_hours'].setValue(4)
        self.form_fields['notes'].clear()
        self.lessons_list.clear()
        self._update_lessons_display()
