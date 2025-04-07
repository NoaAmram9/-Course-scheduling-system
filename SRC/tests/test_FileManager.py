import pytest
import os
from tempfile import NamedTemporaryFile
from SRC.Models.TimeTable import TimeTable
from SRC.Models.Course import Course
from SRC.Models.LessonTimes import LessonTimes
from SRC.Models.Lesson import Lesson
from SRC.Services.FileManager import FileManager
from SRC.Controller.Controller import Controller

file_manager = FileManager()

def test_courses_file_read():
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("$$$$\nCourse\n12345\nInstructor\nL S,5,10:00,16:00,605,061\nT S,5,16:00,17:00,605,061\n" \
        "$$$$\nCourse 2\n14395\nInstructor 2\nL S,1,14:00,16:00,1401,4 S,2,14:00,16:00,1401,4\nT " \
        "S,2,18:00,19:00,1100,22\n")
        test_file = file.name

    courses = file_manager.read_courses_from_file(test_file)

    assert len(courses) == 2 
    assert isinstance(courses[0], Course) 
    os.remove(test_file)

def test_courses_file_not_found():
    courses = file_manager.read_courses_from_file("non_existing_file.txt")
    assert courses == []

def test_courses_empty_file():
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        test_file = file.name

    courses = file_manager.read_courses_from_file(test_file)
    assert courses == []
    os.remove(test_file) 

def test_wrong_format_courses_file():
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("Course\n12345\nL S,5,10:00,16:00,605,061\nT S,5,16:00,17:00,605,061\n") #instructor missing
        test_file = file.name

    courses = file_manager.read_courses_from_file(test_file)
    assert courses == []
    os.remove(test_file)

def test_course_numbers_file_read():
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("11111\n22222\n33333\n")
        test_file = file.name
    
    course_numbers_selection = file_manager.read_course_numbers_from_file(test_file)
    assert len(course_numbers_selection) == 3
    assert course_numbers_selection == ["11111", "22222", "33333"]
    os.remove(test_file)

def test_invalid_course_numbers_selection_file():
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("abcde\nxyz12\n")
        test_file = file.name
    
    course_numbers_selection1 = file_manager.read_course_numbers_from_file(test_file)
    assert course_numbers_selection1 == []

    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("12654\n124@$\n")
        test_file = file.name
    
    course_numbers_selection2 = file_manager.read_course_numbers_from_file(test_file)
    assert course_numbers_selection2 == []
    os.remove(test_file)

def test_invalid_course_numbers_courses_file(): 
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("$$$$\nCourse Name\n1234A\nInstructor Name\nL S,5,10:00,16:00,605,061\nT S,5,16:00,17:00,605,061\n" \
        "$$$$\nCourse Name 2\n123\nInstructor Name\nL S,1,14:00,16:00,1401,4 S,2,14:00,16:00,1401,4\nT " \
        "S,2,18:00,19:00,1100,22\n")
        test_file = file.name

    courses = file_manager.read_courses_from_file(test_file)
    assert len(courses) == 0
    os.remove(test_file)

def test_read_file_with_invalid_encoding():
    with NamedTemporaryFile(delete=False, mode='wb') as bad_file:
        bad_file.write(b'\x80\x81\x82\x83')  # Invalid UTF-8
        bad_filename = bad_file.name

    result = file_manager.read_course_numbers_from_file(bad_filename)
    assert result == []
    os.remove(bad_filename)

def test_too_many_selected_courses():
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("11111\n22222\n33333\n44444\n55555\n66666\n77777\n88888\n")
        test_file = file.name

    result = file_manager.read_course_numbers_from_file(test_file)
    assert result == []
    os.remove(test_file)

def test_course_selection_file_not_found():
    courses = file_manager.read_course_numbers_from_file("non_existing_file.txt")
    assert courses == []

def test_course_selection_file_empty():
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        test_file = file.name

    result = file_manager.read_course_numbers_from_file(test_file)
    assert result == []
    os.remove(test_file)

def test_course_requires_lecture_and_exercise():
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("$$$$\nCourse\n12345\nInstructor\nL S,1,08:00,10:00,101,201\n") #no exercise
        test_file = file.name

    courses = file_manager.read_courses_from_file(test_file)
    assert courses == []
    os.remove(test_file)

    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("$$$$\nCourse\n12345\nInstructor\nT S,2,10:00,12:00,102,202\n") #no lecture
        test_file = file.name

    courses = file_manager.read_courses_from_file(test_file)
    assert courses == []
    os.remove(test_file)

def test_output_format():
    lesson_time1 = LessonTimes("10:00", "12:00", "1")
    lesson_time2 = LessonTimes("13:00", "14:00", "3")
    lecture = Lesson(lesson_time1, "L", "100", "101")
    exercise = Lesson(lesson_time2, "T", "100", "102")
    course = Course("Math", "12345", "Dr. Tom", [lecture], [exercise], [])

    with NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8') as temp_file:
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

    with NamedTemporaryFile(delete=False, mode='r+', encoding='utf-8') as temp_file:
        file_manager.write_schedule_to_file(temp_file.name, [timetable])
        temp_file.seek(0)
        content = temp_file.read()

    os.remove(temp_file.name)

    assert "Math" in content
    assert "12345" in content
    assert "Dr. Tom" in content
    assert "L S,1,10:00,12:00,100,101" in content
    assert "T S,3,13:00,14:00,100,102" in content
    assert "*****" in content

def test_invalid_course_number_length_selection_file():
    with NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as file:
        file.write("123\n")
        file.write("123456\n")
        file.write("12345\n")
        test_file = file.name

    result = file_manager.read_course_numbers_from_file(test_file)
    assert result == []
    os.remove(test_file)

def test_duplicate_course_selection_file():
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("12345\n23456\n12345\n")  # 12345 is duplicated
        test_file = file.name

    result = file_manager.read_course_numbers_from_file(test_file)
    assert result == []
    os.remove(test_file)

def test_duplicate_courses_file():
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("$$$$\nCourse\n12345\nInstructor\nL S,5,10:00,16:00,605,061\nT S,5,16:00,17:00,605,061\n" \
        "$$$$\nCourse\n12345\nInstructor\nL S,5,10:00,16:00,605,061\nT S,5,16:00,17:00,605,061\n")
        test_file = file.name

    courses = file_manager.read_courses_from_file(test_file)
    assert len(courses) == 1 #Duplicate courses should be skipped."
    assert courses[0].code == "12345"
    assert courses[0].name == "Course"
    assert courses[0].instructor == "Instructor"
    os.remove(test_file)

def test_validate_course_numbers_exist_in_courses_file():
    controller = Controller()

    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("$$$$\nCourse 1\n12345\nInstructor 1\nL S,5,10:00,12:00,605,061\n" \
        "$$$$\nCourse 2\n12346\nInstructor 2\nT S,5,14:00,16:00,605,061\n")
        courses_file = file.name

    chosen_courses_file_content = "12345\n12347\n"
    
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write(chosen_courses_file_content)
        chosen_courses_file = file.name

    assert not file_manager.validate_course_numbers_exist(chosen_courses_file, courses_file)
    schedules = controller.create_schedules(chosen_courses_file_content, chosen_courses_file, courses_file)
    assert len(schedules) == 0
    os.remove(courses_file)
    os.remove(chosen_courses_file)