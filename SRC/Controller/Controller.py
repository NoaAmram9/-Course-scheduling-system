import os
from Models.TimeTable import Timetable
from Models.Course import Course

def read_courses_from_file(file_path):
    """קורא קובץ וממיר את הנתונים לרשימת קורסים"""
    courses = []
    if not os.path.exists(file_path):
        raise FileNotFoundError("קובץ הקורסים לא נמצא")
    
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 2:
                course_name = data[0]
                course_code = data[1]
                courses.append(Course(name=course_name, code=course_code))
    return courses


class ScheduleController:
    def __init__(self):
        self.timetable = Timetable()
    
    def generate_schedules(self, file_path):
        """יוצר מערכות שעות על בסיס הנתונים מהקובץ"""
        try:
            courses = read_courses_from_file(file_path)
            self.timetable.courses = courses
            # כאן אפשר להוסיף לוגיקה להפקת מערכות שעות שונות
            return [str(course.name + " - " + course.code) + "\n" for course in courses]
        except Exception as e:
            return str(e)
