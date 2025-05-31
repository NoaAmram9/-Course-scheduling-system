import re
import pandas as pd
from SRC.Interfaces.FileManager import FileManager
from SRC.Models.Course import Course
from SRC.Models.Lesson import Lesson
from SRC.Models.LessonTimes import LessonTimes

class ExcelManager(FileManager):
    @staticmethod
    def parse_time_range(time_str: str) -> tuple:
        if not time_str or pd.isna(time_str):
            return (0, 0)
        
        time_match = re.search(r'(\d{1,2}):(\d{2})-(\d{1,2}):(\d{2})', str(time_str))
        if time_match:
            start_hour = int(time_match.group(1))
            end_hour = int(time_match.group(3))
            return (start_hour, end_hour)
        return (0, 0)

    @staticmethod
    def parse_day_from_hebrew(time_str: str) -> int:
        if not time_str or pd.isna(time_str):
            return 0
        
        day_mapping = {
            'א': 0, 'ב': 1, 'ג': 2, 'ד': 3, 'ה': 4, 'ו': 5, 'ש': 6,
            'ראשון': 0, 'שני': 1, 'שלישי': 2, 'רביעי': 3,
            'חמישי': 4, 'שישי': 5, 'שבת': 6
        }
        match = re.match(r'^([א-ת]+)', str(time_str).strip())
        if match:
            return day_mapping.get(match.group(1), 0)
        return 0

    @staticmethod
    def determine_lesson_type(type_str: str) -> str:
        if not type_str or pd.isna(type_str):
            return "unknown"
        
        type_str = str(type_str).lower()
        if 'הרצאה' in type_str:
            return "lecture"
        elif 'תרגיל' in type_str or 'תרגול' in type_str:
            return "exercise"
        elif 'מעבדה' in type_str:
            return "lab"
        elif 'פיתוח' in type_str:
            return "development"
        elif 'שיעות' in type_str:
            return "lesson"
        else:
            return "other"

    @staticmethod
    def parse_location(location_str: str) -> tuple:
        if not location_str or pd.isna(location_str):
            return ("", "")

        # Remove Hebrew and keep only parts like "1102 - 2" or "A1300 - 1"
        cleaned = re.sub(r'[^\w\s\-]', '', str(location_str))  # remove non-alphanumerics
        parts = cleaned.split('-')

        if len(parts) >= 2:
            building = parts[-2].strip()
            room = parts[-1].strip()
            return (building, room)

        # Fallback: Try to find all alphanumeric words
        tokens = re.findall(r'\w+', str(location_str))
        if len(tokens) >= 2:
            return (tokens[-2], tokens[-1])
        elif len(tokens) == 1:
            return (tokens[0], "")
        
        return ("", "")
    def read_courses_from_file(self, file_path: str) -> list[Course]:
        df = pd.read_excel(file_path)

        column_mapping = {
            'שם': 'name',
            'קוד מלא': 'code',
            'סוג מפגש': 'type',
            'מועד': 'time',
            'מרצים': 'instructors',
            'הערה': 'notes',
            'חדר': 'location',
        }

        for heb_col, eng_col in column_mapping.items():
            if heb_col in df.columns:
                df.rename(columns={heb_col: eng_col}, inplace=True)

        courses_dict = {}

        for _, row in df.iterrows():
            name = str(row.get("name", "")).strip()
            if not name:
                continue

            code = str(row.get("code", "")).strip()
            type_str = str(row.get("type", "")).strip()
            time_str = str(row.get("time", "")).strip()
            instructors_str = str(row.get("instructors", "")).strip()
            notes = str(row.get("notes", "")).strip()
            location_str = str(row.get("location", "")).strip()

            lesson_type = self.determine_lesson_type(type_str)
            start_hour, end_hour = self.parse_time_range(time_str)
            day = self.parse_day_from_hebrew(time_str)
            building, room = self.parse_location(location_str)

            instructors = [inst.strip() for inst in instructors_str.split(',') if inst.strip()]
            weekly_hours = max(0, end_hour - start_hour)

            group_code = int(code.split('-')[-1]) if '-' in code and code.split('-')[-1].isdigit() else 0
            main_code = code.split('-')[0] if '-' in code else code
            course_key = f"{main_code}_{name}"

            lesson = Lesson(
                time=LessonTimes(start_hour, end_hour, day),
                lesson_type=lesson_type,
                building=building,
                room=room,
                instructors=instructors,
                creditPoints=0,
                weeklyHours=weekly_hours,
                groupCode=group_code
            )

            if course_key not in courses_dict:
                courses_dict[course_key] = Course(name=name, code=main_code, semester=0, notes=notes)

            course = courses_dict[course_key]
            if lesson_type == "lecture":
                course.lectures.append(lesson)
            elif lesson_type == "exercise":
                course.exercises.append(lesson)
            elif lesson_type == "lab":
                course.labs.append(lesson)
            elif lesson_type == "development":
                course.departmentHours.append(lesson)
            else:
                course.training.append(lesson)


        return list(courses_dict.values())
