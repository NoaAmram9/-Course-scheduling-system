import pytest
from SRC.Services.ScheduleService import ScheduleService
from SRC.Models.Course import Course
from SRC.Models.Lesson import Lesson
from SRC.Models.LessonTimes import LessonTimes
import time

service = ScheduleService()

def test_generate_all_possible_schedules():
    course1 = Course(
        name="Course1",
        code="11111",
        instructor="Instructor1",
        lectures=[
            Lesson(LessonTimes("08:00", "09:00", "1"), "L", "100", "101"),
            Lesson(LessonTimes("09:00", "10:00", "1"), "L", "100", "102")
        ],
        exercises=[
            Lesson(LessonTimes("10:00", "11:00", "1"), "T", "100", "103")
        ],
        labs=[]
    )

    course2 = Course(
        name="Course2",
        code="22222",
        instructor="Instructor2",
        lectures=[
            Lesson(LessonTimes("11:00", "12:00", "1"), "L", "200", "201")
        ],
        exercises=[
            Lesson(LessonTimes("12:00", "13:00", "1"), "T", "200", "202"),
            Lesson(LessonTimes("13:00", "14:00", "1"), "T", "200", "203")
        ],
        labs=[]
    )

    schedules = service.generate_schedules([course1, course2])

    assert len(schedules) == 4

def test_schedule_conflicts():
    course1 = Course(
        name="Course1",
        code="11111",
        instructor="Instructor1",
        lectures=[
            Lesson(LessonTimes("10:00", "12:00", "1"), "L", "100", "101")
        ],
        exercises=[
            Lesson(LessonTimes("13:00", "14:00", "1"), "T", "100", "102")
        ],
        labs=[]
    )

    course2 = Course(
        name="Course2",
        code="22222",
        instructor="Instructor2",
        lectures=[
            Lesson(LessonTimes("11:00", "13:00", "1"), "L", "200", "201")
        ],
        exercises=[
            Lesson(LessonTimes("14:00", "15:00", "1"), "T", "200", "202")
        ],
        labs=[]
    )

    schedules = service.generate_schedules([course1, course2])
    assert len(schedules) == 0

def test_schedule_course_with_all_parts():
    course = Course(
        name="Course",
        code="11111",
        instructor="Instructor",
        lectures=[
            Lesson(LessonTimes("08:00", "09:00", "2"), "L", "A", "101")
        ],
        exercises=[
            Lesson(LessonTimes("09:00", "10:00", "2"), "T", "A", "102")
        ],
        labs=[
            Lesson(LessonTimes("10:00", "11:00", "2"), "M", "A", "103")
        ]
    )

    schedules = service.generate_schedules([course])
    assert len(schedules) == 1

def test_schedule_course_with_multiple_lecture_groups():
    course = Course(
        name="Course",
        code="11111",
        instructor="Instructor",
        lectures=[
            Lesson(LessonTimes("08:00", "09:00", "1"), "L", "C", "301"),
            Lesson(LessonTimes("09:00", "10:00", "1"), "L", "C", "302"),
            Lesson(LessonTimes("10:00", "11:00", "1"), "L", "C", "303")
        ],
        exercises=[
            Lesson(LessonTimes("11:00", "12:00", "1"), "T", "C", "303")
        ],
        labs=[]
    )

    schedules = service.generate_schedules([course])
    assert len(schedules) == 3

def test_schedule_lessons_on_different_days():
    course1 = Course(
        name="Course1",
        code="11111",
        instructor="Instructor1",
        lectures=[
            Lesson(LessonTimes("10:00", "11:00", "1"), "L", "A", "001")
        ],
        exercises=[
            Lesson(LessonTimes("11:00", "12:00", "1"), "T", "A", "002")
        ],
        labs=[]
    )

    course2 = Course(
        name="Course2",
        code="22222",
        instructor="Instructor2",
        lectures=[
            Lesson(LessonTimes("10:00", "11:00", "2"), "L", "B", "003")
        ],
        exercises=[
            Lesson(LessonTimes("11:00", "12:00", "2"), "T", "B", "004")
        ],
        labs=[]
    )

    schedules = service.generate_schedules([course1, course2])
    assert len(schedules) == 1

def test_schedule_not_consecutive_lessons():
    course = Course(
        name="Course",
        code="11111",
        instructor="Instructor",
        lectures=[
            Lesson(LessonTimes("09:00", "10:00", "3"), "L", "B1", "100")
        ],
        exercises=[
            Lesson(LessonTimes("14:00", "15:00", "3"), "T", "B1", "101")
        ],
        labs=[]
    )

    schedules = service.generate_schedules([course])
    assert len(schedules) == 1

def test_schedule_minimum_one_course():
    course = Course(
        name="Course",
        code="11111",
        instructor="Instructor",
        lectures=[
            Lesson(LessonTimes("08:00", "09:00", "1"), "L", "A", "001")
        ],
        exercises=[
            Lesson(LessonTimes("10:00", "11:00", "1"), "T", "A", "002")
        ],
        labs=[]
    )

    schedules = service.generate_schedules([course])
    assert len(schedules) == 1

def test_schedule_maximum_seven_courses():
    courses = []
    for i in range(7):
        course = Course(
            name=f"Course{i+1}",
            code=f"{i+1}{i+1}{i+1}{i+1}{i+1}",
            instructor=f"Instructor{i+1}",
            lectures=[
                Lesson(LessonTimes("08:00", "09:00", str(i + 1)), "L", f"B{i+1}", f"00{i+1}")
            ],
            exercises=[
                Lesson(LessonTimes("09:00", "10:00", str(i + 1)), "T", f"B{i+1}", f"01{i+1}")
            ],
            labs=[]
        )
        courses.append(course)

    schedules = service.generate_schedules(courses)
    assert len(schedules) > 0

def test_schedule_performance():
    courses = []
    for i in range(7):
        course = Course (
            name=f"Course{i+1}",
            code=f"{i+1}{i+1}{i+1}{i+1}{i+1}",
            instructor=f"Instructor{i+1}",
            lectures = [
                Lesson(LessonTimes("08:00", "09:00", str(i + 1)), "L", f"B{i}", f"{i}01"),
                Lesson(LessonTimes("10:00", "11:00", str(i + 1)), "L", f"B{i}", f"{i}02"),
            ],
            exercises = [
                Lesson(LessonTimes("12:00", "13:00", str(i + 1)), "T", f"B{i}", f"{i}03"),
                Lesson(LessonTimes("14:00", "15:00", str(i + 1)), "T", f"B{i}", f"{i}04"),
            ],
            labs=[]
        )
        courses.append(course)

    start_time = time.time()
    schedules = service.generate_schedules(courses)
    duration = time.time() - start_time

    assert duration < 10
    assert len(schedules) == 16384