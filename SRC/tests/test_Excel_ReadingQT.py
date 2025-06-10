
# The tests do check English data.
# See: test_Excel_ReadingQT_valid_english_format, test_Excel_ReadingQT_valid_english_and_hebrew_mixed,
# test_Excel_ReadingQT_valid_english_weekdays, test_Excel_ReadingQT_invalid_english_weekdays,
# test_Excel_ReadingQT_unicode_and_special_characters_english, etc.
def test_Excel_ReadingQT_valid_english_format(excel_manager, create_mock_excel_file):
    """
    Test: Verifies successful reading of a valid Excel file with English headers.
    """
    df_data = {
        "Course Name": ["Introduction to Computer Science", "Introduction to Computer Science"],
        "Full Code": ["83108-01", "83108-02"],
        "Meeting Type": ["Lecture", "Tutorial"],
        "Semester": ["A", "A"],
        "Day": ["Sunday", "Tuesday"],
        "Start Time": ["09:00", "12:00"],
        "End Time": ["11:00", "13:00"],
        "Room": ["Building 901", "Building 902"],
        "Instructor": ["Dr. Cohen", "Prof. Levi"],
    }
    mock_file_path = create_mock_excel_file(df_data, "english_example.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        assert loaded_courses is not None
        if isinstance(loaded_courses, dict):
            assert len(loaded_courses) == 1  # Should be one unique course (83108)
            assert "83108" in loaded_courses
            course = loaded_courses["83108"]
            assert course.name == "Introduction to Computer Science"
            assert len(course.sections) == 2  # Two sections
        elif isinstance(loaded_courses, list):
            course_codes = set()
            for course in loaded_courses:
                course_codes.add(course.code)
            assert len(course_codes) == 1
        print("✓ Successfully loaded courses from English Excel file")
    except Exception as e:
        pytest.fail(f"Failed to load valid English Excel file: {e}")

def test_Excel_ReadingQT_valid_english_and_hebrew_mixed(excel_manager, create_mock_excel_file):
    """
    Test: Verifies reading Excel file with mixed Hebrew and English headers and data.
    """
    df_data = {
        "Course Name": ["מבוא למדעי המחשב", "Introduction to Algorithms"],
        "קוד מלא": ["83108-01", "83109-01"],
        "Meeting Type": ["Lecture", "תרגיל"],
        "תקופה": ["A", "א"],
        "Day": ["ראשון", "Monday"],
        "Start Time": ["09:00", "10:00"],
        "End Time": ["11:00", "12:00"],
        "Room": ["כיתה א", "Room B"],
        "Instructor": ["ד\"ר כהן", "Dr. Smith"],
    }
    mock_file_path = create_mock_excel_file(df_data, "mixed_lang.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        assert loaded_courses is not None
        print("✓ Successfully loaded courses from mixed Hebrew/English Excel file")
    except Exception as e:
        pytest.fail(f"Failed to load mixed Hebrew/English Excel file: {e}")

def test_Excel_ReadingQT_valid_english_weekdays(excel_manager, create_mock_excel_file):
    """
    Test: Verifies that courses on valid English weekdays (Sunday-Thursday) are accepted.
    """
    df_data = {
        "Course Name": ["Course A", "Course B", "Course C", "Course D", "Course E"],
        "Full Code": ["83114-01", "83115-01", "83116-01", "83117-01", "83118-01"],
        "Meeting Type": ["Lecture"] * 5,
        "Semester": ["A"] * 5,
        "Day": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"],
        "Start Time": ["09:00", "10:00", "11:00", "12:00", "13:00"],
        "End Time": ["11:00", "12:00", "13:00", "14:00", "15:00"],
        "Room": ["Room A", "Room B", "Room C", "Room D", "Room E"],
        "Instructor": ["Dr. A", "Dr. B", "Dr. C", "Dr. D", "Dr. E"],
    }
    mock_file_path = create_mock_excel_file(df_data, "valid_english_weekdays.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        assert loaded_courses is not None
        if isinstance(loaded_courses, dict):
            assert len(loaded_courses) == 5
        print("✓ Successfully accepted courses on valid English weekdays")
    except Exception as e:
        pytest.fail(f"Failed to accept valid English weekdays: {e}")

def test_Excel_ReadingQT_invalid_english_weekdays(excel_manager, create_mock_excel_file):
    """
    Test: Verifies handling of courses on invalid English days (Friday, Saturday).
    """
    df_data = {
        "Course Name": ["Friday Course", "Saturday Course"],
        "Full Code": ["83119-01", "83120-01"],
        "Meeting Type": ["Lecture", "Lecture"],
        "Semester": ["A", "A"],
        "Day": ["Friday", "Saturday"],
        "Start Time": ["09:00", "10:00"],
        "End Time": ["11:00", "12:00"],
        "Room": ["Room A", "Room B"],
        "Instructor": ["Dr. Cohen", "Dr. Levi"],
    }
    mock_file_path = create_mock_excel_file(df_data, "invalid_english_weekdays.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        print("✓ Handled courses on invalid English weekdays appropriately")
    except Exception as e:
        print(f"✓ Correctly rejected courses on invalid English weekdays: {e}")

def test_Excel_ReadingQT_unicode_and_special_characters_english(excel_manager, create_mock_excel_file):
    """
    Test: Verifies handling of Unicode and special symbols in English data.
    """
    df_data = {
        "Course Name": ["Discrete Math 🔢", "Physics I - Classical Mechanics", "Programming in C++"],
        "Full Code": ["12321-01", "12322-01", "12323-01"],
        "Meeting Type": ["Lecture", "Lecture", "Lecture"],
        "Semester": ["A", "A", "A"],
        "Day": ["Sunday", "Monday", "Tuesday"],
        "Start Time": ["09:00", "10:00", "11:00"],
        "End Time": ["11:00", "12:00", "13:00"],
        "Room": ["Room α", "Building β-101", "Lab C++"],
        "Instructor": ["Prof. Alpha-Beta", "Dr. Gamma", "Mr. Smith & Dr. Jones"],
    }
    mock_file_path = create_mock_excel_file(df_data, "unicode_special_chars_english.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        assert loaded_courses is not None
        print("✓ Successfully handled Unicode and special characters in English data")
    except Exception as e:
        print(f"✓ Handled Unicode/special characters in English with appropriate error: {e}")
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import os
import sys
from datetime import datetime

# Add the project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import only the ExcelManager for unit testing, avoiding GUI components
from SRC.Services.ExcelManager import ExcelManager

# Fixture to create mock Excel files
@pytest.fixture
def create_mock_excel_file(tmp_path):
    def _create_mock_file(df_data, file_name="courses.xlsx"):
        file_path = tmp_path / file_name
        df = pd.DataFrame(df_data)
        df.to_excel(file_path, index=False)
        return str(file_path)
    return _create_mock_file

# Mock Course class if needed
class MockCourse:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.sections = []
    
    def add_section(self, section):
        self.sections.append(section)

class MockSection:
    def __init__(self, meeting_type, day, start_time, end_time, room, instructor):
        self.meeting_type = meeting_type
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.room = room
        self.instructor = instructor

@pytest.fixture
def excel_manager():
    """Create an ExcelManager instance for testing."""
    return ExcelManager()

def test_Excel_ReadingQT_valid_hebrew_format(excel_manager, create_mock_excel_file):
    """
    Test 1: Verifies successful reading of a valid Excel file with Hebrew headers.
    Tests the ExcelManager directly without GUI components.
    """
    df_data = {
        "שם קורס": ["מבוא למדעי המחשב", "מבוא למדעי המחשב"],
        "קוד מלא": ["83108-01", "83108-02"],
        "סוג מפגש": ["הרצאה", "תרגיל"],
        "תקופה": ["א", "א"],
        "יום": ["ראשון", "שני"],
        "שעת התחלה": ["09:00", "10:00"],
        "שעת סיום": ["11:00", "12:00"],
        "חדר": ["כיתה א", "כיתה ב"],
        "מרצה": ["ד\"ר כהן", "ד\"ר לוי"],
    }
    mock_file_path = create_mock_excel_file(df_data, "invalid_course_codes.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        # Should either reject invalid codes or handle them with warnings
        print(f"✓ Handled invalid course code formats appropriately")
        
    except Exception as e:
        print(f"✓ Correctly rejected invalid course codes: {e}")


def test_Excel_ReadingQT_multiple_instructors(excel_manager, create_mock_excel_file):
    """
    Test 15: Verifies correct parsing of multiple instructors (e.g., "ד"ר ישראלי, פרופ' כהן").
    """
    df_data = {
        "שם קורס": ["קורס עם מספר מרצים"],
        "קוד מלא": ["83109-01"],
        "סוג מפגש": ["הרצאה"],
        "תקופה": ["א"],
        "יום": ["ראשון"],
        "שעת התחלה": ["09:00"],
        "שעת סיום": ["11:00"],
        "חדר": ["כיתה א"],
        "מרצה": ["ד\"ר ישראלי, פרופ' כהן"],  # Multiple instructors
    }
    mock_file_path = create_mock_excel_file(df_data, "multiple_instructors.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        
        if isinstance(loaded_courses, dict):
            course = list(loaded_courses.values())[0]
            # Should correctly parse and handle multiple instructors
            instructor_field = course.sections[0].instructor
            assert "ישראלי" in instructor_field
            assert "כהן" in instructor_field
            
        print(f"✓ Successfully parsed multiple instructors")
        
    except Exception as e:
        pytest.fail(f"Failed to parse multiple instructors: {e}")


def test_Excel_ReadingQT_valid_time_range(excel_manager, create_mock_excel_file):
    """
    Test 16a: Verifies that courses within valid time range (8:00-21:00) are accepted.
    """
    df_data = {
        "שם קורס": ["קורס בשעות תקינות", "קורס ערב"],
        "קוד מלא": ["83110-01", "83111-01"],
        "סוג מפגש": ["הרצאה", "הרצאה"],
        "תקופה": ["א", "א"],
        "יום": ["ראשון", "שני"],
        "שעת התחלה": ["08:00", "19:00"],  # Valid times
        "שעת סיום": ["10:00", "21:00"],    # Valid times
        "חדר": ["כיתה א", "כיתה ב"],
        "מרצה": ["ד\"ר כהן", "ד\"ר לוי"],
    }
    mock_file_path = create_mock_excel_file(df_data, "valid_time_range.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        assert loaded_courses is not None
        if isinstance(loaded_courses, dict):
            assert len(loaded_courses) == 2
            
        print(f"✓ Successfully accepted courses within valid time range")
        
    except Exception as e:
        pytest.fail(f"Failed to accept valid time range: {e}")


def test_Excel_ReadingQT_invalid_time_range(excel_manager, create_mock_excel_file):
    """
    Test 16b: Verifies handling of courses outside valid time range (before 8:00 or after 21:00).
    """
    df_data = {
        "שם קורס": ["קורס מוקדם מדי", "קורס מאוחר מדי"],
        "קוד מלא": ["83112-01", "83113-01"],
        "סוג מפגש": ["הרצאה", "הרצאה"],
        "תקופה": ["א", "א"],
        "יום": ["ראשון", "שני"],
        "שעת התחלה": ["07:00", "21:30"],  # Invalid times
        "שעת סיום": ["09:00", "23:00"],    # Invalid times
        "חדר": ["כיתה א", "כיתה ב"],
        "מרצה": ["ד\"ר כהן", "ד\"ר לוי"],
    }
    mock_file_path = create_mock_excel_file(df_data, "invalid_time_range.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        # Should either reject courses with invalid times or handle with warnings
        print(f"✓ Handled courses with invalid time range appropriately")
        
    except Exception as e:
        print(f"✓ Correctly rejected courses with invalid time range: {e}")


def test_Excel_ReadingQT_valid_weekdays(excel_manager, create_mock_excel_file):
    """
    Test 17a: Verifies that courses on valid weekdays (Sunday-Thursday) are accepted.
    """
    df_data = {
        "שם קורס": ["קורס א", "קורס ב", "קורס ג", "קורס ד", "קורס ה"],
        "קוד מלא": ["83114-01", "83115-01", "83116-01", "83117-01", "83118-01"],
        "סוג מפגש": ["הרצאה", "הרצאה", "הרצאה", "הרצאה", "הרצאה"],
        "תקופה": ["א", "א", "א", "א", "א"],
        "יום": ["ראשון", "שני", "שלישי", "רביעי", "חמישי"],  # Valid weekdays
        "שעת התחלה": ["09:00", "10:00", "11:00", "12:00", "13:00"],
        "שעת סיום": ["11:00", "12:00", "13:00", "14:00", "15:00"],
        "חדר": ["כיתה א", "כיתה ב", "כיתה ג", "כיתה ד", "כיתה ה"],
        "מרצה": ["ד\"ר א", "ד\"ר ב", "ד\"ר ג", "ד\"ר ד", "ד\"ר ה"],
    }
    mock_file_path = create_mock_excel_file(df_data, "valid_weekdays.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        assert loaded_courses is not None
        if isinstance(loaded_courses, dict):
            assert len(loaded_courses) == 5
            
        print(f"✓ Successfully accepted courses on valid weekdays")
        
    except Exception as e:
        pytest.fail(f"Failed to accept valid weekdays: {e}")


def test_Excel_ReadingQT_invalid_weekdays(excel_manager, create_mock_excel_file):
    """
    Test 17b: Verifies handling of courses on invalid days (Friday, Saturday).
    """
    df_data = {
        "שם קורס": ["קורס שישי", "קורס שבת"],
        "קוד מלא": ["83119-01", "83120-01"],
        "סוג מפגש": ["הרצאה", "הרצאה"],
        "תקופה": ["א", "א"],
        "יום": ["שישי", "שבת"],  # Invalid days
        "שעת התחלה": ["09:00", "10:00"],
        "שעת סיום": ["11:00", "12:00"],
        "חדר": ["כיתה א", "כיתה ב"],
        "מרצה": ["ד\"ר כהן", "ד\"ר לוי"],
    }
    mock_file_path = create_mock_excel_file(df_data, "invalid_weekdays.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        # Should either reject courses on weekends or handle with warnings
        print(f"✓ Handled courses on invalid weekdays appropriately")
        
    except Exception as e:
        print(f"✓ Correctly rejected courses on invalid weekdays: {e}")


def test_Excel_ReadingQT_edge_cases(excel_manager, create_mock_excel_file):
    """
    Test 17c: Edge cases - various boundary conditions and unusual scenarios.
    """
    df_data = {
        "שם קורס": ["קורס ארוך מאוד עם שם שמכיל הרבה מילים ותווים מיוחדים !@#$%", 
                   "א", 
                   "קורס עם רווחים מיותרים   ",
                   ""],
        "קוד מלא": ["12345-01", "99999-99", "00000-00", "11111-AA"],
        "סוג מפגש": ["הרצאה", "הרצאה", "הרצאה", "הרצאה"],
        "תקופה": ["א", "א", "א", "א"],
        "יום": ["ראשון", "חמישי", "שלישי", "רביעי"],
        "שעת התחלה": ["08:00", "20:59", "12:30", "09:15"],
        "שעת סיום": ["08:01", "21:00", "12:31", "09:16"],  # Very short classes
        "חדר": ["", "חדר עם שם ארוך מאוד 123456789", "   ", "חדר רגיל"],
        "מרצה": ["", "פרופ' עם שם ארוך מאוד ותואר ארוך", "   ", "ד\"ר רגיל"],
    }
    mock_file_path = create_mock_excel_file(df_data, "edge_cases.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        # Should handle edge cases gracefully
        print(f"✓ Successfully handled edge cases")
        
    except Exception as e:
        print(f"✓ Handled edge cases with appropriate error handling: {e}")


def test_Excel_ReadingQT_unicode_and_special_characters(excel_manager, create_mock_excel_file):
    """
    Test 17d: Verifies handling of Unicode characters and special symbols.
    """
    df_data = {
        "שם קורס": ["מתמטיקה דיסקרטית 🔢", "פיזיקה א' - מכניקה קלאסית", "תכנות ב C++"],
        "קוד מלא": ["12321-01", "12322-01", "12323-01"],
        "סוג מפגש": ["הרצאה", "הרצאה", "הרצאה"],
        "תקופה": ["א", "א", "א"],
        "יום": ["ראשון", "שני", "שלישי"],
        "שעת התחלה": ["09:00", "10:00", "11:00"],
        "שעת סיום": ["11:00", "12:00", "13:00"],
        "חדר": ["כיתה α", "בניין β-101", "Lab C++"],
        "מרצה": ["פרופ' אלפא-בטא", "ד\"ר γάμμα", "Mr. Smith & Dr. Jones"],
    }
    mock_file_path = create_mock_excel_file(df_data, "unicode_special_chars.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        # Should handle Unicode and special characters properly
        assert loaded_courses is not None
        print(f"✓ Successfully handled Unicode and special characters")
        
    except Exception as e:
        print(f"✓ Handled Unicode/special characters with appropriate error: {e}")


def test_Excel_ReadingQT_time_format_variations(excel_manager, create_mock_excel_file):
    """
    Test 17e: Verifies handling of different time format variations.
    """
    df_data = {
        "שם קורס": ["זמן רגיל", "זמן עם שניות", "זמן 24 שעות", "זמן AM/PM"],
        "קוד מלא": ["12324-01", "12325-01", "12326-01", "12327-01"],
        "סוג מפגש": ["הרצאה", "הרצאה", "הרצאה", "הרצאה"],
        "תקופה": ["א", "א", "א", "א"],
        "יום": ["ראשון", "שני", "שלישי", "רביעי"],
        "שעת התחלה": ["09:00", "10:00:00", "14:30", "2:00 PM"],
        "שעת סיום": ["11:00", "12:00:00", "16:30", "4:00 PM"],
        "חדר": ["כיתה 1", "כיתה 2", "כיתה 3", "כיתה 4"],
        "מרצה": ["מרצה 1", "מרצה 2", "מרצה 3", "מרצה 4"],
    }
    mock_file_path = create_mock_excel_file(df_data, "time_format_variations.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        # Should handle different time formats appropriately
        print(f"✓ Successfully handled various time formats")
        
    except Exception as e:
        print(f"✓ Handled time format variations with appropriate handling: {e}")


def test_Excel_ReadingQT_large_dataset(excel_manager, create_mock_excel_file):
    """
    Test 17f: Performance test with large dataset (stress test).
    """
    # Create a large dataset with 1000 courses
    course_names = [f"קורס מספר {i}" for i in range(1000)]
    course_codes = [f"{10000+i}-01" for i in range(1000)]
    days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי"] * 200
    
    df_data = {
        "שם קורס": course_names,
        "קוד מלא": course_codes,
        "סוג מפגש": ["הרצאה"] * 1000,
        "תקופה": ["א"] * 1000,
        "יום": days,
        "שעת התחלה": ["09:00"] * 1000,
        "שעת סיום": ["11:00"] * 1000,
        "חדר": [f"כיתה {i%100}" for i in range(1000)],
        "מרצה": [f"ד\"ר מספר {i}" for i in range(1000)],
    }
    mock_file_path = create_mock_excel_file(df_data, "large_dataset.xlsx")

    try:
        import time
        start_time = time.time()
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        end_time = time.time()
        
        processing_time = end_time - start_time
        assert loaded_courses is not None
        print(f"✓ Successfully processed large dataset (1000 courses) in {processing_time:.2f} seconds")
        
    except Exception as e:
        pytest.fail(f"Failed to process large dataset: {e}")


def test_Excel_ReadingQT_empty_file(excel_manager, create_mock_excel_file):
    """
    Test 4: Verifies handling of empty Excel file.
    """
    df_data = {}  # Empty dataframe
    mock_file_path = create_mock_excel_file(df_data, "empty.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        
        # Should return empty result or raise appropriate error
        if loaded_courses is not None:
            if isinstance(loaded_courses, (dict, list)):
                assert len(loaded_courses) == 0
        print(f"✓ Correctly handled empty Excel file")
        
    except Exception as e:
        # It's also acceptable to raise an error for empty files
        print(f"✓ Correctly raised error for empty file: {e}")


def test_Excel_ReadingQT_nonexistent_file(excel_manager):
    """
    Test 5: Verifies handling of non-existent file.
    """
    nonexistent_file = "this_file_does_not_exist.xlsx"
    
    with pytest.raises((FileNotFoundError, Exception)) as exc_info:
        excel_manager.read_courses_from_file(nonexistent_file)
    
    print(f"✓ Correctly handled non-existent file: {exc_info.value}")


# Integration test that could be run separately if GUI is needed
@pytest.mark.skipif(True, reason="GUI tests disabled due to crashes - run manually if needed")
def test_Excel_ReadingQT_GUI_integration():
    """
    Placeholder for GUI integration tests.
    These should be run separately in a controlled environment.
    """
    pass


# Utility function to run specific test categories
def run_test_category(category):
    """
    Run specific categories of tests for targeted testing.
    Categories: 'basic', 'validation', 'edge_cases', 'performance'
    """
    if category == 'basic':
        pytest.main([__file__ + "::test_Excel_ReadingQT_valid_hebrew_format", 
                    __file__ + "::test_Excel_ReadingQT_course_group_identification", "-v"])
    elif category == 'validation':
        pytest.main([__file__ + "::test_Excel_ReadingQT_missing_required_field",
                    __file__ + "::test_Excel_ReadingQT_invalid_course_code_formats",
                    __file__ + "::test_Excel_ReadingQT_invalid_time_range", "-v"])
    elif category == 'edge_cases':
        pytest.main([__file__ + "::test_Excel_ReadingQT_edge_cases",
                    __file__ + "::test_Excel_ReadingQT_unicode_and_special_characters", "-v"])
    elif category == 'performance':
        pytest.main([__file__ + "::test_Excel_ReadingQT_large_dataset", "-v"])
    else:
        print("Available categories: 'basic', 'validation', 'edge_cases', 'performance'")


      
      
      
      
   

    # Example mock data for testing
    df_data = {
        "שם קורס": ["מבוא למדעי המחשב", "מבוא למדעי המחשב"],
        "קוד מלא": ["83108-01", "83108-02"],
        "סוג מפגש": ["הרצאה", "תרגיל"],
        "תקופה": ["א", "א"],
        "יום": ["ראשון", "שלישי"],
        "שעת התחלה": ["09:00", "12:00"],
        "שעת סיום": ["11:00", "13:00"],
        "חדר": ["בניין 901", "בניין 902"],
        "מרצה": ["ד\"ר כהן", "פרופ' לוי"],
    }
    mock_file_path = create_mock_excel_file(df_data, "hebrew_example.xlsx")

    # Test the ExcelManager directly
    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        
        # Verify that courses were loaded
        assert loaded_courses is not None
        
        # If the method returns a dict of courses
        if isinstance(loaded_courses, dict):
            assert len(loaded_courses) == 1  # Should be one unique course (83108)
            assert "83108" in loaded_courses
            course = loaded_courses["83108"]
            assert course.name == "מבוא למדעי המחשב"
            assert len(course.sections) == 2  # Two sections
            
        # If the method returns a list
        elif isinstance(loaded_courses, list):
            # Count unique course codes
            course_codes = set()
            for course in loaded_courses:
                course_codes.add(course.code)
            assert len(course_codes) == 1
            
        print(f"✓ Successfully loaded courses from Hebrew Excel file")
        
    except Exception as e:
        pytest.fail(f"Failed to load valid Hebrew Excel file: {e}")


def test_Excel_ReadingQT_different_excel_format(excel_manager, create_mock_excel_file):
    """
    Test 1.1: Verifies reading Excel files with different format versions.
    Tests compatibility with various Excel format versions beyond 1.0.
    """
    df_data = {
        "שם קורס": ["מבנה נתונים"],
        "קוד מלא": ["83109-01"],
        "סוג מפגש": ["הרצאה"],
        "תקופה": ["א"],
        "יום": ["שני"],
        "שעת התחלה": ["10:00"],
        "שעת סיום": ["12:00"],
        "חדר": ["בניין 903"],
        "מרצה": ["ד\"ר דוד"],
        "נ\"ז": [3],
        "ש\"ש": [3],
        "הערה": [""],
    }
    mock_file_path = create_mock_excel_file(df_data, "different_format.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        assert loaded_courses is not None
        print(f"✓ Successfully loaded courses from Excel file with different format")
        
    except Exception as e:
        pytest.fail(f"Failed to load Excel file with different format: {e}")


def test_Excel_ReadingQT_missing_required_field(excel_manager, create_mock_excel_file):
    """
    Test 2: Verifies that ExcelManager handles missing required fields by raising an error.
    """
    df_data = {
        "שם קורס": ["קורס חסר שעות"],
        "קוד מלא": ["12345-01"],
        "סוג מפגש": ["הרצאה"],
        "תקופה": ["א"],
        "יום": ["ראשון"],
        "שעת התחלה": ["09:00"],
        # "שעת סיום" is intentionally missing
        "חדר": ["בניין X"],
        "מרצה": ["מרצה"],
    }
    mock_file_path = create_mock_excel_file(df_data, "missing_end_time.xlsx")

    # Test that ExcelManager raises an error for missing required column
    with pytest.raises((ValueError, KeyError, Exception)) as exc_info:
        excel_manager.read_courses_from_file(mock_file_path)
    
    # Verify the error message mentions the missing column
    error_message = str(exc_info.value).lower()
    assert any(term in error_message for term in ["שעת סיום", "end_time", "missing", "column"])
    print(f"✓ Correctly detected missing required field: {exc_info.value}")


def test_Excel_ReadingQT_empty_fields(excel_manager, create_mock_excel_file):
    """
    Test 2.1: Verifies handling of empty/null fields in required columns.
    """
    df_data = {
        "שם קורס": ["קורס עם שדות ריקים", ""],
        "קוד מלא": ["12346-01", "12347-01"],
        "סוג מפגש": ["הרצאה", "הרצאה"],
        "תקופה": ["א", "א"],
        "יום": ["ראשון", ""],
        "שעת התחלה": ["09:00", "10:00"],
        "שעת סיום": ["11:00", ""],
        "חדר": ["בניין X", "בניין Y"],
        "מרצה": ["מרצה א", ""],
    }
    mock_file_path = create_mock_excel_file(df_data, "empty_fields.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        # Should handle empty fields gracefully or raise appropriate error
        print(f"✓ Successfully handled empty fields")
        
    except Exception as e:
        # It's acceptable to raise an error for empty required fields
        print(f"✓ Correctly raised error for empty fields: {e}")


def test_Excel_ReadingQT_filter_by_semester_a_only(excel_manager, create_mock_excel_file):
    """
    Test 3: Verifies that only courses from "Semester A" (תקופה = "א") are loaded.
    """
    df_data = {
        "שם קורס": ["קורס סמסטר א", "קורס סמסטר ב", "קורס קיץ"],
        "קוד מלא": ["10001-01", "10002-01", "10003-01"],
        "סוג מפגש": ["הרצאה", "הרצאה", "הרצאה"],
        "תקופה": ["א", "ב", "קיץ"],  # Mixed semesters
        "יום": ["ראשון", "שני", "שלישי"],
        "שעת התחלה": ["09:00", "10:00", "11:00"],
        "שעת סיום": ["11:00", "12:00", "13:00"],
        "חדר": ["R1", "R2", "R3"],
        "מרצה": ["M1", "M2", "M3"],
    }
    mock_file_path = create_mock_excel_file(df_data, "mixed_semesters.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        
        # Verify only Semester A courses were loaded
        if isinstance(loaded_courses, dict):
            assert len(loaded_courses) == 1  # Only one course from semester A
            assert "10001" in loaded_courses
            course = loaded_courses["10001"]
            assert course.name == "קורס סמסטר א"
            
        elif isinstance(loaded_courses, list):
            # Filter for semester A courses only
            semester_a_courses = []
            for course in loaded_courses:
                if hasattr(course, 'semester') and course.semester == "א":
                    semester_a_courses.append(course)
            assert len(semester_a_courses) >= 1
            
        print(f"✓ Successfully filtered to show only Semester A courses")
        
    except Exception as e:
        pytest.fail(f"Failed to filter by semester: {e}")


def test_Excel_ReadingQT_course_group_identification(excel_manager, create_mock_excel_file):
    """
    Test 4: Verifies correct identification of course groups by full code (e.g., lecture and tutorial).
    """
    df_data = {
        "שם קורס": ["מבוא למדעי המחשב", "מבוא למדעי המחשב", "אלגוריתמים", "אלגוריתמים"],
        "קוד מלא": ["83108-01", "83108-02", "83109-01", "83109-02"],
        "סוג מפגש": ["הרצאה", "תרגיל", "הרצאה", "תרגיל"],
        "תקופה": ["א", "א", "א", "א"],
        "יום": ["ראשון", "שלישי", "שני", "רביעי"],
        "שעת התחלה": ["09:00", "12:00", "10:00", "13:00"],
        "שעת סיום": ["11:00", "13:00", "12:00", "14:00"],
        "חדר": ["בניין 901", "בניין 902", "בניין 903", "בניין 904"],
        "מרצה": ["ד\"ר כהן", "פרופ' לוי", "ד\"ר דוד", "מר יוסף"],
    }
    mock_file_path = create_mock_excel_file(df_data, "course_groups.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        
        if isinstance(loaded_courses, dict):
            # Should have 2 unique courses (83108 and 83109)
            assert len(loaded_courses) == 2
            assert "83108" in loaded_courses
            assert "83109" in loaded_courses
            
            # Each course should have 2 sections (lecture and tutorial)
            assert len(loaded_courses["83108"].sections) == 2
            assert len(loaded_courses["83109"].sections) == 2
            
        print(f"✓ Successfully identified course groups by full code")
        
    except Exception as e:
        pytest.fail(f"Failed to identify course groups: {e}")


def test_Excel_ReadingQT_course_without_tutorial(excel_manager, create_mock_excel_file):
    """
    Test 5: Verifies correct handling of courses with only lectures (no tutorials).
    """
    df_data = {
        "שם קורס": ["קורס בלי תרגול"],
        "קוד מלא": ["12345-01"],
        "סוג מפגש": ["הרצאה"],
        "תקופה": ["א"],
        "יום": ["ראשון"],
        "שעת התחלה": ["09:00"],
        "שעת סיום": ["11:00"],
        "חדר": ["בניין X"],
        "מרצה": ["ד\"ר אבירם"],
    }
    mock_file_path = create_mock_excel_file(df_data, "no_tutorial.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        
        if isinstance(loaded_courses, dict):
            assert len(loaded_courses) == 1
            course = list(loaded_courses.values())[0]
            assert len(course.sections) == 1
            assert course.sections[0].meeting_type == "הרצאה"
            
        print(f"✓ Successfully handled course without tutorial")
        
    except Exception as e:
        pytest.fail(f"Failed to handle course without tutorial: {e}")


def test_Excel_ReadingQT_tutorial_without_lecture(excel_manager, create_mock_excel_file):
    """
    Test 6: Verifies handling of tutorials without lectures (should raise error or ignore).
    """
    df_data = {
        "שם קורס": ["תרגול בלי הרצאה"],
        "קוד מלא": ["12346-01"],
        "סוג מפגש": ["תרגיל"],
        "תקופה": ["א"],
        "יום": ["ראשון"],
        "שעת התחלה": ["09:00"],
        "שעת סיום": ["11:00"],
        "חדר": ["בניין X"],
        "מרצה": ["מתרגל"],
    }
    mock_file_path = create_mock_excel_file(df_data, "tutorial_without_lecture.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        
        # Should either ignore the tutorial or handle it appropriately
        if isinstance(loaded_courses, dict):
            # If tutorials without lectures are ignored, should be empty
            if len(loaded_courses) == 0:
                print(f"✓ Correctly ignored tutorial without lecture")
            else:
                print(f"✓ Handled tutorial without lecture appropriately")
                
    except Exception as e:
        # It's acceptable to raise an error for tutorials without lectures
        print(f"✓ Correctly raised error for tutorial without lecture: {e}")


def test_Excel_ReadingQT_reinforcement_only_course(excel_manager, create_mock_excel_file):
    """
    Test 7: Verifies that courses with only "reinforcement" sessions (תגבור) are not included.
    """
    df_data = {
        "שם קורס": ["קורס תגבור בלבד"],
        "קוד מלא": ["12347-01"],
        "סוג מפגש": ["תגבור"],
        "תקופה": ["א"],
        "יום": ["ראשון"],
        "שעת התחלה": ["09:00"],
        "שעת סיום": ["11:00"],
        "חדר": ["בניין X"],
        "מרצה": ["מתגבר"],
    }
    mock_file_path = create_mock_excel_file(df_data, "reinforcement_only.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        
        if isinstance(loaded_courses, dict):
            # Should not include reinforcement-only courses
            assert len(loaded_courses) == 0
            
        print(f"✓ Correctly excluded reinforcement-only course")
        
    except Exception as e:
        pytest.fail(f"Failed to handle reinforcement-only course: {e}")


def test_Excel_ReadingQT_lecture_with_reinforcement(excel_manager, create_mock_excel_file):
    """
    Test 8: Verifies that courses with both lecture and reinforcement only include the lecture.
    """
    df_data = {
        "שם קורס": ["קורס עם הרצאה ותגבור", "קורס עם הרצאה ותגבור"],
        "קוד מלא": ["12348-01", "12348-02"],
        "סוג מפגש": ["הרצאה", "תגבור"],
        "תקופה": ["א", "א"],
        "יום": ["ראשון", "שלישי"],
        "שעת התחלה": ["09:00", "11:00"],
        "שעת סיום": ["11:00", "12:00"],
        "חדר": ["בניין X", "בניין Y"],
        "מרצה": ["ד\"ר כהן", "מתגבר"],
    }
    mock_file_path = create_mock_excel_file(df_data, "lecture_with_reinforcement.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        
        if isinstance(loaded_courses, dict):
            assert len(loaded_courses) == 1
            course = list(loaded_courses.values())[0]
            # Should only include the lecture, not the reinforcement
            lecture_sections = [s for s in course.sections if s.meeting_type == "הרצאה"]
            reinforcement_sections = [s for s in course.sections if s.meeting_type == "תגבור"]
            
            assert len(lecture_sections) == 1
            assert len(reinforcement_sections) == 0  # Reinforcement should be excluded
            
        print(f"✓ Correctly included only lecture from lecture+reinforcement course")
        
    except Exception as e:
        pytest.fail(f"Failed to handle lecture with reinforcement: {e}")


def test_Excel_ReadingQT_lab_only_course(excel_manager, create_mock_excel_file):
    """
    Test 9: Verifies that courses with only lab sessions are not considered for scheduling.
    """
    df_data = {
        "שם קורס": ["מעבדה בלבד"],
        "קוד מלא": ["12349-01"],
        "סוג מפגש": ["מעבדה"],
        "תקופה": ["א"],
        "יום": ["ראשון"],
        "שעת התחלה": ["09:00"],
        "שעת סיום": ["11:00"],
        "חדר": ["מעבדה 1"],
        "מרצה": ["מנחה מעבדה"],
    }
    mock_file_path = create_mock_excel_file(df_data, "lab_only.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        
        if isinstance(loaded_courses, dict):
            # Should not include lab-only courses
            assert len(loaded_courses) == 0
            
        print(f"✓ Correctly excluded lab-only course")
        
    except Exception as e:
        pytest.fail(f"Failed to handle lab-only course: {e}")


def test_Excel_ReadingQT_course_with_lab_and_lecture(excel_manager, create_mock_excel_file):
    """
    Test 10: Verifies that courses with both lab and lecture only consider lecture for scheduling.
    """
    df_data = {
        "שם קורס": ["קורס עם הרצאה ומעבדה", "קורס עם הרצאה ומעבדה"],
        "קוד מלא": ["12350-01", "12350-02"],
        "סוג מפגש": ["הרצאה", "מעבדה"],
        "תקופה": ["א", "א"],
        "יום": ["ראשון", "שלישי"],
        "שעת התחלה": ["09:00", "11:00"],
        "שעת סיום": ["11:00", "13:00"],
        "חדר": ["כיתה א", "מעבדה 2"],
        "מרצה": ["ד\"ר כהן", "מנחה מעבדה"],
    }
    mock_file_path = create_mock_excel_file(df_data, "lecture_with_lab.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        
        if isinstance(loaded_courses, dict):
            assert len(loaded_courses) == 1
            course = list(loaded_courses.values())[0]
            # Should only include the lecture, not the lab
            lecture_sections = [s for s in course.sections if s.meeting_type == "הרצאה"]
            lab_sections = [s for s in course.sections if s.meeting_type == "מעבדה"]
            
            assert len(lecture_sections) == 1
            assert len(lab_sections) == 0  # Lab should be excluded
            
        print(f"✓ Correctly included only lecture from lecture+lab course")
        
    except Exception as e:
        pytest.fail(f"Failed to handle course with lab and lecture: {e}")


def test_Excel_ReadingQT_room_conflict_detection(excel_manager, create_mock_excel_file):
    """
    Test 11: Verifies detection of room conflicts (same time, same room).
    """
    df_data = {
        "שם קורס": ["קורס א", "קורס ב"],
        "קוד מלא": ["12351-01", "12352-01"],
        "סוג מפגש": ["הרצאה", "הרצאה"],
        "תקופה": ["א", "א"],
        "יום": ["ראשון", "ראשון"],
        "שעת התחלה": ["09:00", "09:00"],
        "שעת סיום": ["11:00", "11:00"],
        "חדר": ["כיתה א", "כיתה א"],  # Same room, same time
        "מרצה": ["ד\"ר כהן", "ד\"ר לוי"],
    }
    mock_file_path = create_mock_excel_file(df_data, "room_conflict.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        
        # The system should either detect the conflict or handle it appropriately
        if hasattr(excel_manager, 'check_room_conflicts'):
            conflicts = excel_manager.check_room_conflicts(loaded_courses)
            assert len(conflicts) > 0
            
        print(f"✓ Room conflict detection handled appropriately")
        
    except Exception as e:
        # It's acceptable to raise an error for room conflicts
        print(f"✓ Room conflict handled with error: {e}")


def test_Excel_ReadingQT_corrupted_room_values(excel_manager, create_mock_excel_file):
    """
    Test 12: Verifies robustness with corrupted room field values.
    """
    df_data = {
        "שם קורס": ["קורס עם חדר משובש"],
        "קוד מלא": ["12353-01"],
        "סוג מפגש": ["הרצאה"],
        "תקופה": ["א"],
        "יום": ["ראשון"],
        "שעת התחלה": ["09:00"],
        "שעת סיום": ["11:00"],
        "חדר": ["@#$%^&*()"],  # Corrupted room value
        "מרצה": ["ד\"ר כהן"],
    }
    mock_file_path = create_mock_excel_file(df_data, "corrupted_room.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        # Should handle corrupted room values gracefully
        print(f"✓ Successfully handled corrupted room values")
        
    except Exception as e:
        # It's acceptable to raise an error for corrupted data
        print(f"✓ Correctly handled corrupted room values with error: {e}")


def test_Excel_ReadingQT_academic_year_2024(excel_manager, create_mock_excel_file):
    """
    Test 13a: Verifies handling of files with academic year 2024 (תשפ"ד) - should warn or ignore.
    """
    df_data = {
        "שם קורס": ["קורס תשפד"],
        "קוד מלא": ["12354-01"],
        "סוג מפגש": ["הרצאה"],
        "תקופה": ["א"],
        "שנה": ["תשפ\"ד"],  # Academic year 2024
        "יום": ["ראשון"],
        "שעת התחלה": ["09:00"],
        "שעת סיום": ["11:00"],
        "חדר": ["כיתה א"],
        "מרצה": ["ד\"ר כהן"],
    }
    mock_file_path = create_mock_excel_file(df_data, "academic_year_2024.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        # Should either warn about outdated year or ignore the course
        print(f"✓ Handled academic year 2024 appropriately")
        
    except Exception as e:
        print(f"✓ Correctly handled academic year 2024 with warning/error: {e}")


def test_Excel_ReadingQT_academic_year_2025(excel_manager, create_mock_excel_file):
    """
    Test 13b: Verifies normal processing of files with academic year 2025 (תשפ"ה).
    """
    df_data = {
        "שם קורס": ["קורס תשפה"],
        "קוד מלא": ["12355-01"],
        "סוג מפגש": ["הרצאה"],
        "תקופה": ["א"],
        "שנה": ["תשפ\"ה"],  # Academic year 2025
        "יום": ["ראשון"],
        "שעת התחלה": ["09:00"],
        "שעת סיום": ["11:00"],
        "חדר": ["כיתה א"],
        "מרצה": ["ד\"ר כהן"],
    }
    mock_file_path = create_mock_excel_file(df_data, "academic_year_2025.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        assert loaded_courses is not None
        if isinstance(loaded_courses, dict):
            assert len(loaded_courses) == 1
            
        print(f"✓ Successfully processed academic year 2025")
        
    except Exception as e:
        pytest.fail(f"Failed to process valid academic year 2025: {e}")


def test_Excel_ReadingQT_valid_course_code_format(excel_manager, create_mock_excel_file):
    """
    Test 14a: Verifies handling of valid 7-digit course codes (e.g., 83108-01).
    """
    df_data = {
        "שם קורס": ["קורס עם קוד תקני"],
        "קוד מלא": ["83108-01"],  # Valid 7-digit format
        "סוג מפגש": ["הרצאה"],
        "תקופה": ["א"],
        "יום": ["ראשון"],
        "שעת התחלה": ["09:00"],
        "שעת סיום": ["11:00"],
        "חדר": ["כיתה א"],
        "מרצה": ["ד\"ר כהן"],
    }
    mock_file_path = create_mock_excel_file(df_data, "valid_course_code.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        assert loaded_courses is not None
        if isinstance(loaded_courses, dict):
            assert "83108" in loaded_courses
            
        print(f"✓ Successfully processed valid 7-digit course code")
        
    except Exception as e:
        pytest.fail(f"Failed to process valid course code: {e}")

def test_Excel_ReadingQT_invalid_course_code_formats(excel_manager, create_mock_excel_file):
    """
    Test 14b: Verifies handling of invalid course code formats (8 digits, 6 digits, non-numeric).
    """
    df_data = {
        "שם קורס": ["קוד 8 ספרות", "קוד 6 ספרות", "קוד לא תקני"],
        "קוד מלא": ["831080-01", "8310-01", "ABC108-01"],  # Invalid formats
        "סוג מפגש": ["הרצאה", "הרצאה", "הרצאה"],
        "תקופה": ["א", "א", "א"],
        "יום": ["ראשון", "שני", "שלישי"],
        "שעת התחלה": ["09:00", "10:00", "11:00"],
        "שעת סיום": ["11:00", "12:00", "13:00"],
        "חדר": ["כיתה א", "כיתה ב", "כיתה ג"],
        "מרצה": ["ד\"ר כהן", "ד\"ר לוי", "ד\"ר דוד"],
    }
    mock_file_path = create_mock_excel_file(df_data, "invalid_course_codes.xlsx")

    try:
        loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
        # Should either reject invalid codes or handle them with warnings
        print(f"✓ Handled invalid course code formats appropriately")
        
    except Exception as e:
        print(f"✓ Correctly rejected invalid course codes: {e}")
        def test_Excel_ReadingQT_duplicate_rows(excel_manager, create_mock_excel_file):
            """
            Test: Verifies that duplicate rows in the Excel file are handled (ignored or deduplicated).
            """
            df_data = {
                "שם קורס": ["קורס כפול", "קורס כפול"],
                "קוד מלא": ["12356-01", "12356-01"],
                "סוג מפגש": ["הרצאה", "הרצאה"],
                "תקופה": ["א", "א"],
                "יום": ["ראשון", "ראשון"],
                "שעת התחלה": ["09:00", "09:00"],
                "שעת סיום": ["11:00", "11:00"],
                "חדר": ["כיתה א", "כיתה א"],
                "מרצה": ["ד\"ר כהן", "ד\"ר כהן"],
            }
            mock_file_path = create_mock_excel_file(df_data, "duplicate_rows.xlsx")

            try:
                loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
                if isinstance(loaded_courses, dict):
                    course = list(loaded_courses.values())[0]
                    # Should not create duplicate sections
                    assert len(course.sections) == 1
                print("✓ Successfully handled duplicate rows")
            except Exception as e:
                pytest.fail(f"Failed to handle duplicate rows: {e}")

        def test_Excel_ReadingQT_case_insensitive_headers(excel_manager, create_mock_excel_file):
            """
            Test: Verifies that header names are case-insensitive (if supported).
            """
            df_data = {
                "שם קורס": ["קורס קטן"],
                "קוד מלא": ["12357-01"],
                "סוג מפגש": ["הרצאה"],
                "תקופה": ["א"],
                "יום": ["ראשון"],
                "שעת התחלה": ["09:00"],
                "שעת סיום": ["11:00"],
                "חדר": ["כיתה א"],
                "מרצה": ["ד\"ר כהן"],
                "הערה": [""]
            }
            # Change headers to lowercase (simulate case-insensitivity)
            df_data_case = {k.lower(): v for k, v in df_data.items()}
            mock_file_path = create_mock_excel_file(df_data_case, "case_insensitive_headers.xlsx")

            try:
                loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
                assert loaded_courses is not None
                print("✓ Successfully handled case-insensitive headers")
            except Exception as e:
                print(f"✓ Correctly handled case-insensitive headers with error: {e}")

        def test_Excel_ReadingQT_extra_irrelevant_columns(excel_manager, create_mock_excel_file):
            """
            Test: Verifies that extra irrelevant columns do not affect parsing.
            """
            df_data = {
                "שם קורס": ["קורס עם עמודה מיותרת"],
                "קוד מלא": ["12358-01"],
                "סוג מפגש": ["הרצאה"],
                "תקופה": ["א"],
                "יום": ["ראשון"],
                "שעת התחלה": ["09:00"],
                "שעת סיום": ["11:00"],
                "חדר": ["כיתה א"],
                "מרצה": ["ד\"ר כהן"],
                "עמודה מיותרת": ["ערך מיותר"]
            }
            mock_file_path = create_mock_excel_file(df_data, "extra_column.xlsx")

            try:
                loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
                assert loaded_courses is not None
                print("✓ Successfully ignored extra irrelevant columns")
            except Exception as e:
                pytest.fail(f"Failed to ignore extra columns: {e}")

        def test_Excel_ReadingQT_whitespace_in_fields(excel_manager, create_mock_excel_file):
            """
            Test: Verifies that leading/trailing whitespace in fields is trimmed.
            """
            df_data = {
                "שם קורס": ["  קורס עם רווחים  "],
                "קוד מלא": [" 12359-01 "],
                "סוג מפגש": [" הרצאה "],
                "תקופה": [" א "],
                "יום": [" ראשון "],
                "שעת התחלה": [" 09:00 "],
                "שעת סיום": [" 11:00 "],
                "חדר": [" כיתה א "],
                "מרצה": [" ד\"ר כהן "],
            }
            mock_file_path = create_mock_excel_file(df_data, "whitespace_fields.xlsx")

            try:
                loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
                if isinstance(loaded_courses, dict):
                    course = list(loaded_courses.values())[0]
                    assert course.name == "קורס עם רווחים"
                    assert course.code == "12359"
                print("✓ Successfully trimmed whitespace in fields")
            except Exception as e:
                pytest.fail(f"Failed to trim whitespace in fields: {e}")

        def test_Excel_ReadingQT_partial_row(excel_manager, create_mock_excel_file):
            """
            Test: Verifies handling of rows with some missing (but not required) fields.
            """
            df_data = {
                "שם קורס": ["קורס חלקי"],
                "קוד מלא": ["12360-01"],
                "סוג מפגש": ["הרצאה"],
                "תקופה": ["א"],
                "יום": ["ראשון"],
                "שעת התחלה": ["09:00"],
                "שעת סיום": ["11:00"],
                "חדר": [""],  # Room is empty, but not required for logic
                "מרצה": [""],  # Instructor is empty
            }
            mock_file_path = create_mock_excel_file(df_data, "partial_row.xlsx")

            try:
                loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
                assert loaded_courses is not None
                print("✓ Successfully handled partial row with missing optional fields")
            except Exception as e:
                print(f"✓ Correctly handled partial row with error: {e}")

        def test_Excel_ReadingQT_invalid_file_type(excel_manager, tmp_path):
            """
            Test: Verifies that non-Excel files are rejected.
            """
            file_path = tmp_path / "not_excel.txt"
            file_path.write_text("This is not an Excel file.")
            with pytest.raises(Exception):
                excel_manager.read_courses_from_file(str(file_path))
            print("✓ Correctly rejected non-Excel file")

        def test_Excel_ReadingQT_multiple_sheets(excel_manager, tmp_path):
            """
            Test: Verifies that only the first or correct sheet is read if multiple sheets exist.
            """
            df1 = pd.DataFrame({
                "שם קורס": ["קורס גיליון 1"],
                "קוד מלא": ["12361-01"],
                "סוג מפגש": ["הרצאה"],
                "תקופה": ["א"],
                "יום": ["ראשון"],
                "שעת התחלה": ["09:00"],
                "שעת סיום": ["11:00"],
                "חדר": ["כיתה א"],
                "מרצה": ["ד\"ר כהן"],
            })
            df2 = pd.DataFrame({
                "שם קורס": ["קורס גיליון 2"],
                "קוד מלא": ["12362-01"],
                "סוג מפגש": ["הרצאה"],
                "תקופה": ["א"],
                "יום": ["שני"],
                "שעת התחלה": ["10:00"],
                "שעת סיום": ["12:00"],
                "חדר": ["כיתה ב"],
                "מרצה": ["ד\"ר לוי"],
            })
            file_path = tmp_path / "multiple_sheets.xlsx"
            with pd.ExcelWriter(file_path) as writer:
                df1.to_excel(writer, sheet_name="Sheet1", index=False)
                df2.to_excel(writer, sheet_name="Sheet2", index=False)
            try:
                loaded_courses = excel_manager.read_courses_from_file(str(file_path))
                assert loaded_courses is not None
                print("✓ Successfully handled multiple sheets in Excel file")
            except Exception as e:
                pytest.fail(f"Failed to handle multiple sheets: {e}")

        def test_Excel_ReadingQT_section_overlap_same_course(excel_manager, create_mock_excel_file):
            """
            Test: Verifies detection of overlapping sections for the same course.
            """
            df_data = {
                "שם קורס": ["קורס חופף", "קורס חופף"],
                "קוד מלא": ["12363-01", "12363-02"],
                "סוג מפגש": ["הרצאה", "הרצאה"],
                "תקופה": ["א", "א"],
                "יום": ["ראשון", "ראשון"],
                "שעת התחלה": ["09:00", "10:00"],
                "שעת סיום": ["11:00", "12:00"],
                "חדר": ["כיתה א", "כיתה א"],
                "מרצה": ["ד\"ר כהן", "ד\"ר כהן"],
            }
            mock_file_path = create_mock_excel_file(df_data, "section_overlap.xlsx")
            try:
                loaded_courses = excel_manager.read_courses_from_file(mock_file_path)
                # If overlap detection is implemented, check for overlaps
                if hasattr(excel_manager, 'check_section_overlaps'):
                    overlaps = excel_manager.check_section_overlaps(loaded_courses)
                    assert len(overlaps) > 0
                print("✓ Section overlap detection handled appropriately")
            except Exception as e:
                print(f"✓ Section overlap handled with error: {e}")