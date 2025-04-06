import pytest
from SRC.Services.ScheduleService import ScheduleService
from SRC.Models.Course import Course
from SRC.Models.Lesson import Lesson
from SRC.Models.LessonTimes import LessonTimes
import time

def test_generate_all_possible_schedules():
    service = ScheduleService()

    # First course: 2 lectures x 1 exercise
    course1 = Course(
        name="Course1",
        code="C1",
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

    # Second course: 1 lecture x 2 exercises
    course2 = Course(
        name="Course2",
        code="C2",
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

    # course1: 2 lectures x 1 exercise = 2 combinations
    # course2: 1 lecture x 2 exercises = 2 combinations
    # total valid combinations (if no conflicts): 2 x 2 = 4
    assert len(schedules) == 4, "Should generate all possible combinations for two courses without conflicts"

def test_detect_schedule_conflicts():
    service = ScheduleService()

    course1 = Course(
        name="Course1",
        code="C1",
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
        code="C2",
        instructor="Instructor2",
        lectures=[
            Lesson(LessonTimes("11:00", "13:00", "1"), "L", "200", "201")  # Conflict with course1's lecture
        ],
        exercises=[
            Lesson(LessonTimes("14:00", "15:00", "1"), "T", "200", "202")
        ],
        labs=[]
    )

    schedules = service.generate_schedules([course1, course2])
    assert len(schedules) == 0, "Should not generate schedules with conflicting lectures"

def test_schedule_course_with_all_components():
    service = ScheduleService()

    course = Course(
        name="FullCourse",
        code="FC1",
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
    assert len(schedules) == 1, "Should generate a schedule with all components (lecture, exercise, lab)"

def test_schedule_course_with_multiple_lecture_groups():
    service = ScheduleService()

    course = Course(
        name="MultiLecture",
        code="ML1",
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
    assert len(schedules) == 3, "Should create a schedule for each lecture group (with the same exercise)"

def test_lessons_on_different_days_do_not_conflict():
    service = ScheduleService()

    course1 = Course(
        name="Course1",
        code="C1",
        instructor="Inst1",
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
        code="C2",
        instructor="Inst2",
        lectures=[
            Lesson(LessonTimes("10:00", "11:00", "2"), "L", "B", "003")
        ],
        exercises=[
            Lesson(LessonTimes("11:00", "12:00", "2"), "T", "B", "004")
        ],
        labs=[]
    )

    schedules = service.generate_schedules([course1, course2])
    assert len(schedules) == 1, "Courses on different days should be allowed"

def test_non_consecutive_lessons_are_valid():
    service = ScheduleService()

    course = Course(
        name="CourseBreaks",
        code="CB1",
        instructor="Prof. Break",
        lectures=[
            Lesson(LessonTimes("09:00", "10:00", "3"), "L", "B1", "100")
        ],
        exercises=[
            Lesson(LessonTimes("14:00", "15:00", "3"), "T", "B1", "101")
        ],
        labs=[]
    )

    schedules = service.generate_schedules([course])
    assert len(schedules) == 1, "Should handle non-consecutive lessons with breaks"

def test_minimum_one_course_schedule():
    service = ScheduleService()

    course = Course(
        name="SoloCourse",
        code="SOLO1",
        instructor="Solo Teach",
        lectures=[
            Lesson(LessonTimes("08:00", "09:00", "1"), "L", "A", "001")
        ],
        exercises=[
            Lesson(LessonTimes("10:00", "11:00", "1"), "T", "A", "002")
        ],
        labs=[]
    )

    schedules = service.generate_schedules([course])
    assert len(schedules) == 1, "Should handle schedule with only one course"

def test_maximum_seven_courses_schedule():
    service = ScheduleService()

    courses = []
    for i in range(7):
        course = Course(
            name=f"Course{i+1}",
            code=f"C{i+1}",
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
    assert len(schedules) > 0, "Should generate valid schedules with 7 courses"

def test_schedule_generation_performance():
    service = ScheduleService()

    courses = []
    for i in range(7):
        lectures = [
            Lesson(LessonTimes("08:00", "09:00", str(i + 1)), "L", f"B{i}", f"{i}01"),
            Lesson(LessonTimes("10:00", "11:00", str(i + 1)), "L", f"B{i}", f"{i}02"),
        ]
        exercises = [
            Lesson(LessonTimes("12:00", "13:00", str(i + 1)), "T", f"B{i}", f"{i}03"),
            Lesson(LessonTimes("14:00", "15:00", str(i + 1)), "T", f"B{i}", f"{i}04"),
        ]
        course = Course(
            name=f"PerfCourse{i+1}",
            code=f"P{i+1}",
            instructor=f"Dr. Speed{i+1}",
            lectures=lectures,
            exercises=exercises,
            labs=[]
        )
        courses.append(course)

    # Time the schedule generation
    start_time = time.time()
    schedules = service.generate_schedules(courses)
    duration = time.time() - start_time

    assert duration < 10, f"Schedule generation took too long: {duration:.2f} seconds"
    assert len(schedules) > 0, "No schedules were generated, which is suspiciously fast 😅"