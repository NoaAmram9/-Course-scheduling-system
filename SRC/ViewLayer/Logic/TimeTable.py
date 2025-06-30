# # logic_timetable.py
# # This file contains the logic for mapping courses to time slots in a timetable.

# DAYS = ["Sunday" ,"Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday"]
# HOURS = list(range(8, 22))  # 8:00 to 21:00 (the range excluses the upper bound)

# def map_courses_to_slots(timetable):
#     """Maps each course to its time slots in the form {(day, hour): course}."""
#     slot_map = {} 
#     try: # the timetable is a Timetable object
#         courses = timetable.courses 
#     except: # the timetable is a list of courses
#         courses = timetable
    

#     for course in courses:
#         for lesson_type, lesson_list in [("Lecture", course.lectures),
#                                          ("Exercise", course.exercises),
#                                          ("Lab", course.labs),
#                                          ("Reinforcement", course.reinforcement),
#                                          ("DepartmentHour", course.departmentHours),
#                                          ("Training", course.training)]:
#             for lesson in lesson_list:
#                 day = DAYS[lesson.time.day - 1]  # Convert day index to string. lesson["day"] should be an index (numerical).
#                 start = int(lesson.time.start_hour)
#                 end = int(lesson.time.end_hour)
                
#                 # Fill in the slots for this lesson
#                 for hour in range(start, end):
#                     slot_map[(day, hour)] = {
#                         "name": course.name,
#                         "code": course.code,
#                         "type": lesson_type,
#                         #"instructor": course.instructor,
#                         "location": f"{lesson.building}-{lesson.room}" 
#                     }

#     return slot_map
# logic_timetable.py

from collections import defaultdict

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
HOURS = list(range(8, 22))  # 8:00 to 21:00


def map_courses_to_slots(data, course_lookup=None):
    """
    Maps each lesson to its time slots:
    - If data is a Timetable (has `.courses`), maps its courses.
    - If data is a list of (course_id, Lesson), maps those using course_lookup (dict: course_id -> course name/code).
    
    :param data: Timetable object or list of (course_id, Lesson)
    :param course_lookup: dict mapping course_id to Course (required if data is list of tuples)
    :return: dict of {(day, hour): lesson_info}
    """
    slot_map = {}

    # Determine input type
    if hasattr(data, "courses"):
        # Case 1: Timetable object with full course info
        for course in data.courses:
            for lesson_type, lessons in [
                ("Lecture", course.lectures),
                ("Exercise", course.exercises),
                ("Lab", course.labs),
                ("Reinforcement", course.reinforcement),
                ("DepartmentHour", course.departmentHours),
                ("Training", course.training)
            ]:
                for lesson in lessons:
                    _map_lesson(slot_map, course.name, course.code, lesson_type, lesson)
    else:
        # Case 2: List of (course_id, Lesson) tuples
        if course_lookup is None:
            raise ValueError("course_lookup dictionary is required when using (course_id, Lesson) list.")
        
        for course_id, lesson in data:
            course = course_lookup.get(course_id)
            if course:
                lesson_type = lesson.lesson_type
                _map_lesson(slot_map, course.name, course.code, lesson_type, lesson)

    return slot_map


def _map_lesson(slot_map, course_name, course_code, lesson_type, lesson):
    """
    Helper function to add a lesson to the slot map.
    """
    day_index = lesson.time.day
    if not (1 <= day_index <= 7):
        return  # skip invalid day

    day = DAYS[day_index - 1]
    start = lesson.time.start_hour
    end = lesson.time.end_hour

    for hour in range(start, end):
        slot_map[(day, hour)] = {
            "name": course_name,
            "code": course_code,
            "type": lesson_type,
            "location": f"{lesson.building}-{lesson.room}",
            "lesson": lesson
        }
