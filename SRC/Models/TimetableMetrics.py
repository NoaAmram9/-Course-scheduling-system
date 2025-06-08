class TimetableMetrics:
    """
    This class represents metrics for user preferences in schedule display.

    Users can choose to display schedules based on:
    - Active study days (1-7)
    - Number of free windows (0-98)
    - Total hours of all free windows (0-98)
    - Average start time of the schedule
    - Average end time of the schedule
    """
    def __init__(self, active_days: int = 0,
                 free_windows_number: int = 0,
                 free_windows_sum: int = 0,
                 average_start_time: float = 0, 
                 average_end_time: float = 0):
        self._active_days = active_days # number of active days in the schedule (1-7)
        self._free_windows_number = free_windows_number # number of free windows in the schedule (0-98)
        self._free_windows_sum = free_windows_sum # sum of all free windows in the schedule (0-98)
        self._average_start_time = average_start_time # average start time of the schedule 
        self._average_end_time = average_end_time # average end time of the schedule

    @property
    def active_days(self):
        return self._active_days
    @property
    def free_windows_number(self):
        return self._free_windows_number
    @property
    def free_windows_sum(self):
        return self._free_windows_sum
    @property
    def average_start_time(self):
        return self._average_start_time
    @property
    def average_end_time(self):
        return self._average_end_time