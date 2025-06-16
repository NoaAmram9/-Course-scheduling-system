from SRC.Models.TimetableMetrics import TimetableMetrics

class TimeTable:
    def __init__(self, courses: list = None, metrics: TimetableMetrics = None):

        self._courses = courses if courses else []  # list of courses in the timetable
        self._metrics = None # TimetableMetrics object to hold metrics

    @property
    def courses(self):
        return self._courses

    @courses.setter
    def courses(self, value):
        self._courses = value

        
    @property
    def metrics(self):
        return self._metrics
    
    @metrics.setter
    def metrics(self, value: TimetableMetrics):
        self._metrics = value
    
    @property
    def get_lesson_times(self):
        """returns a list of all lesson times in the timetable"""
        times = []
        for course in self.courses:
            # if course has lectures
            if hasattr(course, '_lectures') and course._lectures:
                for lesson in course._lectures:
                    if hasattr(lesson, '_time'):
                        times.append(lesson._time)
            #if course has exercises
            if hasattr(course, '_exercises') and course._exercises:
                for lesson in course._exercises:
                    if hasattr(lesson, '_time'):
                        times.append(lesson._time)
            # if course has labs
            if hasattr(course, '_labs') and course._labs:
                for lesson in course._labs:
                    if hasattr(lesson, '_time'):
                        times.append(lesson._time)
            # if course has _departmentHours
            if hasattr(course, '_departmentHours') and course._departmentHours:
                for lesson in course._departmentHours:
                    if hasattr(lesson, '_time'):
                        times.append(lesson._time)
            # if course has reinforcement lessons
            if hasattr(course, '_reinforcement') and course._reinforcement:
                for lesson in course._reinforcement:
                    if hasattr(lesson, '_time'):
                        times.append(lesson._time)
            # if course has training lessons
            if hasattr(course, '_training') and course._training:
                for lesson in course._training:
                    if hasattr(lesson, '_time'):
                        times.append(lesson._time)
            
        return times