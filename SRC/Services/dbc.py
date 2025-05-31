
    
import os
import sys

# Add project root to path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from SRC.Services.ExcelManager import ExcelManager

def debug_excel_parsing(file_path):
    manager = ExcelManager()
    courses = manager.read_courses_from_file(file_path)

    for course in courses:
        print(f"\n📘 Course: {course._name} ({course._code})")
        
        def print_lessons(label, lessons):
            for lesson in lessons:
                print(f"  🔹 {label}: Day {lesson.time.day}, {lesson.time.start_hour}-{lesson.time.end_hour}, Room {lesson.room}, Building {lesson.building} , Code {lesson.groupCode}")

        print_lessons("Lecture", course.lectures)
        print_lessons("Exercise", course.exercises)
        print_lessons("Lab", course.labs)
        print_lessons("DepartmentHour", course.departmentHours)
        print_lessons("Training", course.training)

if __name__ == "__main__":
    # ⚠️ Replace this with your actual path to the Excel file
    excel_file =r"C:\Users\noaam\Desktop\מסמכי תואר- שנה ב\לימודי\software_engineer1\shcedual\-Course-scheduling-system\SRC\Services\example.xlsx"

    
    if os.path.exists(excel_file):
        debug_excel_parsing(excel_file)
    else:
        print("❌ Excel file not found!")
