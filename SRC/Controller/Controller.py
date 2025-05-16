from SRC.Services.FileManager import FileManager
from SRC.Services.ScheduleService import ScheduleService
import SRC.ViewLayer.View.TimetablesPage as TimetablesPage
from tkinterdnd2 import TkinterDnD

class Controller:
    
    # Function to set the progress of the program
    def run(self, file_path1, file_path2):
        courses_info = self.process_repository_file(file_path1) # Process the repository file with all the courses info
        selected_courses = self.get_selected_courses(file_path2) # Get the selected courses from the user
        selected_courses_info = self.selected_courses_info(courses_info, selected_courses) # Get the selected courses info from the repository
        time_table = self.create_schedules(selected_courses_info, file_path2, file_path1) # Create the schedules based on the selected courses
        # self.display_schedule(time_table) # Display the schedule using the TimetableApp class
        #self.write_schedule_to_file(time_table) # Write the schedule to an output file
    
    # Function to process the repository file with all the courses info       
    def process_repository_file(self, file_path):
        dataManager = FileManager()
        return dataManager.read_courses_from_file(file_path)
    
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
    
    # Function to create the schedules based on the selected courses
    def create_schedules(self, selected_courses, selected_courses_path, courses_info_path):
        dataManager = FileManager()

        # Validate that all selected course numbers exist in the courses info
        if not dataManager.validate_course_numbers_exist(selected_courses_path, courses_info_path):
            print("Error: Some selected courses are invalid.")
            return []
        
        scheduleService = ScheduleService()
        return scheduleService.generate_schedules(selected_courses)
    
    
    # Function to write the schedule to an output file
    def write_schedule_to_file(self, time_table):
        dataManager = FileManager()
        dataManager.write_schedule_to_file("schedule.txt", time_table)
    
    # todo: change location    
    def display_schedule(self, time_table):
        root = TkinterDnD.Tk()
        TimetablesPage.TimetablesPage(root, time_table)
        # Function to display the schedule using the TimetableApp class
        root.mainloop()  # <<< This is required to display the GUI window

    
    def create_selected_courses_file(self, selected_courses, file_path):
        dataManager = FileManager()
        dataManager.write_course_numbers_to_file(file_path, selected_courses)
    
    def get_all_options(self, file_path1, file_path2):
        courses_info = self.process_repository_file(file_path1) # Process the repository file with all the courses info
       
        selected_courses = self.get_selected_courses(file_path2) # Get the selected courses from the user
        selected_courses_info = self.selected_courses_info(courses_info, selected_courses) # Get the selected courses info from the repository
        time_table = self.create_schedules(selected_courses_info, file_path2, file_path1) # Create the schedules based on the selected courses
        return time_table
    
    def handle_exit(self):
        """
        Handle the exit of the application.
        This method is called when the application is about to exit.
        delete the temporary files
        
        """
        file_path1 = "Data/selected_courses.txt"
        file_path2 = "Data/courses.txt"
        dataManager = FileManager()
        dataManager.delete_temp_files(file_path1, file_path2)

    