import re
import pandas as pd
from datetime import datetime
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
            'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ש': 7,
            'ראשון': 1, 'שני': 2, 'שלישי': 3, 'רביעי': 4,
            'חמישי': 5, 'שישי': 6, 'שבת': 7
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

        cleaned = re.sub(r'[^\w\s\-]', '', str(location_str))
        parts = cleaned.split('-')

        if len(parts) >= 2:
            building = parts[-2].strip()
            room = parts[-1].strip()
            return (building, room)

        tokens = re.findall(r'\w+', str(location_str))
        if len(tokens) >= 2:
            return (tokens[-2], tokens[-1])
        elif len(tokens) == 1:
            return (tokens[0], "")

        return ("", "")

    def read_courses_from_file(self, file_path: str) -> tuple[list[Course], list[ValidationError]]:
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

        for index, row in df.iterrows():
            name = str(row.get("name", "")).strip()
            code = str(row.get("code", "")).strip()
            row_context = {"row": index + 2, "course": name or "Unknown"}

            if not name:
                errors.append(ValidationError("Missing course name", context=row_context))
                continue
            if not code:
                errors.append(ValidationError("Missing course code", context=row_context))
                continue

            type_str = str(row.get("type", "")).strip()
            time_str = str(row.get("time", "")).strip()
            instructors_str = str(row.get("instructors", "")).strip()
            notes = str(row.get("notes", "")).strip() if not pd.isna(row.get("notes", "")) else ""
            location_str = str(row.get("location", "")).strip() if not pd.isna(row.get("location", "")) else ""
            semester_hebrew = str(row.get("semester_hebrew", "")).strip()
            semester = 1 if "א" in semester_hebrew else 2 if "ב" in semester_hebrew else 0

            lesson_type = self.determine_lesson_type(type_str)

            # Skip if time is completely empty or NaN
            if not time_str or pd.isna(row.get("time")):
                continue
            
            start_hour, end_hour = self.parse_time_range(time_str)
            day = self.parse_day_from_hebrew(time_str)

            if start_hour == 0 and end_hour == 0:
                errors.append(ValidationError("Invalid time format", context=row_context))
            if day == 0:
                errors.append(ValidationError("Invalid or missing day", context=row_context))


            try:
                start_time = datetime.strptime(f"{start_hour:02}:00", "%H:%M")
                end_time = datetime.strptime(f"{end_hour:02}:00", "%H:%M")
                if not (datetime.strptime("08:00", "%H:%M") <= start_time < end_time <= datetime.strptime("22:00", "%H:%M")):
                    raise ValueError("Time must be between 08:00 and 22:00 and start < end")
            except Exception as e:
                errors.append(ValidationError(f"Time error: {e}", context=row_context))

            building, room = self.parse_location(location_str)
            instructors = [inst.strip() for inst in instructors_str.split(',') if inst.strip()]

            try:
                credit_points = float(row.get("credit_points", 0)) if not pd.isna(row.get("credit_points")) else 0
            except:
                credit_points = 0
                errors.append(ValidationError("Invalid credit points", context=row_context))

            try:
                weekly_hours = float(row.get("weekly_hours_explicit", 0)) if not pd.isna(row.get("weekly_hours_explicit")) else 0
            except:
                weekly_hours = 0
                errors.append(ValidationError("Invalid weekly hours", context=row_context))

            group_code = int(code.split('-')[-1]) if '-' in code and code.split('-')[-1].isdigit() else 0
            if group_code == 0:
                errors.append(
                    ValidationError(
                        f"Missing or invalid group number in course code '{code}'. Expected format: '12345-01'.",
                        context=row_context
                    )
                )

            main_code = code.split('-')[0] if '-' in code else code
            if not (main_code.isdigit() and len(main_code) == 5):
                errors.append(
                    ValidationError(
                        f"Invalid course code '{main_code}'. It must be a 5-digit number.",
                        context=row_context
                    )
                )

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
                course.departmentHours.append(lesson) #אשנב???

        # Post-validation: check for duplicate group codes and mismatched course names
        seen_group_codes = {} 
        code_to_names = {}     

        for course in courses_dict.values():
            main_code = course.code
            course_name = course.name

            # Track course names associated with this main_code
            if main_code not in code_to_names:
                code_to_names[main_code] = set()
            code_to_names[main_code].add(course_name)

            # Track group codes within the same course
            if main_code not in seen_group_codes:
                seen_group_codes[main_code] = set()

            all_lessons = (
                course.lectures + course.exercises + course.labs +
                course.reinforcement + course.training + course.departmentHours
            )

            for lesson in all_lessons:
                if lesson.groupCode in seen_group_codes[main_code]:
                    errors.append(
                        ValidationError(
                            f"Duplicate group number {lesson.groupCode:02} found in course {main_code} ({course_name})",
                            context={"course": course_name, "group": lesson.groupCode}
                        )
                    )
                else:
                    seen_group_codes[main_code].add(lesson.groupCode)

        # Check if any main course code is associated with multiple names
        for main_code, names in code_to_names.items():
            if len(names) > 1:
                name_list = ', '.join(sorted(names))
                errors.append(
                    ValidationError(
                        f"Course number {main_code} appears with multiple names: {name_list}",
                        context={"course_code": main_code}
                    )
                )


        # Post-validation: Ensure valid lesson combinations
        for course in courses_dict.values():
            if course.training and not course.reinforcement:
                errors.append(
                    ValidationError(
                        f"Course '{course.name}' ({course.code}) has training but no reinforcement.",
                        context={"course": course.name}
                    )
                )


        return list(courses_dict.values()), errors
