def sort_timetables(timetables, key, ascending):
    """
    Sorts a list of timetables based on a specified key and order.

    :param timetables: List of timetable dictionaries to sort.
    :param key: The key to sort by, e.g., "name", "type", "modified".
    :param ascending: If True, sorts in ascending order; if False, sorts in descending order.
    :return: Sorted list of timetables.
    """
    timetables.sort(key=lambda timetable: getattr(timetable.preferences_details, key), reverse=not ascending)
    print(f"Sorted timetables by {key} in {'ascending' if ascending else 'descending'} order.")
    
    for timetable in timetables:
        print(f"Days: {timetable.preferences_details.days}, Free Windows: {timetable.preferences_details.free_windows_number}")