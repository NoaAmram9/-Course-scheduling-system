# logic_timetable.py
# This file contains the logic for mapping courses to time slots in a timetable.

DAYS = ["Sunday" ,"Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday"]
HOURS = list(range(8, 22))  # 8:00 to 21:00 (the range excluses the upper bound)

def map_courses_to_slots(timetable):
    """Maps each course to its time slots in the form {(day, hour): course}."""
    slot_map = {} 
    courses = timetable.courses 

    for course in courses:
        for lesson_type, lesson_list in [("Lecture", course.lectures),
                                         ("Exercise", course.exercises),
                                         ("Lab", course.labs),
                                         ("Reinforcement", course.reinforcement),
                                         ("DepartmentHour", course.departmentHours),
                                         ("Training", course.training)]:
            for lesson in lesson_list:
                day = DAYS[lesson.time.day - 1]  # Convert day index to string. lesson["day"] should be an index (numerical).
                start = int(lesson.time.start_hour)
                end = int(lesson.time.end_hour)
                
                # Fill in the slots for this lesson
                for hour in range(start, end):
                    slot_map[(day, hour)] = {
                        "name": course.name,
                        "code": course.code,
                        "type": lesson_type,
                        #"instructor": course.instructor,
                        "location": f"{lesson.building}-{lesson.room}" 
                    }

    return slot_map