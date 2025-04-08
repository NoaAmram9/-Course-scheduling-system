from SRC.Models.LessonTimes import LessonTimes
class Lesson:
    def __init__(self, time: LessonTimes = None, lesson_type: str = "", building: int = 0, room: int = 0):
        self._time = time if time else LessonTimes()  # lesson time (day, start time, end time)
        self._lesson_type = lesson_type  # lecture, exercise, lab
        self._building = building  # lesson building
        self._room = room  # lesson room

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

