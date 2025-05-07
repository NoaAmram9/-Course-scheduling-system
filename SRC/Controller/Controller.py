import os
from SRC.Models.Course import Course
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
        self.display_schedule(time_table) # Display the schedule using the TimetableApp class
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
        TimetablesPage.TimetableApp(root, time_table)
        # Function to display the schedule using the TimetableApp class
        root.mainloop()  # <<< This is required to display the GUI window

    
    
    # Function to get the courses from the repository file
    def get_courses(self):
        return [
            Course(
                name="Introduction to Computer Science",
                code="CS101",
                instructor="Dr. Alice",
                lectures=["Mon 10:00-12:00"],
                exercises=["Wed 14:00-15:00"],
                labs=["Thu 10:00-11:00"]
            ),
            Course(
                name="Data Structures",
                code="CS102",
                instructor="Prof. Bob",
                lectures=["Tue 12:00-14:00"],
                exercises=["Thu 16:00-17:00"],
                labs=[]
            ),
            Course(
                name="Operating Systems",
                code="CS201",
                instructor="Dr. Carol",
                lectures=["Mon 08:00-10:00"],
                exercises=["Wed 10:00-11:00"],
                labs=["Fri 09:00-10:00"]
            ),
            Course(
                name="Algorithms",
                code="CS202",
                instructor="Dr. David",
                lectures=["Tue 10:00-12:00"],
                exercises=["Thu 12:00-13:00"],
                labs=[]
            ),
            Course(
                name="Databases",
                code="CS301",
                instructor="Prof. Eva",
                lectures=["Wed 08:00-10:00"],
                exercises=["Fri 11:00-12:00"],
                labs=["Mon 14:00-15:00"]
            ),
        ]
    