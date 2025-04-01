class LessonTimes:
    def __init__(self, start_hour: int = 0, end_hour: int = 0, day: int = 0):
        self._start_hour = start_hour  # שעת התחלה
        self._end_hour = end_hour  # שעת סיום
        self._day = day  # יום בשבוע (0=ראשון, 6=שבת)

    @property
    def start_hour(self):
        return self._start_hour

    @start_hour.setter
    def start_hour(self, value):
        self._start_hour = value

    @property
    def end_hour(self):
        return self._end_hour

    @end_hour.setter
    def end_hour(self, value):
        self._end_hour = value

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):
        self._day = value