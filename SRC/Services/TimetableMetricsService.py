from SRC.Models.TimetableMetrics import TimetableMetrics
from SRC.Models.TimeTable import TimeTable
from SRC.Models.LessonTimes import LessonTimes

from collections import defaultdict

class TimetableMetricsService:
    def __init__(self):
        timetable = None
 
    # Method to apply user preferences details to the timetable.
    def generate_metrics(self, timetable):
        """
        Apply user preferences details to the timetable.
        
        Args:
            timetable (TimeTable): The timetable to which preferences details will be applied.
            If the timetable empty or has no courses, the method will return without applying preferences.
        Returns:
            None: This method does not return anything, it updates the timetable's preferences details.
        """
        self.timetable = timetable # set the current timetable to calculate preferences on
        lesson_times = self.get_lesson_times()  # Get the lesson times from the timetable
        
        # Calculate various preferences based on the timetable
        active_days = self.calculate_active_days(lesson_times=lesson_times)
        free_windows_num, free_windows_sum = self.calculate_free_windows(lesson_times=lesson_times)
        avg_start_time, avg_end_time = self.calculate_avg_times(lesson_times=lesson_times)
        
        # Create the preferences details & update in the timetable
        metrics = TimetableMetrics(
            active_days=active_days,
            free_windows_number=free_windows_num,
            free_windows_sum=free_windows_sum,
            average_start_time=avg_start_time,
            average_end_time=avg_end_time
        )
        
        self.timetable.metrics = metrics
        # print(f"applied preferences: {self.timetable._metrics.active_days} active days, "
        #       f"{self.timetable._metrics.free_windows_number} free windows, "
        #       f"avg start time: {self.timetable._metrics.average_start_time}, "
        #       f"avg end time: {self.timetable._metrics.average_end_time}")
 
    # Method to get the lesson times from the timetable.
    def get_lesson_times(self):
        """ 
        Get the lesson times from the timetable.
        
        Returns:
            defaultdict: A dictionary where keys are (active) days of the week,
                and values are lists of LessonTimes objects for that day, sorted by start hour.
            
        """
        if not self.timetable or not self.timetable.courses:
            return []
        # Collect all lesson times from the timetable's courses
        lesson_times = []
        for course in self.timetable.courses:
            if course.code.startswith("BLOCKED"):
                continue  # Skip dummy time constraints
            
            for lesson_list in [course.lectures, course.exercises, course.labs, course.departmentHours,
                                course.reinforcement, course.training]:
                if not lesson_list:
                    continue
                for lesson in lesson_list:
                    lesson_times.append(lesson.time)
        
        # Group lesson times by day
        lessons_by_day = defaultdict(list)
        for lesson_time in lesson_times:
            lessons_by_day[lesson_time.day].append(lesson_time)
        # Sort lessons by start hour for each day
        for day, lessons in lessons_by_day.items():
            lessons.sort(key=lambda lt: self.extract_hour(lt.start_hour))
        
        return lessons_by_day
    
    # Method to calculate the number of active days in the timetable.       
    def calculate_active_days(self, lesson_times=None):
        """
        Calculate the number of active days in the timetable.
        Args:
            lesson_times (dict): Dictionary of lesson lists grouped by day.
            
        Returns:
            int: The number of active days.
        """
     
    
        return  len(lesson_times) if lesson_times else 0
       
        
    
    # Method to calculate the number and total duration of free windows in the timetable.       
    def calculate_free_windows(self, lesson_times=None):
        """ 
        Calculate the number and total duration of free windows (gaps) between lessons in a day.

        note: A free window is defined as a continuous period of more than half an hour
                in which there is no course but there are courses before and after it on the same day.
        Args:
            lesson_times (dict): Dictionary of lesson lists grouped by day, sorted by start hour.

        Returns:
            tuple: (free_windows, total_free_hours)
        """
        free_windows = 0
        total_free_hours = 0
        for lessons in lesson_times.values():
            # Check for gaps between lessons
            for i in range(len(lessons) - 1):
                current_end = self.extract_hour(lessons[i].end_hour)
                next_start = self.extract_hour(lessons[i + 1].start_hour)
                
                gap = next_start - current_end
                if gap > 0:
                    free_windows += 1
                    total_free_hours += gap
              
        
        return free_windows, total_free_hours
    
    ####DEBUGGING METHODS - Uncomment to use for debugging purposes#####
    # def calculate_avg_times(self, lesson_times=None):
    #     """
    #     Calculate the average start and end times of lessons in the timetable.
    #     Args:
    #         lesson_times (dict): Dictionary of lesson lists grouped by day.

    #     Returns:
    #         tuple: (avg_start, avg_end) where:
    #     """   
    #     print(f"DEBUG: Starting calculate_avg_times")
    #     print(f"DEBUG: lesson_times = {lesson_times}")
        
    #     total_start = 0
    #     total_end = 0
    #     total_days = self.calculate_active_days(lesson_times=lesson_times)
        
    #     print(f"DEBUG: total_days = {total_days}")
        
    #     # Check if we have any active days
    #     if total_days == 0:
    #         print("DEBUG: No active days found - returning default values")
    #         return 0, 0  # או ערכים default אחרים שמתאימים לך
        
    #     # Check if lesson_times is empty or None
    #     if not lesson_times:
    #         print("DEBUG: lesson_times is empty or None")
    #         return 0, 0
        
    #     # for each day, add the start and end times of lessons to the totals
    #     for day, daily_lessons in lesson_times.items():
    #         print(f"DEBUG: Processing day {day} with {len(daily_lessons)} lessons")
            
    #         if not daily_lessons:  # אם אין שיעורים ביום הזה
    #             print(f"DEBUG: No lessons for day {day}")
    #             continue
                
    #         last_lesson_index = len(daily_lessons) - 1
            
    #         # בדיקה נוספת שהשיעור הראשון והאחרון קיימים
    #         if daily_lessons[0] is None or daily_lessons[last_lesson_index] is None:
    #             print(f"DEBUG: Invalid lesson found on day {day}")
    #             continue
                
    #         start_hour = self.extract_hour(daily_lessons[0].start_hour)
    #         end_hour = self.extract_hour(daily_lessons[last_lesson_index].end_hour)
            
    #         print(f"DEBUG: Day {day} - start: {start_hour}, end: {end_hour}")
            
    #         total_start += start_hour
    #         total_end += end_hour
        
    #     print(f"DEBUG: total_start = {total_start}, total_end = {total_end}, total_days = {total_days}")
        
    #     # Calculate the average start and end times - with zero division protection
    #     if total_days > 0:
    #         avg_start = total_start / total_days
    #         avg_end = total_end / total_days
    #         print(f"DEBUG: avg_start = {avg_start}, avg_end = {avg_end}")
    #     else:
    #         print("DEBUG: total_days is 0 - cannot calculate average")
    #         avg_start = 0
    #         avg_end = 0
        
    #     return avg_start, avg_end
    
    # Method to calculate the average start and end times in the timetable.       
    def calculate_avg_times(self, lesson_times=None):
        """
        Calculate the average start and end times of lessons in the timetable.
        Args:
            lesson_times (dict): Dictionary of lesson lists grouped by day.

        Returns:
            tuple: (avg_start, avg_end) where:
        """   
        total_start = 0
        total_end = 0
        total_days = self.calculate_active_days(lesson_times=lesson_times)
        
        # for each day, add the start and end times of lessons to the totals
        for daily_lessons in lesson_times.values():
            last_lesson_index = len(daily_lessons) - 1
            total_start += self.extract_hour(daily_lessons[0].start_hour) 
            total_end += self.extract_hour(daily_lessons[last_lesson_index].end_hour)
        # Calculate the average start and end times
        avg_start = total_start / total_days
        avg_end = total_end / total_days
        
        return avg_start, avg_end
    
    # Method to extract the hour from a time string in HH:MM format.
    def extract_hour(self, time_val: str) -> int:
        """
        Extract the hour component from a time value that may be a string in HH:MM format or an integer.

        Args:
            time_val (str | int): A time string (e.g., "09:30") or already an integer hour (e.g., 9)

        Returns:
            int: The hour part as an integer, e.g., 9
        """
       
        if isinstance(time_val, int):
            return time_val
        elif isinstance(time_val, str):
            return int(time_val.split(":")[0])
        else:
            raise ValueError(f"Unexpected time value format: {time_val}")
