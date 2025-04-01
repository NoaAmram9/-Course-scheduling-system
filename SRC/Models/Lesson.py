import LessonTimes
class Lesson:
    def __init__(self, professor: str = "", time: LessonTimes = None, lesson_type: str = "", building: int = 0, room: int = 0):
        self._professor = professor  # שם המרצה
        self._time = time if time else LessonTimes()  # הזמן של השיעור
        self._lesson_type = lesson_type  # סוג השיעור (הרצאה, תרגול, מעבדה)
        self._building = building  # מיקום השיעור
        self._room = room  # חדר השיעור

    @property
    def professor(self):
        return self._professor

    @professor.setter
    def professor(self, value):
        self._professor = value

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

