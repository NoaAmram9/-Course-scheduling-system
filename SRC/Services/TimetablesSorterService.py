from bisect import insort
from typing import Callable

class TimetablesSorterService:
    def __init__(self):
        self.all_schedules = [] 
        self.sorted_cache = {}   # cache for sorted lists by different keys
        self.sort_key_funcs = {  # keys for sorting and their corresponding functions
            "active_days": lambda t: t.active_days,
            "average_start_time": lambda t: t.average_start_time,
            "average_end_time": lambda t: t.average_end_time,
            "free_windows_sum": lambda t: t.free_windows_sum,
            "free_windows_number": lambda t: t.free_windows_number,
        }

import bisect
from collections import defaultdict

class TimetablesSorterService:
    def __init__(self):
        # רשימת כל מערכות השעות שנוצרו, לפי סדר הוספה
        self.all_schedules = []  # list of all timetables so far

        # cache של מיונים:
        # key: (metric_key, reverse)
        # value: list of (metric_value, timetable)
        self.sorted_cache = defaultdict(list) # cache for sorted lists by different keys

    def add_timetable(self, timetable):
        """נקראת כאשר נוצרת מערכת שעות חדשה"""
        self.all_schedules.append(timetable)

        # עדכון כל המיונים שכבר קיימים בקאש
        for (metric_key, reverse), sorted_list in self.sorted_cache.items():
            metric_value = getattr(timetable, metric_key)
            # שימוש ב-bisect כדי להכניס את המערכת למיקום הנכון
            bisect.insort(sorted_list, (metric_value, timetable))

    def get_sorted(self, metric_key, reverse=False):
        """החזרת מערכות ממויינות לפי מפתח מיון מסוים"""
        cache_key = (metric_key, reverse)

        if cache_key not in self.sorted_cache:
            # יצירת רשימה ממויינת בפעם הראשונה
            sorted_list = sorted(
                ((getattr(t, metric_key), t) for t in self.all_schedules),
                reverse=reverse
            )
            self.sorted_cache[cache_key] = sorted_list

        # החזרת רק הרשימה של האובייקטים עצמם (בלי הערך)
        return [t for _, t in self.sorted_cache[cache_key]]

    def get_unsorted(self):
        """מחזיר את הרשימה הלא ממויינת (לפי סדר יצירה)"""
        return self.all_schedules
