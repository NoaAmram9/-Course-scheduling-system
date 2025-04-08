class TimeTable:
    def __init__(self, courses: list = None):
        self._courses = courses if courses else []  # list of courses in the timetable

    @property
    def courses(self):
        return self._courses

    @courses.setter
    def courses(self, value):
        self._courses = value