import re
import pandas as pd
from SRC.Interfaces.FileManager import FileManager
from SRC.Models.Course import Course
from SRC.Models.Lesson import Lesson
from SRC.Models.LessonTimes import LessonTimes
from SRC.Models.ValidationError import ValidationError

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
        elif 'ש.מחלקה' in type_str:
            return "departmentHours"
        elif 'תגבור' in type_str:
            return "reinforcement"
        elif 'הדרכה' in type_str:
            return "training"
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
            'תקופה': 'semester_hebrew',
            'נ"ז' : 'credit_points',
            'ש"ש' : 'weekly_hours_explicit'
        }

        for heb_col, eng_col in column_mapping.items():
            if heb_col in df.columns:
                df.rename(columns={heb_col: eng_col}, inplace=True)

        courses_dict = {}
        errors = []
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
            semester_hebrew = str(row.get("semester_hebrew", "")).strip()
            semester = 1 if "א" in semester_hebrew else 2 if "ב" in semester_hebrew else 0


            lesson_type = self.determine_lesson_type(type_str)
            start_hour, end_hour = self.parse_time_range(time_str)
            day = self.parse_day_from_hebrew(time_str)
            building, room = self.parse_location(location_str)

            instructors = [inst.strip() for inst in instructors_str.split(',') if inst.strip()]
            credit_points = float(row.get("credit_points", 0))  # נ"ז
            weekly_hours = float(row.get("weekly_hours_explicit", 0))  # ש"ש 

            group_code = int(code.split('-')[-1]) if '-' in code and code.split('-')[-1].isdigit() else 0
            main_code = code.split('-')[0] if '-' in code else code
            course_key = f"{main_code}_{name}"

            lesson = Lesson(
                time=LessonTimes(start_hour, end_hour, day),
                lesson_type=lesson_type,
                building=building,
                room=room,
                instructors=instructors,
                creditPoints=credit_points,
                weeklyHours=weekly_hours,
                groupCode=group_code
            )

            if course_key not in courses_dict:
                courses_dict[course_key] = Course(name=name, code=main_code, semester=semester, notes=notes)

            course = courses_dict[course_key]
            if lesson_type == "lecture":
                course.lectures.append(lesson)
            elif lesson_type == "exercise":
                course.exercises.append(lesson)
            elif lesson_type == "lab":
                course.labs.append(lesson)
            elif lesson_type == "departmentHours":
                course.departmentHours.append(lesson)
            elif lesson_type == "reinforcement":
                course.reinforcement.append(lesson)
            elif lesson_type == "training":
                course.training.append(lesson)
            else:
                course.training.append(lesson)
                
            
        return list(courses_dict.values()), errors
    # def read_courses_from_file(self, file_path: str) -> tuple[list[Course], list[ValidationError]]:
    #     df = pd.read_excel(file_path)

    #     column_mapping = {
    #         'שם': 'name',
    #         'קוד מלא': 'code',
    #         'סוג מפגש': 'type',
    #         'מועד': 'time',
    #         'מרצים': 'instructors',
    #         'הערה': 'notes',
    #         'חדר': 'location',
    #         'תקופה': 'semester_hebrew',
    #         'נ"ז': 'credit_points',
    #         'ש"ש': 'weekly_hours_explicit'
    #     }

    #     for heb_col, eng_col in column_mapping.items():
    #         if heb_col in df.columns:
    #             df.rename(columns={heb_col: eng_col}, inplace=True)

    #     courses_dict = {}
    #     errors = []

    #     for index, row in df.iterrows():
    #         name = str(row.get("name", "")).strip()
    #         code = str(row.get("code", "")).strip()
    #         row_context = {"row": index + 2, "course": name or "לא ידוע"}

    #         # שגיאות בסיסיות
    #         if not name:
    #             errors.append(ValidationError("שם הקורס חסר", context=row_context))
    #             continue
    #         if not code:
    #             errors.append(ValidationError("קוד הקורס חסר", context=row_context))
    #             continue

    #         type_str = str(row.get("type", "")).strip()
    #         time_str = str(row.get("time", "")).strip()
    #         instructors_str = str(row.get("instructors", "")).strip()
    #         notes = str(row.get("notes", "")).strip() if not pd.isna(row.get("notes", "")) else ""
    #         location_str = str(row.get("location", "")).strip() if not pd.isna(row.get("location", "")) else ""
    #         semester_hebrew = str(row.get("semester_hebrew", "")).strip()
    #         semester = 1 if "א" in semester_hebrew else 2 if "ב" in semester_hebrew else 0

    #         lesson_type = self.determine_lesson_type(type_str)
    #         start_hour, end_hour = self.parse_time_range(time_str)
    #         day = self.parse_day_from_hebrew(time_str)

    #         if start_hour == 0 and end_hour == 0:
    #             errors.append(ValidationError("שעת התחלה/סיום לא תקינה או חסרה", context=row_context))
    #         if day == 0:
    #             errors.append(ValidationError("יום לא תקין או חסר", context=row_context))

    #         building, room = self.parse_location(location_str)
    #         instructors = [inst.strip() for inst in instructors_str.split(',') if inst.strip()]

    #         try:
    #             credit_points = float(row.get("credit_points", 0)) if not pd.isna(row.get("credit_points")) else 0
    #         except:
    #             credit_points = 0
    #             errors.append(ValidationError('נ"ז לא תקין', context=row_context))

    #         try:
    #             weekly_hours = float(row.get("weekly_hours_explicit", 0)) if not pd.isna(row.get("weekly_hours_explicit")) else 0
    #         except:
    #             weekly_hours = 0
    #             errors.append(ValidationError("ש\"ש לא תקין", context=row_context))

    #         group_code = int(code.split('-')[-1]) if '-' in code and code.split('-')[-1].isdigit() else 0
    #         main_code = code.split('-')[0] if '-' in code else code
    #         course_key = f"{main_code}_{name}"

    #         lesson = Lesson(
    #             time=LessonTimes(start_hour, end_hour, day),
    #             lesson_type=lesson_type,
    #             building=building,
    #             room=room,
    #             instructors=instructors,
    #             creditPoints=credit_points,
    #             weeklyHours=weekly_hours,
    #             groupCode=group_code
    #         )

    #         if course_key not in courses_dict:
    #             courses_dict[course_key] = Course(name=name, code=main_code, semester=semester, notes=notes)

    #         course = courses_dict[course_key]
    #         if lesson_type == "lecture":
    #             course.lectures.append(lesson)
    #         elif lesson_type == "exercise":
    #             course.exercises.append(lesson)
    #         elif lesson_type == "lab":
    #             course.labs.append(lesson)
    #         elif lesson_type == "development":
    #             course.departmentHours.append(lesson)
    #         else:
    #             course.training.append(lesson)

    #     return list(courses_dict.values()), errors
