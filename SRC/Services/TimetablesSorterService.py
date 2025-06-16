import bisect
from collections import defaultdict

class TimetablesSorterService:
    def __init__(self):
        # List of all generated timetables, in the order they were created
        self.all_schedules = []

        # Cache for sorted lists of timetables
        # Key: (metric_key, reverse) tuple
        # Value: list of tuples (metric_value, timetable)
        self.sorted_cache = defaultdict(list)

    def add_timetable(self, timetable):
        """Called whenever a new timetable is generated"""
        self.all_schedules.append(timetable)

        # Update all existing sorted caches with the new timetable
        for (metric_key, reverse), sorted_list in self.sorted_cache.items():
            metric_value = getattr(timetable, metric_key)
            # Insert into the sorted list at the correct position using bisect
            bisect.insort(sorted_list, (metric_value, timetable))

    def get_sorted(self, metric_key, reverse=False):
        """
        Return timetables sorted by a given metric key.
        Uses cached results if available, otherwise computes and caches them.
        """
        cache_key = (metric_key, reverse)

        if cache_key not in self.sorted_cache:
            # First time sorting by this metric – build and cache the sorted list
            sorted_list = sorted(
                ((getattr(t, metric_key), t) for t in self.all_schedules),
                reverse=reverse
            )
            self.sorted_cache[cache_key] = sorted_list

        # Return only the timetables, without the metric values
        return [t for _, t in self.sorted_cache[cache_key]]

    def get_unsorted(self):
        """Return the unsorted list of timetables (by creation order)"""
        return self.all_schedules
