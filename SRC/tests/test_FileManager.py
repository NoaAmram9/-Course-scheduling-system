import os
import pytest
from SRC.Models.Course import Course
from SRC.Models.ValidationError import ValidationError
from SRC.Models.TimeTable import TimeTable
from SRC.Models.LessonTimes import LessonTimes
from SRC.Models.Lesson import Lesson
from SRC.Services.FileManager import FileManager
from SRC.Controller.Controller import Controller

file_manager = FileManager()

DATA_DIR = os.path.join(os.path.dirname(__file__), "tests_data")

def get_path(filename):
    return os.path.join(DATA_DIR, filename)

def test_courses_file_read():
    courses = file_manager.read_courses_from_file(get_path("valid_courses.txt"))
    assert len(courses) == 2
    assert isinstance(courses[0], Course)

def test_courses_file_not_found():
    courses = file_manager.read_courses_from_file("non_existing_file.txt")
    assert len(courses) == 1
    assert isinstance(courses[0], ValidationError)

def test_courses_empty_file():
    courses = file_manager.read_courses_from_file(get_path("empty.txt"))
    assert len(courses) == 1
    assert isinstance(courses[0], ValidationError)

def test_wrong_format_courses_file():
    courses = file_manager.read_courses_from_file(get_path("invalid_courses.txt"))
    assert len(courses) == 1
    assert isinstance(courses[0], ValidationError)

def test_course_numbers_file_read():
    course_numbers = file_manager.read_course_numbers_from_file(get_path("chosen_courses_valid.txt"))
    assert course_numbers == ["12345", "12347"]

def test_invalid_course_numbers_selection_file():
    course_numbers = file_manager.read_course_numbers_from_file(get_path("chosen_courses_invalid.txt"))
    assert course_numbers == []

def test_invalid_course_numbers_courses_file():
    courses = file_manager.read_courses_from_file(get_path("courses_with_invalid_codes.txt"))
    assert all(isinstance(c, ValidationError) for c in courses)

def test_read_file_with_invalid_encoding():
    result = file_manager.read_course_numbers_from_file(get_path("encoding_error.bin"))
    assert result == []

def test_too_many_selected_courses():
    result = file_manager.read_course_numbers_from_file(get_path("too_many_selected.txt"))
    assert result == []

def test_course_selection_file_not_found():
    result = file_manager.read_course_numbers_from_file("non_existing_file.txt")
    assert result == []

def test_course_selection_file_empty():
    result = file_manager.read_course_numbers_from_file(get_path("empty.txt"))
    assert result == []

def test_duplicate_course_selection_file():
    result = file_manager.read_course_numbers_from_file(get_path("duplicate_selection.txt"))
    assert result == []

def test_duplicate_courses_file():
    courses = file_manager.read_courses_from_file(get_path("duplicate_courses.txt"))
    assert len(courses) == 1
    assert isinstance(courses[0], ValidationError)
    assert "duplicate" in courses[0].message.lower()

def test_validate_course_numbers_exist_in_courses_file():
    controller = Controller()
    result = file_manager.validate_course_numbers_exist(
        get_path("chosen_courses_not_match.txt"),
        get_path("valid_courses.txt")
    )
    assert not result
    schedules = controller.create_schedules("12345\n99999\n", get_path("chosen_courses_not_match.txt"), get_path("valid_courses.txt"))
    assert len(schedules) == 0

def test_output_format():
    lesson_time1 = LessonTimes("10:00", "12:00", "1")
    lesson_time2 = LessonTimes("13:00", "14:00", "3")
    lecture = Lesson(lesson_time1, "L", "100", "101")
    exercise = Lesson(lesson_time2, "T", "100", "102")
    course = Course("Math", "12345", "Dr. Tom", [lecture], [exercise], [])

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as temp_file:
        file_manager.write_courses_to_file(temp_file, [course])
        temp_file.seek(0)
        content = temp_file.read()
    os.remove(temp_file.name)

    assert "Math" in content
    assert "12345" in content
    assert "Dr. Tom" in content
    assert "L S,1,10:00,12:00,100,101" in content
    assert "T S,3,13:00,14:00,100,102" in content
    assert "$$$$" in content

def test_write_schedule_to_file():
    lesson_time1 = LessonTimes("10:00", "12:00", "1")
    lesson_time2 = LessonTimes("13:00", "14:00", "3")
    lecture = Lesson(lesson_time1, "L", "100", "101")
    exercise = Lesson(lesson_time2, "T", "100", "102")
    course = Course("Math", "12345", "Dr. Tom", [lecture], [exercise], [])
    timetable = TimeTable([course])

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as temp_file:
        file_manager.write_schedule_to_file(temp_file.name, [timetable])
        temp_file.seek(0)
        content = temp_file.read()
    os.remove(temp_file.name)

    assert "Math" in content
    assert "12345" in content
    assert "*****" in content