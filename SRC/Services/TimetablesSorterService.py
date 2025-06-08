from bisect import insort
from typing import Callable

class TimetablesSorterService:
    def __init__(self):
        self.all_schedules = []  # list of all timetables so far
        self.sorted_cache = {}   # cache for sorted lists by different keys
        self.sort_key_funcs = {  # keys for sorting and their corresponding functions
            "active_days": lambda t: t.active_days,
            "average_start_time": lambda t: t.average_start_time,
            "average_end_time": lambda t: t.average_end_time,
            "free_windows_sum": lambda t: t.free_windows_sum,
            "free_windows_number": lambda t: t.free_windows_number,
        }

    def add_timetable(self, timetable):
        """מוסיפה מערכת שעות לכל הרשימות הרלוונטיות"""
        self.all_schedules.append(timetable)

        for key, sorted_list in self.sorted_cache.items():
            key_func = self.sort_key_funcs[key]
            insort(sorted_list, timetable, key=key_func)

    def get_sorted(self, sort_key: str, reverse: bool = False):
        """מחזירה רשימה ממויינת לפי המפתח - ואם לא קיימת בקאש, יוצרת אותה"""
        if sort_key in self.sorted_cache:
            result = self.sorted_cache[sort_key]
        else:
            key_func = self.sort_key_funcs[sort_key]
            result = sorted(self.all_schedules, key=key_func)
            self.sorted_cache[sort_key] = result

        return list(reversed(result)) if reverse else result
