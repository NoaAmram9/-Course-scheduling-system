class Preferences:
    """
    Class representing user preferences for a schedules displaying.
    
    The user can choose to display scheduels by:
    - active study days (1-7)
    - number of free windows (0-98)
    - sum of hours of all free windows (0-98)
    - avarage start time of the schedule
    - avarage end time of the schedule
    """
    def __init__(self, days: int = 0,
                 free_windows_number: int = 0,
                 free_windows_sum: int = 0,
                 avarage_start_time: float = 0, 
                 avarage_end_time: float = 0):
        self._days = days # number of active days in the schedule (1-7)
        self._free_windows_number = free_windows_number # number of free windows in the schedule (0-98)
        self._free_windows_sum = free_windows_sum # sum of all free windows in the schedule (0-98)
        self._avarage_start_time = avarage_start_time # avarage start time of the schedule 
        self._avarage_end_time = avarage_end_time # avarage end time of the schedule

    @property
    def days(self):
        return self._days
    @property
    def free_windows_number(self):
        return self._free_windows_number
    @property
    def free_windows_sum(self):
        return self._free_windows_sum
    @property
    def avarage_start_time(self):
        return self._avarage_start_time
    @property
    def avarage_end_time(self):
        return self._avarage_end_time