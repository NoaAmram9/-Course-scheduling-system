from bisect import insort, bisect_left
from collections import defaultdict

class TimetablesSorter:
    """
    A class to sort timetables based on various metrics.
    It caches sorted lists to improve performance on repeated sort requests.
    This class allows sorting timetables by different keys and in both ascending and descending order.
    It also provides a method to add new timetables and update the sorted cache accordingly.
    """
    def __init__(self):
        self.sorted_schedules_cache = dict()  # key: (metric_key, ascending) -> sorted list
    
    def sort_timetables_by_key(self, all_schedules, key, ascending):
        """ 
        Sorts the provided list of timetables by a specified key and order.
        If the sorted list for the given key and order is already cached, it returns the cached list.
        
        :param all_schedules: List of timetable objects to be sorted.
        :param key: The attribute of the timetable metrics to sort by.
        :param ascending: Boolean indicating whether to sort in ascending order (True) or descending order (False).
        
        :return: A sorted list of timetables.
        """
        cache_key = (key, ascending)
        
        if cache_key in self.sorted_schedules_cache:
            sorted_schedules = self.sorted_schedules_cache[cache_key]
            # Check if the cached sorted list contains all schedules
            if len(sorted_schedules) == len(all_schedules):
                return sorted_schedules
        # If the cache is empty or does not contain the key, sort the schedules
        sorted_list = sorted(all_schedules, key=lambda t: getattr(t.metrics, key), reverse=not ascending)
        self.sorted_schedules_cache[cache_key] = sorted_list
        return sorted_list
    
    def add_timetables(self, timetable_batch):
        """
        Adds a new timetable batch to the sorter and updates the sorted cache.
        
        :param timetable_batch: The timetable_batch object to add.
        
        """
        for (key, ascending) in self.sorted_schedules_cache.keys():
            for timetable in timetable_batch:
                # Insert the timetable into the sorted cache for the given key and order
                if ascending:
                    # Use insort to maintain ascending order
                    insort(self.sorted_schedules_cache[(key, ascending)], timetable,
                           key=lambda t: getattr(t.metrics, key))
                else:
                    # Use a custom insort to maintain descending order
                    insort_descending(self.sorted_schedules_cache[(key, ascending)], timetable,
                                      key=lambda t: getattr(t.metrics, key))
        
def insort_descending(sorted_list, new_item, key=lambda item: item):
    """
    Inserts a new_item into sorted_list while maintaining descending order,
    using the given key function for comparison.

    :param sorted_list: List that is already sorted in descending order.
    :param new_item: The item to insert.
    :param key: A function that extracts a comparison key from each item.
                By default, the item itself is used.
    """

    # Extract the comparison key for the new item.
    new_key = key(new_item)

    # Build a list of keys for all items currently in the list.
    # Negate the keys to simulate descending order using bisect_left,
    # which only works with ascending sequences.
    keys = [-key(item) for item in sorted_list]

    # Find the position where the new item should be inserted
    # to maintain descending order.
    index = bisect_left(keys, -new_key)

    # Insert the new item into the correct position.
    sorted_list.insert(index, new_item)
