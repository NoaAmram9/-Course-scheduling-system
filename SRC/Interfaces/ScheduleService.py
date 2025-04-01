from itertools import product
from SRC.Interfaces.IScheduleService import IScheduleService
from SRC.Models.TimeTable import TimeTable


class ScheduleService(IScheduleService):
    def generate_schedules(self, courses: list) -> list:
        possible_timetables = []
        
        # רשימת כל הקומבינציות האפשריות של שיעורים לכל קורס (הרצאה אחת, תרגול אחד, מעבדה אחת)
        course_combinations = []
        for course in courses:
            options = []
            
            # בחירת אפשרויות להרצאה, תרגול ומעבדה
            lectures = course._lectures if course._lectures else [None]
            exercises = course._exercises if course._exercises else [None]
            labs = course._labs if course._labs else [None]
            
            # כל שילוב אפשרי של הרצאה אחת, תרגול אחד ומעבדה אחת
            course_combinations.append(list(product(lectures, exercises, labs)))
        
        # יוצרים את כל הקומבינציות האפשריות של מערכות שעות
        for combination in product(*course_combinations):
            timetable_lessons = [lesson for course_lessons in combination for lesson in course_lessons if lesson is not None]
            
            if self._is_valid_timetable(timetable_lessons):
                possible_timetables.append(TimeTable(timetable_lessons))
        
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
