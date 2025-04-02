from itertools import product
from SRC.Interfaces.IScheduleService import IScheduleService
from SRC.Models.TimeTable import TimeTable
from SRC.Models.Course import Course

class ScheduleService(IScheduleService):
    def generate_schedules(self, courses: list) -> list:
        possible_timetables = []
        
        # רשימת כל הקומבינציות האפשריות של שיעורים לכל קורס (הרצאה אחת, תרגול אחד, מעבדה אחת)
        course_combinations = []
        for course in courses:
            lectures = course._lectures if course._lectures else [None]
            exercises = course._exercises if course._exercises else [None]
            labs = course._labs if course._labs else [None]
            
            # כל שילוב אפשרי של הרצאה אחת, תרגול אחד ומעבדה אחת לקורס מסוים
            course_combinations.append([(course._name, course._code, lec, ex, lab) for lec, ex, lab in product(lectures, exercises, labs)])
        
        # יוצרים את כל הקומבינציות האפשריות של מערכות שעות
        for combination in product(*course_combinations):
            timetable_courses = []
            timetable_lessons = []
            
            for course_name, course_code, lec, ex, lab in combination:
                selected_lessons = [lesson for lesson in (lec, ex, lab) if lesson is not None]
                timetable_lessons.extend(selected_lessons)
                timetable_courses.append(Course(name=course_name, code=course_code, lectures=[lec] if lec else [], exercises=[ex] if ex else [], labs=[lab] if lab else []))
                
            if self._is_valid_timetable(timetable_lessons):
                possible_timetables.append(TimeTable(timetable_courses))
        
        return possible_timetables

    def _is_valid_timetable(self, lessons: list) -> bool:
        """
        בודקת אם אין התנגשויות במערכת השעות.
        """
        for i, lesson1 in enumerate(lessons):
            for lesson2 in lessons[i+1:]:
                if self._is_conflicting(lesson1, lesson2):
                    return False
        return True
    
    def _is_conflicting(self, lesson1, lesson2) -> bool:
        """
        בודקת האם שני שיעורים מתנגשים בזמנים.
        """
        if lesson1._time._day != lesson2._time._day:
            return False
        return not (lesson1._time._end_hour <= lesson2._time._start_hour or lesson2._time._end_hour <= lesson1._time._start_hour)
