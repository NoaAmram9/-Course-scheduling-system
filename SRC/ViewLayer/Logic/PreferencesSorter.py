def sort_timetables(timetables, key, ascending):
    """
    Sorts a list of timetables based on a specified key and order.

    :param timetables: List of timetable dictionaries to sort.
    :param key: The key to sort by, e.g., "days", "free windows".
    :param ascending: If True, sorts in ascending order; if False, sorts in descending order.
    
    :return: None. Modifies the input list of timetables in-place, sorting them by the given preference key and order.
    """
    timetables.sort(key=lambda timetable: getattr(timetable.preferences_details, key), reverse=not ascending)
    # print(f"Sorted timetables by {key} in {'ascending' if ascending else 'descending'} order.")
    