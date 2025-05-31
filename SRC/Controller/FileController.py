from SRC.Services.ExcelManager import ExcelManager
from SRC.Services.TxtManager import TxtManager
from SRC.Interfaces.FileManager import FileManager
from SRC.Services.ScheduleService import ScheduleService

class FileController:
    def __init__(self, file_type: str):
        if file_type == "excel":
            self.file_manager = ExcelManager()
        elif file_type == "txt":
            self.file_manager = TxtManager()
        else:
            raise ValueError("Unsupported file type. Use 'excel' or 'txt'.")

    def read_courses_from_file(self, file_path: str):
        return self.file_manager.read_courses_from_file(file_path)

    def write_courses(self, file_path: str, courses):
        self.file_manager.write_courses_to_file(file_path, courses)
       
     # Function to get the selected courses from the user    
    def get_selected_courses(self, file_path):
        dataManager = FileManager()
        return dataManager.read_course_numbers_from_file(file_path)   
    # Function to get the selected courses info from the repository
    def selected_courses_info(self, courses_info, selected_courses):
        selected_courses_info = []
        for course in courses_info:
            if course.code in selected_courses:
                selected_courses_info.append(course)
        return selected_courses_info
    
    # Function to create the schedual from selected courses file
    def create_selected_courses_file(self, selected_courses, file_path):
        dataManager = FileManager()
        dataManager.write_course_numbers_to_file(file_path, selected_courses)
      
        
    # Function to create the schedules based on the selected courses
    def create_schedules(self, selected_courses):
        scheduleService = ScheduleService()
        return scheduleService.generate_schedules(selected_courses, limit=1000)
    
    def get_all_options(self, file_path1, file_path2):
        courses_info = self.read_courses_from_file(file_path1) # Process the repository file with all the courses info

        selected_courses = self.get_selected_courses(file_path2) # Get the selected courses from the user
        selected_courses_info = self.selected_courses_info(courses_info, selected_courses) # Get the selected courses info from the repository
        time_table = self.create_schedules(selected_courses_info) # Create the schedules based on the selected courses
        return time_table
    
    def handle_exit(self):
        """
        Handle the exit of the application.
        This method is called when the application is about to exit.
        delete the temporary files
        
        """
        file_path1 = "Data/selected_courses.txt"
        file_path2 = "Data/courses.xlsx"
        dataManager = FileManager()
        dataManager.delete_temp_files(file_path1, file_path2)

    