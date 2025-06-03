from SRC.Models.LessonTimes import LessonTimes
class Lesson:
    def __init__(self, time: LessonTimes = None, lesson_type: str = "", building: int = 0, room: int = 0, instructors: list = None, creditPoints: int = 0, weeklyHours: float = 0.0, groupCode: int = 0):
        self._time = time if time else LessonTimes()  # lesson time (day, start time, end time)
        self._lesson_type = lesson_type  # lecture, exercise, lab
        self._building = building  # lesson building
        self._room = room  # lesson room
        self._instructors = instructors if instructors else []
        self._creditPoints = creditPoints
        self._weeklyHours = weeklyHours
        self._groupCode = groupCode
    
    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def lesson_type(self):
        return self._lesson_type

    @lesson_type.setter
    def lesson_type(self, value):
        self._lesson_type = value

    @property
    def building(self):
        return self._building

    @building.setter
    def building(self, value):
        self._building = value

    @property
    def room(self):
        return self._room

    @room.setter
    def room(self, value):
        self._room = value

    @property
    def instructors(self):
        return self._instructors

    @instructors.setter
    def instructors(self, value):
        self._instructors = value

    @property
    def creditPoints(self):
        return self._creditPoints

    @creditPoints.setter
    def creditPoints(self, value):
        self._creditPoints = value

    @property
    def weeklyHours(self):
        return self._weeklyHours

    @weeklyHours.setter
    def weeklyHours(self, value):
        self._weeklyHours = value

    @property
    def groupCode(self):
        return self._groupCode

    @groupCode.setter
    def groupCode(self, value):
        self._groupCode = value

