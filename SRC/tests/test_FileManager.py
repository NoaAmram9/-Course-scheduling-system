import pytest
import os
from tempfile import NamedTemporaryFile
from SRC.Models.Course import Course
from SRC.Models.LessonTimes import LessonTimes
from SRC.Models.Lesson import Lesson
from SRC.Services.FileManager import FileManager

def test_valid_file_read():
    file_manager = FileManager()

    # Create a temporary file with valid content
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("$$$$\nCourse Name\n12345\nInstructor Name\nL S,5,10:00,16:00,605,061\nT S,5,16:00,17:00,605,061\n" \
        "$$$$\nCourse Name 2\n14395\nInstructor Name\nL S,1,14:00,16:00,1401,4 S,2,14:00,16:00,1401,4\nT " \
        "S,2,18:00,19:00,1100,22\n")
        test_file = file.name
    
    # Read courses from the file
    courses = file_manager.read_courses_from_file(test_file)

    # Assertions
    assert len(courses) == 2  # Ensure that at least one course is loaded
    assert isinstance(courses[0], Course)  # Ensure that the data is converted to Course objects
    os.remove(test_file)  # Clean up

def test_file_not_found():
    file_manager = FileManager()
    
    # Try to read a non-existing file
    courses = file_manager.read_courses_from_file("non_existing_file.txt")

    # Assertions
    assert courses == [], "The system should return an empty list if the file doesn't exist."

def test_empty_file():
    file_manager = FileManager()
    
    # Create an empty file
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        test_file = file.name

    # Try reading the empty file
    courses = file_manager.read_courses_from_file(test_file)

    # Assertions
    assert courses == [], "The system should return an empty list if the file is empty."
    os.remove(test_file)  # Clean up

def test_wrong_format_file():
    file_manager = FileManager()
    
    # Create an empty file
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("Course Name\n12345\nL S,5,10:00,16:00,605,061\nT S,5,16:00,17:00,605,061\n")
        test_file = file.name

    # Try reading the empty file
    courses = file_manager.read_courses_from_file(test_file)

    # Assertions
    assert courses == [], "The system should return an empty list if the file is empty."
    os.remove(test_file)  # Clean up

def test_valid_course_numbers():
    file_manager = FileManager()

    # Simulate a file with valid course numbers
    course_file_content = "12345\n23456\n34567\n"
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write(course_file_content)
        test_file = file.name
    
    # Read course numbers from file
    course_numbers = file_manager.read_course_numbers_from_file(test_file)
    
    # Assertions
    assert len(course_numbers) == 3, "The system should load the correct number of course numbers."
    assert course_numbers == ["12345", "23456", "34567"], "The course numbers should match the expected values."
    os.remove(test_file)  # Clean up

def test_invalid_course_numbers():
    file_manager = FileManager()

    # Simulate a file with invalid course numbers (non-numeric)
    course_file_content1 = "abcde\nxyz12\n"
    course_file_content2 = "12654\n124@$\n"
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write(course_file_content1)
        test_file = file.name
    
    # Read course numbers from file
    course_numbers1 = file_manager.read_course_numbers_from_file(test_file)
    
    # Assertions
    assert course_numbers1 == [], "The system should return an empty list if the course numbers are invalid."

    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write(course_file_content2)
        test_file = file.name
    
    # Read course numbers from file
    course_numbers2 = file_manager.read_course_numbers_from_file(test_file)
    
    # Assertions
    assert course_numbers2 == [], "The system should return an empty list if the course numbers are invalid."
    os.remove(test_file)  # Clean up

def test_read_course_numbers_from_file_too_many_courses():
    file_manager = FileManager()
    
    # Create a temporary file with more than 7 course numbers
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("1\n2\n3\n4\n5\n6\n7\n8\n")
        test_file = file.name

    # Try reading the file with too many courses
    result = file_manager.read_course_numbers_from_file(test_file)

    # Assertions: The system should return an empty list due to too many courses
    assert result == []

    # Clean up
    os.remove(test_file)

def test_read_course_numbers_from_file_valid_courses():
    file_manager = FileManager()
    
    # Create a temporary file with exactly 7 course numbers
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        file.write("1\n2\n3\n4\n5\n6\n7")
        test_file = file.name

    # Try reading the file with exactly 7 courses
    result = file_manager.read_course_numbers_from_file(test_file)

    # Assertions: The system should return the list of course numbers
    assert result == ['1', '2', '3', '4', '5', '6', '7']

    # Clean up
    os.remove(test_file)

def test_read_course_numbers_from_file_empty():
    file_manager = FileManager()
    
    # Create a temporary empty file
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as file:
        test_file = file.name

    # Try reading the empty file
    result = file_manager.read_course_numbers_from_file(test_file)

    # Assertions: The system should return an empty list for an empty file
    assert result == []

    # Clean up
    os.remove(test_file)