from datetime import datetime
import os
import re
from SRC.Interfaces.FileManager import FileManager
from SRC.Models.Course import Course
from SRC.Models.Lesson import Lesson
from SRC.Models.LessonTimes import LessonTimes
from SRC.Models.ValidationError import ValidationError
class TxtManager(FileManager):
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
                

                name, code, instructor = lines[:3]  # The first three lines are name, number, and instructor
                
                # Check course number (ensure it's 5 digits and numeric)
                if not (code.isdigit() and len(code) == 5):
                    errors.append(ValidationError(f"Invalid course number '{code}' for course '{name}'. It must be a 5-digit number."))
                    continue  # Skip this course if the number is invalid


                # Ensure no empty values for mandatory fields
                if not (name and code and instructor):
                    errors.append(ValidationError(f"Invalid course '{name}': Missing required fields."))
                    continue
            
                # Check if the exact course (same number, name, and instructor) already exists
                course_key = (code, name, instructor)
                if course_key in seen_courses:
                    errors.append(ValidationError(f"duplicate course '{name}' ({code}) by '{instructor}'."))
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
                        errors.append(ValidationError(f"Unknown lesson type '{lessonType}' in course '{name}'"))
                        continue
                    
                    # Regular expression pattern for time slots
                    time_slot_pattern = re.compile(r"(\d),(\d{2}:\d{2}),(\d{2}:\d{2}),(\d{1,4}),(\d{1,3})")
                    
                    time_slots = [slot.strip() for slot in lessonData.split("S,") if slot.strip()] # Split the line into time slots, remove the separator s
                    
                    for time_slot in time_slots:
                        match = time_slot_pattern.match(time_slot)  # Check if the line matches the time slot format
                        
                        if not match:
                            errors.append(ValidationError(f"Invalid time slot format: '{time_slot}' in course '{name}'"))
                            continue
                            
                        day, start, end, building, room = match.groups()
                        
                        try:
                            day = int(day)  # המרת היום למספר שלם
                            if not (1 <= day <= 7):  # בדיקה שהיום בין 1 ל-7 (ראשון עד שבת)
                                raise ValueError("Day must be between 1 and 7.")

                            # נניח ש-start ו-end הם מחרוזות בפורמט "HH:MM"
                            # נחלץ רק את השעה (HH) מתוך המחרוזת
                            start_hour = start.split(':')[0]
                            end_hour = end.split(':')[0]
                              
                            # המרת השעות למבני datetime לצורך בדיקות השוואה
                            start_time = datetime.strptime(start, "%H:%M")
                            end_time = datetime.strptime(end, "%H:%M")

                            # הגדרת טווח שעות חוקי
                            earliest = datetime.strptime("08:00", "%H:%M")
                            latest = datetime.strptime("21:00", "%H:%M")

                            if not (earliest <= start_time < end_time <= latest):
                                raise ValueError("Time must be between 08:00 and 21:00, and start < end.")

                            # אם כל הבדיקות עברו, צור את האובייקט LessonTimes עם השעות כמחרוזות HH בלבד
                            lessonTimes = LessonTimes(int(start_hour), int(end_hour), day)
                        except ValueError as e:
                            errors.append(ValidationError(f"Invalid time slot data in course '{name}': {e} --> '{time_slot}'"))
                            continue
                        
                        lessonTimes = LessonTimes(int(start_hour), int(end_hour), day)  # Create a new lesson times object
                        lesson = Lesson(lessonTimes, lessonType, building, room)  # Create a new lesson object
                        # Store in the correct category
                        if lessonType == "L":
                            lectures.append(lesson)
                        elif lessonType == "T":
                            exercises.append(lesson)
                        elif lessonType == "M":
                            labs.append(lesson)
                    
                if not (lectures): # Ensure at least one lecture
                    errors.append(ValidationError(f"Course '{name}': No valid lecture found."))
                    continue
            
                course = Course(name, code,1, lectures, exercises, labs)
                courses.append(course)  # add the course to the list


        except Exception as e:
            return [ValidationError(f"Error reading file '{filename}': {e}")] 
        
        return (courses, errors)