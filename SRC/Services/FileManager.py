import re
import os

from datetime import datetime
from SRC.Models.Course import Course
from SRC.Models.LessonTimes import LessonTimes
from SRC.Models.Lesson import Lesson
from SRC.Models.ValidationError import ValidationError

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
            
            if len(course_numbers) != len(set(course_numbers)):
                print(f"Warning: Duplicate course numbers found in '{filename}'.")
                return []
            
            for num in course_numbers:
                if not num.isdigit():
                    print(f"Warning: Invalid course number '{num}' found in '{filename}'. Only numeric values are allowed.")
                    return []
                
                if not len(num) == 5:
                    print(f"Warning: Invalid Non 5-digit course number found in '{filename}'.")
                    return []

        except Exception as e:
            print(f"Error reading file '{filename}': {e}")
            
        return course_numbers  # Return the list of course numbers

    # Read courses from a file
    def read_courses_from_file(self, filename):
        """ Reads a file and converts it into a list of Course objects """
        courses = []
        errors = []
        seen_courses = set()

        if not os.path.exists(filename):
            return [ValidationError(f"File '{filename}' not found.")]
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()   # Read the entire file content
                
            if not content:
                return [ValidationError(f"File '{filename}' is empty.")]

            # Split the file into blocks (of courses) using "$$$$" as a separator
            course_blocks = content.split("$$$$")[1:] # ignore the first element (empty string for the first $$$$) 
            
            if not course_blocks or all(block.strip() == "" for block in course_blocks):
                return [ValidationError(f"No valid course data found in '{filename}'.")]
            
            # Iterate over each course block
            for block in course_blocks:
                
                lines = block.strip().split("\n") # Split into lines
                
                if len(lines) < 4:
                    errors.append(ValidationError(f"Invalid course data: Less than 4 lines of basic info (name, code, instructor, lecture).", context=lines[:1]))
                    continue  # Ensure at least course name, course number, and instructor, Lecture (at least one)
                

                name, course_number, instructor = lines[:3]  # The first three lines are name, number, and instructor
                
                # Check course number (ensure it's 5 digits and numeric)
                if not (course_number.isdigit() and len(course_number) == 5):
                    errors.append(ValidationError(f"Invalid course number '{course_number}' for course '{name}'. It must be a 5-digit number."))
                    continue  # Skip this course if the number is invalid


                # Ensure no empty values for mandatory fields
                if not (name and course_number and instructor):
                    errors.append(ValidationError(f"Invalid course '{name}': Missing required fields."))
                    continue
            
                # Check if the exact course (same number, name, and instructor) already exists
                course_key = (course_number, name, instructor)
                if course_key in seen_courses:
                    errors.append(ValidationError(f"Skipping duplicate course '{name}' ({course_number}) by '{instructor}'."))
                    continue
                seen_courses.add(course_key)

                # Separate lessons by type
                lectures = []
                exercises = []
                labs = []
                    
                for line in lines[3:]:  # Iterate over the remaining lines in the course block for lessons data
                    
                    lessonType, lessonData = line[0], line[1:].strip() # Get the type of the line (Lecture, Exercise, or Lab)
                    
                    # If it's not a valid lesson type, skip the line
                    if lessonType not in {"L", "T", "M"}:
                        errors.append(ValidationError(f"Skipping unknown lesson type '{lessonType}' in course '{name}'"))
                        continue
                    
                    # Regular expression pattern for time slots
                    time_slot_pattern = re.compile(r"(\d),(\d{2}:\d{2}),(\d{2}:\d{2}),(\d{1,4}),(\d{1,3})")
                    
                    time_slots = [slot.strip() for slot in lessonData.split("S,") if slot.strip()] # Split the line into time slots, remove the separator s
                    
                    for time_slot in time_slots:
                        match = time_slot_pattern.match(time_slot)  # Check if the line matches the time slot format
                        
                        if not match:
                            errors.append(ValidationError(f"Skipping invalid time slot format: '{time_slot}' in course '{name}'"))
                            continue
                            
                        day, start, end, building, room = match.groups()
                        
                        try:
                            day = int(day)  # Convert day to integer
                            if not (1 <= day <= 7): # Check if day is between 1 and 7 (Sunday to saturday)
                                raise ValueError("Day must be between 1 and 7.")

                            # Convert times to datetime objects for comparison
                            start_time = datetime.strptime(start, "%H:%M")
                            end_time = datetime.strptime(end, "%H:%M")

                            # Define time bounds
                            earliest = datetime.strptime("08:00", "%H:%M")
                            latest = datetime.strptime("21:00", "%H:%M")

                            if not (earliest <= start_time < end_time <= latest):
                                raise ValueError("Time must be between 08:00 and 21:00, and start < end.")

                            # If all checks pass, create the lesson time object
                            lessonTimes = LessonTimes(start, end, day)

                        except ValueError as e:
                            errors.append(ValidationError(f"Invalid time slot data in course '{name}': {e} --> '{time_slot}'"))
                            continue
                        
                        lessonTimes= LessonTimes (start, end, day)  # Create a new lesson times object
                        lesson = Lesson(lessonTimes, lessonType, building, room)  # Create a new lesson object
                        # Store in the correct category
                        if lessonType == "L":
                            lectures.append(lesson)
                        elif lessonType == "T":
                            exercises.append(lesson)
                        elif lessonType == "M":
                            labs.append(lesson)
                    
                if not (lectures): # Ensure at least one lecture
                    errors.append(ValidationError(f"Skipping course '{name}': No valid lecture found."))
                    continue
            
                course = Course(name, course_number, instructor, lectures, exercises, labs)
                courses.append(course)  # add the course to the list


        except Exception as e:
            return [ValidationError(f"Error reading file '{filename}': {e}")] 
        # return courses, errors
        return errors if errors else courses  # Return the list of courses/errors if any

    # Validate that selected courses exist in the courses file
    def validate_course_numbers_exist(self, numbers_filename, courses_filename):
        """ Checks if course numbers in the selected courses file exist in the courses file. """
        valid_course_numbers = set(course.code for course in self.read_courses_from_file(courses_filename))
        selected_course_numbers = self.read_course_numbers_from_file(numbers_filename)

        missing_courses = [num for num in selected_course_numbers if num not in valid_course_numbers]
        if missing_courses:
            print(f"Warning: The following course numbers are invalid (not found in course list): {', '.join(missing_courses)}")
            return False
        
        return True
    
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