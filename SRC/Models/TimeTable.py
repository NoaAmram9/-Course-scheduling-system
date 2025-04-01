class Timetable:
    def __init__(self, courses: list = None):
        self._courses = courses if courses else []  # רשימה של קורסים במערכת השעות

    @property
    def courses(self):
        return self._courses

    @courses.setter
    def courses(self, value):
        self._courses = value