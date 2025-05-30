# from itertools import product
# from SRC.Interfaces.IScheduleService import IScheduleService
# from SRC.Models.TimeTable import TimeTable
# from SRC.Models.Course import Course

# class ScheduleService(IScheduleService):
#     def generate_schedules(self, courses: list) -> list:
        
#         possible_timetables = []
        
#         # alright so for each course, we wanna figure out all the different combos
#         # of one lecture, one exercise, and one lab (if they exist)
#         course_combinations = []
#         for course in courses:
#             lectures = course._lectures if course._lectures else [None]
#             exercises = course._exercises if course._exercises else [None]
#             labs = course._labs if course._labs else [None]
            
#             # build every possible combo for this one course
#             course_combinations.append([
#                 (course._name, course._code, course.instructor, lec, ex, lab)
#                 for lec, ex, lab in product(lectures, exercises, labs)
#             ])
        
#         # now let’s build every possible full timetable using one combo per course
#         for combination in product(*course_combinations):
#             timetable_courses = []
#             timetable_lessons = []
            
#             for course_name, course_code, course_instructor, lec, ex, lab in combination:
#                 # grab only the stuff that actually exists (not None)
#                 selected_lessons = [lesson for lesson in (lec, ex, lab) if lesson is not None]
#                 timetable_lessons.extend(selected_lessons)
                
#                 # recreate the course object with just the selected lessons
#                 timetable_courses.append(
#                     Course(
#                         name=course_name,
#                         code=course_code,
#                         instructor=course_instructor,
#                         lectures=[lec] if lec else [],
#                         exercises=[ex] if ex else [],
#                         labs=[lab] if lab else []
#                     )
#                 )
            
#             # only keep the timetable if there’s no lesson overlap
#             if self._is_valid_timetable(timetable_lessons):
#                 possible_timetables.append(TimeTable(timetable_courses))
        
#         return possible_timetables

#     def _is_valid_timetable(self, lessons: list) -> bool:
#         # check if any lessons are stepping on each other’s toes
#         for i, lesson1 in enumerate(lessons):
#             for lesson2 in lessons[i+1:]:
#                 if self._is_conflicting(lesson1, lesson2):
#                     return False
#         return True
    
#     def _is_conflicting(self, lesson1, lesson2) -> bool:
#         # basic check – if they're not even on the same day, we're chill
#         if lesson1._time._day != lesson2._time._day:
#             return False
#         # if one ends before the other starts, also chill – otherwise, boom, conflict
#         return not (
#             lesson1._time._end_hour <= lesson2._time._start_hour or
#             lesson2._time._end_hour <= lesson1._time._start_hour
#         )

#####################################

#seconde try

####################################33
# """faster Algorithm for generating schedules"""
# from itertools import product
# from collections import defaultdict
# from SRC.Interfaces.IScheduleService import IScheduleService
# from SRC.Models.TimeTable import TimeTable
# from SRC.Models.Course import Course
# from itertools import product
# from SRC.Interfaces.IScheduleService import IScheduleService
# from SRC.Models.TimeTable import TimeTable
# from SRC.Models.Course import Course

# class ScheduleService(IScheduleService):
#     def generate_schedules(self, courses: list) -> list:
        
#         possible_timetables = []
        
#         # alright so for each course, we wanna figure out all the different combos
#         # of one lecture, one exercise, and one lab (if they exist)
#         course_combinations = []
#         for course in courses:
#             lectures = course._lectures if course._lectures else [None]
#             exercises = course._exercises if course._exercises else [None]
#             labs = course._labs if course._labs else [None]
            
#             # build every possible combo for this one course
#             course_combinations.append([
#                 (course._name, course._code, course.instructor, lec, ex, lab)
#                 for lec, ex, lab in product(lectures, exercises, labs)
#             ])
        
#         # now let’s build every possible full timetable using one combo per course
#         for combination in product(*course_combinations):
#             timetable_courses = []
#             timetable_lessons = []
            
#             for course_name, course_code, course_instructor, lec, ex, lab in combination:
#                 # grab only the stuff that actually exists (not None)
#                 selected_lessons = [lesson for lesson in (lec, ex, lab) if lesson is not None]
#                 timetable_lessons.extend(selected_lessons)
                
#                 # recreate the course object with just the selected lessons
#                 timetable_courses.append(
#                     Course(
#                         name=course_name,
#                         code=course_code,
#                         instructor=course_instructor,
#                         lectures=[lec] if lec else [],
#                         exercises=[ex] if ex else [],
#                         labs=[lab] if lab else []
#                     )
#                 )
            
#             # only keep the timetable if there’s no lesson overlap
#             if self._is_valid_timetable(timetable_lessons):
#                 possible_timetables.append(TimeTable(timetable_courses))
        
#         return possible_timetables

#     def _is_valid_timetable(self, lessons: list) -> bool:
#         # check if any lessons are stepping on each other’s toes
#         for i, lesson1 in enumerate(lessons):
#             for lesson2 in lessons[i+1:]:
#                 if self._is_conflicting(lesson1, lesson2):
#                     return False
#         return True
    
#     def _is_conflicting(self, lesson1, lesson2) -> bool:
#         # basic check – if they're not even on the same day, we're chill
#         if lesson1._time._day != lesson2._time._day:
#             return False
#         # if one ends before the other starts, also chill – otherwise, boom, conflict
#         return not (
#             lesson1._time._end_hour <= lesson2._time._start_hour or
#             lesson2._time._end_hour <= lesson1._time._start_hour
#         )


########################3
# third try
#########################



from itertools import product
from SRC.Interfaces.IScheduleService import IScheduleService
from SRC.Models.TimeTable import TimeTable
from SRC.Models.Course import Course

class ScheduleService(IScheduleService):
    def generate_schedules(self, courses: list) -> list:
        possible_timetables = []

        # For each course, get all valid combinations of its components
        course_combinations = []
        for course in courses:
            # Prepare all lesson types, defaulting to [None] if empty
            lectures = course._lectures if course._lectures else [None]
            exercises = course._exercises if course._exercises else [None]
            labs = course._labs if course._labs else [None]
            departmentHours = course._departmentHours if hasattr(course, "_departmentHours") and course._departmentHours else [None]
            reinforcement = course._reinforcement if hasattr(course, "_reinforcement") and course._reinforcement else [None]
            training = course._training if hasattr(course, "_training") and course._training else [None]

            # Cartesian product of all combinations
            course_combinations.append([
                (
                    course._name,
                    course._code,
                    #course._instructor,
                    lec, ex, lab,
                    dept, reinf, train
                )
                for lec, ex, lab, dept, reinf, train in product(
                    lectures, exercises, labs,
                    departmentHours, reinforcement, training
                )
            ])

        # Build complete timetable combinations
        for combination in product(*course_combinations):
            timetable_courses = []
            timetable_lessons = []

            for (name, code, #instructor,
                 lec, ex, lab,
                 dept, reinf, train) in combination:

                selected_lessons = [
                    lesson for lesson in (lec, ex, lab, dept, reinf, train)
                    if lesson is not None
                ]
                timetable_lessons.extend(selected_lessons)

                timetable_courses.append(
                    Course(
                        name=name,
                        code=code,
                        #instructor=instructor,
                        lectures=[lec] if lec else [],
                        exercises=[ex] if ex else [],
                        labs=[lab] if lab else [],
                        departmentHours=[dept] if dept else [],
                        reinforcement=[reinf] if reinf else [],
                        training=[train] if train else []
                    )
                )

            if self._is_valid_timetable(timetable_lessons):
                possible_timetables.append(TimeTable(timetable_courses))

        return possible_timetables

    def _is_valid_timetable(self, lessons: list) -> bool:
        for i, lesson1 in enumerate(lessons):
            for lesson2 in lessons[i+1:]:
                if self._is_conflicting(lesson1, lesson2):
                    return False
        return True

    def _is_conflicting(self, lesson1, lesson2) -> bool:
        if lesson1._time._day != lesson2._time._day:
            return False
        return not (
            lesson1._time._end_hour <= lesson2._time._start_hour or
            lesson2._time._end_hour <= lesson1._time._start_hour
        )
