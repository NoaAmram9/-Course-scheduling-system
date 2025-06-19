# import re

# class CourseFormValidator:
#     """Utility class for validating course form data"""
    
#     def __init__(self):
#         # Regex pattern for course codes (letters followed by numbers)
#         self.course_code_pattern = re.compile(r'^[A-Za-z]{2,6}\d{3,4}[A-Za-z]?$')
    
#     def validate_course_code(self, code):
#         """
#         Validate course code format
#         Expected formats: CS101, MATH200, PHYS101A, etc.
#         """
#         if not code:
#             return False
        
#         return bool(self.course_code_pattern.match(code.strip()))
    
#     def validate_required_field(self, value):
#         """Check if a required field has content"""
#         return bool(value and value.strip())
    
#     def validate_credits(self, credits):
#         """Validate credit points (should be positive number)"""
#         return isinstance(credits, int) and 0 <= credits <= 10
    
#     def validate_semester(self, semester):
#         """Validate semester selection"""
#         valid_semesters = ["Fall", "Spring", "Summer", "Winter"]
#         return semester in valid_semesters
    
#     def validate_email(self, email):
#         """Validate email format (for instructor contact)"""
#         if not email:
#             return True  # Email is optional
        
#         email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
#         return bool(email_pattern.match(email.strip()))
    
#     def validate_course_name(self, name):
#         """Validate course name (should not be empty and reasonable length)"""
#         if not name or not name.strip():
#             return False
        
#         name = name.strip()
#         return 3 <= len(name) <= 100
    
#     def validate_all_form_data(self, form_data):
#         """
#         Validate all form data at once
#         Returns (is_valid, error_messages)
#         """
#         errors = []
        
#         # Required fields
#         if not self.validate_required_field(form_data.get('code')):
#             errors.append("Course code is required")
#         elif not self.validate_course_code(form_data.get('code')):
#             errors.append("Invalid course code format (expected: CS101, MATH200, etc.)")
        
#         if not self.validate_course_name(form_data.get('name')):
#             errors.append("Course name is required and should be 3-100 characters")
        
#         # Optional field validations
#         if form_data.get('credits') is not None and not self.validate_credits(form_data.get('credits')):
#             errors.append("Credits should be between 0 and 10")
        
#         semester = form_data.get('semester')
#         if semester and semester != "Select..." and not self.validate_semester(semester):
#             errors.append("Invalid semester selection")
        
#         return len(errors) == 0, errors
    
#     def sanitize_course_code(self, code):
#         """Clean and format course code"""
#         if not code:
#             return ""
        
#         # Remove spaces and convert to uppercase
#         cleaned = ''.join(code.split()).upper()
#         return cleaned
    
#     def sanitize_text_field(self, text):
#         """Clean text fields (remove extra spaces, etc.)"""
#         if not text:
#             return ""
        
#         # Remove leading/trailing spaces and normalize internal spaces
#         return ' '.join(text.split())
    
#     def get_validation_hints(self):
#         """Get validation hints for the UI"""
#         return {
#             'course_code': "Format: 2-6 letters followed by 3-4 numbers (e.g., CS101, MATH200)",
#             'course_name': "Required field, 3-100 characters",
#             'credits': "Number between 0 and 10",
#             'semester': "Select from available options",
#         }




from PyQt5.QtWidgets import QMessageBox
import re

class CourseFormValidator:
    """
    Handles validation of form fields for course creation in AddCourseDialog.
    """

    def __init__(self, form_fields, parent=None):
        self.form_fields = form_fields
        self.parent = parent  # For QMessageBox context if needed

    def validate(self):
        """
        Validate all required fields and custom rules.
        Returns True if all validations pass, otherwise False.
        """
        if not self._validate_required_fields():
            return False

        if not self._validate_course_code():
            return False

        return True

    def _validate_required_fields(self):
        """Ensure required fields are filled."""
        required = ['code', 'name']
        for key in required:
            field = self.form_fields.get(key)
            if not field or not field.text().strip():
                self._show_warning(f"Please fill in the {key.replace('_', ' ').title()} field.", field)
                return False
        return True

    def _validate_course_code(self):
        """Validate that the course code is exactly 5 digits."""
        code_field = self.form_fields['code']
        code = code_field.text().strip()
        if not re.match(r'^\d{5}$', code):
            self._show_warning("Course code must be exactly 5 digits (e.g., 12345).", code_field)
            return False
        return True

    def _show_warning(self, message, widget=None):
        """Display a warning message and optionally focus a widget."""
        QMessageBox.warning(self.parent, "Validation Error", message)
        if widget:
            widget.setFocus()
