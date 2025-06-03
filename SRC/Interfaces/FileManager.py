import os
from SRC.Interfaces.IFileManager import IFileManager

class FileManager(IFileManager):
    def read_from_file(self):
        raise NotImplementedError("Subclasses must implement this method.")
    
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
    
    def write_course_numbers_to_file(self, filename, course_numbers):
        """Writes a list of course numbers to a file"""
        try:
            with open(filename, "w", encoding="utf-8") as file:
                for number in course_numbers:
                    file.write(f"{number}\n")
            # print(f"Course numbers successfully written to '{filename}'.")
        except Exception as e:
            print(f"Error writing course numbers to file '{filename}': {e}")
    
    def delete_temp_files(self, filename1, filename2):
        """Delete temporary files created during the process"""
        temp_files = [filename1, filename2]
        for file in temp_files:
            if os.path.exists(file):
                 os.remove(file)
            