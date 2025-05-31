from SRC.Models.Preferences import Preferences
class TimeTable:
    def __init__(self, courses: list = None,preferences: Preferences = None):
        self._preferences = preferences if preferences else Preferences()
        self._courses = courses if courses else []  # list of courses in the timetable

    @property
    def courses(self):
        return self._courses

    @courses.setter
    def courses(self, value):
        self._courses = value
    

   
    