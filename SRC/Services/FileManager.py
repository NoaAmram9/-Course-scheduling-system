import re
import os

from SRC.Models.Course import Course
from SRC.Models.LessonTimes import LessonTimes
from SRC.Models.Lesson import Lesson

class FileManager:
    
    # Constructor
    def __init__(self):
        pass

    # Read course numbers from a file - the chosen courses
    def read_course_numbers_from_file(self, filename):
        """ Reads a file and converts it into a list of course numbers """
        course_numbers = []
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            return []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()   # Read the entire file content
                
            if not content:
                print(f"Warning: File '{filename}' is empty.")
                return []

            course_numbers = content.strip().split("\n")  # Split the file into lines
            
            if not course_numbers or all(number.strip() == "" for number in course_numbers):
                print(f"Warning: No valid course numbers found in '{filename}'.")
                return []
            
            if len(course_numbers) > 7:
                print(f"Warning: Expected no more then 7 course numbers, but found {len(course_numbers)} in '{filename}'.")
                return []
            
            # Validate all entries are digits
            for num in course_numbers:
                if not num.isdigit():
                    print(f"Warning: Invalid course number '{num}' found in '{filename}'. Only numeric values are allowed.")
                    return []

        except Exception as e:
            print(f"Error reading file '{filename}': {e}")

        return course_numbers  # Return the list of course numbers

    # Read courses from a file
    def read_courses_from_file(self, filename):
        """ Reads a file and converts it into a list of Course objects """
        courses = []
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            return []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()   # Read the entire file content
                
            if not content:
                print(f"Warning: File '{filename}' is empty.")
                return []

            # Split the file into blocks (of courses) using "$$$$" as a separator
            course_blocks = content.split("$$$$")[1:] # ignore the first element (empty string for the first $$$$) 
            
            if not course_blocks or all(block.strip() == "" for block in course_blocks):
                print(f"Warning: No valid course data found in '{filename}'.")
                return []
            
            # Iterate over each course block
            for block in course_blocks:
                
                lines = block.strip().split("\n") # Split into lines
                
                if len(lines) < 5:
                    print("Skipping invalid course block: Less than 5 lines of basic info.")
                    continue  # Ensure at least course name, course number, and instructor, Lecture, exercise (at least one)
                

                name, course_number, instructor = lines[:3]  # The first three lines are name, number, and instructor
                
                # Ensure no empty values for mandatory fields
                if not (name and course_number and instructor):
                    print(f"Skipping invalid course '{name}': Missing required fields.")
                    continue
            
                # Separate lessons by type
                lectures = []
                exercises = []
                labs = []
                    
                for line in lines[3:]:  # Iterate over the remaining lines in the course block for lessons data
                    
                    lessonType, lessonData = line[0], line[1:].strip() # Get the type of the line (Lecture, Exercise, or Lab)
                    
                    # If it's not a valid lesson type, skip the line
                    if lessonType not in {"L", "T", "M"}:
                        print(f"Skipping unknown lesson type '{lessonType}' in course '{name}'")
                        continue
                    
                    # Regular expression pattern for time slots
                    time_slot_pattern = re.compile(r"(\d),(\d{2}:\d{2}),(\d{2}:\d{2}),(\d{1,4}),(\d{1,3})")
                    
                    time_slots = [slot.strip() for slot in lessonData.split("S,") if slot.strip()] # Split the line into time slots, remove the separator s
                    
                    for time_slot in time_slots:
                        match = time_slot_pattern.match(time_slot)  # Check if the line matches the time slot format
                        
                        if not match:
                            print(f"Skipping invalid time slot format: '{time_slot}' in course '{name}'")
                            continue
                            
                        day, start, end, building, room = match.groups()
                        lessonTimes= LessonTimes (start, end, day)  # Create a new lesson times object
                        lesson = Lesson(lessonTimes, lessonType, building, room)  # Create a new lesson object
                        # Store in the correct category
                        if lessonType == "L":
                            lectures.append(lesson)
                        elif lessonType == "T":
                            exercises.append(lesson)
                        elif lessonType == "M":
                            labs.append(lesson)
                    
                if not (lectures and exercises): # Ensure at least one lecture and one exercise
                    print(f"Skipping course '{name}': No valid lessons found.")
                    continue
            
                course = Course(name, course_number, instructor, lectures, exercises, labs)
                courses.append(course)  # add the course to the list


        except Exception as e:
            print(f"Error reading file '{filename}': {e}")

        return courses  # Return the list of courses

    # Write courses to a file
    def write_courses_to_file(self, file, courses):
        """ Writes a list of courses to a new file in the required format """
        try: 
                for course in courses:                    
                    if not course.name or not course.code or not course.instructor or not course.lectures:
                        print(f"Skipping incomplete course '{course.name}' during writing.")
                        continue
                
                    # Write Course Name, Course Number, and Instructor
                    file.write(f"{course.name}\n")
                    file.write(f"{course.code}\n")
                    file.write(f"{course.instructor}\n")

                    # Write Lectures, Exercises, and Labs in order
                    file.write(self.format_lessons(course.lectures, "L"))
                    file.write(self.format_lessons(course.exercises, "T"))
                    file.write(self.format_lessons(course.labs, "M"))

                    # Add course separator
                    file.write("$$$$\n")

        except Exception as e:
            print(f"Error writing file '{file}': {e}")

    # Write timetable options to a file
    def write_schedule_to_file(self, filename, schedule_options):
        """ Writes multiple timetable options to a file in the required format """
        try:
            # נוודא שהקובץ נפתח במצב כתיבה רגילה בהתחלה (ניצור קובץ חדש)
            with open(filename, "w", encoding="utf-8") as file:
                file.write("")  # מרוקן את הקובץ אם הוא כבר קיים
                
                for schedule in schedule_options:
                    # כתיבת כל אפשרות מערכת שעות לקובץ
                    self.write_courses_to_file(file, schedule.courses)  
                    file.write("*****\n")
                print(f"Schedule options successfully written to '{filename}'.")
                

        except Exception as e:
            print(f"Error writing schedule to file '{filename}': {e}")
       
    # Format lessons for writing to file
    def format_lessons(self,lessons, lesson_type):
        """Formats lesson data for writing to a file"""
        if not lessons:
            return ""
        
        try:
            times = [f"S,{l.time.day},{l.time.start_hour},{l.time.end_hour},{l.building},{l.room}" for l in lessons]
            return lesson_type + " " + ", ".join(times) + "\n"
        
        except Exception as e:
            print(f"Error formatting lessons: {e}")
            return ""