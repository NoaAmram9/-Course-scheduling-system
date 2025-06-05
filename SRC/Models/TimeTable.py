from SRC.Models.Preferences import Preferences

class TimeTable:
    def __init__(self, courses: list = None, preferences_details: Preferences = None):

        self._courses = courses if courses else []  # list of courses in the timetable
        self._preferences_details = None # Preferences object to hold details for user's displaying preferences

    @property
    def courses(self):
        return self._courses

    @courses.setter
    def courses(self, value):
        self._courses = value

        
    @property
    def preferences_details(self):
        return self._preferences_details
    
    @preferences_details.setter
    def preferences_details(self, value: Preferences):
        self._preferences_details = value
    
    @property
    def get_lesson_times(self):
        """מחזיר את כל זמני השיעורים מכל הקורסים"""
        times = []
        for course in self.courses:
            # אם יש lectures
            if hasattr(course, '_lectures') and course._lectures:
                for lesson in course._lectures:
                    if hasattr(lesson, '_time'):
                        times.append(lesson._time)
            # אם יש exercises
            if hasattr(course, '_exercises') and course._exercises:
                for lesson in course._exercises:
                    if hasattr(lesson, '_time'):
                        times.append(lesson._time)
            # אם יש labs
            if hasattr(course, '_labs') and course._labs:
                for lesson in course._labs:
                    if hasattr(lesson, '_time'):
                        times.append(lesson._time)
            # וכן הלאה עבור departmentHours, reinforcement, training...
            # אם יש departmentHours
            if hasattr(course, '_departmentHours') and course._departmentHours:
                for lesson in course._departmentHours:
                    if hasattr(lesson, '_time'):
                        times.append(lesson._time)
                        
            # אם יש reinforcement
            if hasattr(course, '_reinforcement') and course._reinforcement:
                for lesson in course._reinforcement:
                    if hasattr(lesson, '_time'):
                        times.append(lesson._time)
            
            # אם יש training
            if hasattr(course, '_training') and course._training:
                for lesson in course._training:
                    if hasattr(lesson, '_time'):
                        times.append(lesson._time)
            
        return times

