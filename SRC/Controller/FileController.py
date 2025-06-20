from SRC.Services.ExcelManager import ExcelManager
from SRC.Services.TxtManager import TxtManager
from SRC.Interfaces.FileManager import FileManager
from SRC.Services.ScheduleService import ScheduleService
from SRC.Services.TimeConstraintsService import TimeConstraintsService

class FileController:
    def __init__(self, file_type: str, filePath: str = None):
        self.filePath = filePath
        if file_type == ".xlsx" or file_type == ".xls":
            self.file_manager = ExcelManager()
        elif file_type == ".txt":
            self.file_manager = TxtManager()
        else:
            raise ValueError("Unsupported file type. Use 'excel' or 'txt'.")
        self.time_constraints_service = TimeConstraintsService()
        self._injected_constraints = []



    def get_file_type(self) -> str:
        return self.file_type

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
  

    def get_all_options(self, file_path1, file_path2, batch_size=100):
        """
        Returns batches of timetables instead of individual timetables
        This replaces the old method that returned individual timetables
        """

        courses_info = self.read_courses_from_file(file_path1)[0]  # Get the first element which is the courses info
        selected_courses = self.get_selected_courses(file_path2)
        selected_courses_info = self.selected_courses_info(courses_info, selected_courses)
        
        # Optional: Include dummy blocked courses if added earlier
        if hasattr(self, "_injected_constraints"):
            selected_courses_info.extend(self._injected_constraints)


        try:
            schedule_service = ScheduleService()
            
            # Get the progressive generator (no limit)
            schedule_generator = schedule_service.generate_schedules_progressive(
                selected_courses_info,  
                limit=None # No limit, to get all possible schedules
            )
            
            # Collect into batches
            batch = []
            for timetable in schedule_generator:
                batch.append(timetable)
                
                # When batch is full, yield it
                if len(batch) >= batch_size:
                    yield batch
                    batch = []  # Reset for next batch
                    
            # Yield final batch if it has any items
            if batch:
                yield batch
                            
        except Exception as e:
            print(f"Error in batch generator: {str(e)}")
            return []  # החזר רשימה ריקה במקום 

       
    def handle_exit(self):
        """
        Handle the exit of the application.
        This method is called when the application is about to exit.
        delete the temporary files
        
        """
        # file_path1 = self.filePath
        # file_path2 = "Data/courses.xlsx"
        # file_path2 = "Data/selected_courses.txt"
        files = ["Data/courses.xlsx", "Data/selected_courses.txt", self.filePath]
        dataManager = FileManager()
        dataManager.delete_temp_files(files)

    def apply_time_constraints(self, constraints: list[dict]):
        """Set the dummy courses to be injected as blocked time slots."""
        self._injected_constraints = self.time_constraints_service.generate_busy_slots(constraints)

    def clear_time_constraints(self):
        """Clear any previously set time constraints (remove dummy courses)."""
        self._injected_constraints = []
