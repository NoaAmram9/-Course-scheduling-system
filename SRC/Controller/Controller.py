import os
from SRC.Services.FileManager import FileManager
from SRC.Services.ScheduleService import ScheduleService

class Controller:
    
    # Function to set the progress of the program
    def run(self, file_path1, file_path2):
        courses_info = self.process_repository_file(file_path1) # Process the repository file with all the courses info
        selected_courses = self.get_selected_courses(file_path2) # Get the selected courses from the user
        selected_courses_info = self.selected_courses_info(courses_info, selected_courses) # Get the selected courses info from the repository
        time_table = self.create_schedules(selected_courses_info) # Create the schedules based on the selected courses
        self.write_schedule_to_file(time_table) # Write the schedule to an output file
    
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
    def create_schedules(self, selected_courses):
        scheduleService = ScheduleService()
        return scheduleService.generate_schedules(selected_courses)
    
    # Function to write the schedule to an output file
    def write_schedule_to_file(self, time_table):
        dataManager = FileManager()
        dataManager.write_schedule_to_file("schedule.txt", time_table)