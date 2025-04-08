class LessonTimes:
    def __init__(self, start_hour: int = 0, end_hour: int = 0, day: int = 0):
        self._start_hour = start_hour  # start hour (0-23)
        self._end_hour = end_hour  # end hour (0-23)
        self._day = day  # day of the week (0-6, where 0 is Sunday and 6 is Saturday)

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