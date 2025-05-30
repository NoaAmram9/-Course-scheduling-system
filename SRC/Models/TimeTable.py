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