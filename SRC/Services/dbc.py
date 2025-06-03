import os
import sys
import traceback

# Add project root to path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from SRC.Services.ExcelManager import ExcelManager

def debug_excel_parsing(file_path):
    try:
        manager = ExcelManager()
        courses = manager.read_courses_from_file(file_path)

        for course in courses:
            print(f"\n📘 Course: {course._name} ({course._code})")
            print(f"📝 Notes: {course._notes}")
            print(f"📚 Semester: {course._semester}")
            
            def print_lessons(label, lessons):
                for i, lesson in enumerate(lessons, 1):
                    print(f"  🔹 {label} {i}:")
                    print(f"     🕒 Day: {lesson.time.day}")
                    print(f"     ⏰ Time: {lesson.time.start_hour}-{lesson.time.end_hour}")
                    print(f"     🏫 Building: {lesson.building}")
                    print(f"     🚪 Room: {lesson.room}")
                    print(f"     👥 Instructors: {', '.join(lesson.instructors) if lesson.instructors else 'None'}")
                    print(f"     🎓 Credit Points: {lesson.creditPoints}")
                    print(f"     🧮 Weekly Hours: {lesson.weeklyHours}")
                    print(f"     🔢 Group Code: {lesson.groupCode}")

            print_lessons("Lecture", course.lectures)
            print_lessons("Exercise", course.exercises)
            print_lessons("Lab", course.labs)
            print_lessons("DepartmentHour", course.departmentHours)
            print_lessons("Training", course.training)

    except Exception as e:
        print("❌ An error occurred while parsing the Excel file:")
        traceback.print_exc()

if __name__ == "__main__":
    # ⚠️ Replace this with your actual path to the Excel file
    excel_file = r"C:\Users\noaam\Desktop\מסמכי תואר- שנה ב\לימודי\software_engineer1\shcedual\-Course-scheduling-system\SRC\Services\EngineeringV2.xlsx"

    if os.path.exists(excel_file):
        debug_excel_parsing(excel_file)
    else:
        print("❌ Excel file not found!")
