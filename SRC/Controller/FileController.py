from SRC.Services.ExcelManager import ExcelManager
from SRC.Services.TxtManager import TxtManager
from SRC.Interfaces.FileManager import FileManager
from SRC.Services.ScheduleService import ScheduleService
from SRC.Services.TimeConstraintsService import TimeConstraintsService
from SRC.Services.ExcelExportManager import ExcelExportManager
from SRC.DataBase.DataBaseManager import DatabaseManager 

class FileController:
    def __init__(self, file_type: str, filePath: str = None, use_database: bool = True):
        self.filePath = filePath
        self.file_type = file_type  # הוספתי את השורה הזו שחסרה
        self.use_database = use_database
        
        # Initialize database if requested
        if self.use_database:
            self.db_manager = DatabaseManager()
        
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
        """
        Read courses from file and optionally import to database
        """
        courses_data = self.file_manager.read_courses_from_file(file_path)
        
        # אם יש בסיס נתונים, נייבא את הקורסים
        if self.use_database and courses_data:
            courses_list = courses_data[0] if isinstance(courses_data, tuple) else courses_data
            if courses_list:
                imported_count, errors = self.db_manager.import_courses_from_list(courses_list)
                print(f"Imported {imported_count} courses to database")
                if errors:
                    print(f"Encountered {len(errors)} errors during import")
        
        return courses_data

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
        **שומר על הפרמטרים המקוריים בדיוק**
        """
        # אם יש דאטהבייס ולא נשלח file_path1, נשתמש בדאטהבייס
        if self.use_database and file_path1 is None:
            courses_info = self.get_courses_from_database()
        else:
            # אם נשלח file_path1 או שאין דאטהבייס, נשתמש בקובץ
            if file_path1 is None:
                raise ValueError("file_path1 is required when not using database")
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

    def save_courses_to_file(self, file_path: str, courses: list):
        """
        Save the courses to a file.
        This method will save the courses to the specified file path.
        """
        export_manager = ExcelExportManager()
        # ייצוא בסיסי
        export_manager.export_courses_to_excel(courses, file_path)
    
    def handle_exit(self):
        """
        Handle the exit of the application.
        This method is called when the application is about to exit.
        delete the temporary files
        """
        # file_path1 = self.filePath
        # file_path2 = "Data/courses.xlsx"
        # file_path2 = "Data/selected_courses.txt"
        files = ["Data/courses.xlsx", "Data/selected_courses.txt"]
        if self.filePath:
            files.append(self.filePath)
        dataManager = FileManager()
        dataManager.delete_temp_files(files)

    def apply_time_constraints(self, constraints: list[dict]):
        """Set the dummy courses to be injected as blocked time slots."""
        self._injected_constraints = self.time_constraints_service.generate_busy_slots(constraints)

    def clear_time_constraints(self):
        """Clear any previously set time constraints (remove dummy courses)."""
        self._injected_constraints = []

    # === פונקציות דאטהבייס נוספות (לא משנות את הפונקציונליות המקורית) ===
    
    def get_courses_from_database(self, semester: int = None, search_term: str = None):
        """
        Get courses from database with optional filtering
        """
        if not self.use_database:
            raise ValueError("Database is not enabled for this controller")
        
        if semester:
            return self.db_manager.get_courses_by_semester(semester)
        elif search_term:
            return self.db_manager.search_courses(search_term)
        else:
            return self.db_manager.get_all_courses()

    def clear_database(self):
        """Clear all data from database"""
        if not self.use_database:
            raise ValueError("Database is not enabled")
        print("Clearing database...")
        return self.db_manager.clear_all_data()
    
    def get_database_stats(self):
        """Get database statistics"""
        if not self.use_database:
            raise ValueError("Database is not enabled")
        return self.db_manager.get_database_stats()
  
    def delete_course_from_database(self, course_code: str, course_name: str = None):
        """Delete course from database"""
        if not self.use_database:
            raise ValueError("Database is not enabled")
        return self.db_manager.delete_course(course_code, course_name)
    
    def search_courses_in_database(self, search_term: str):
        """Search courses in database"""
        if not self.use_database:
            raise ValueError("Database is not enabled")
        return self.db_manager.search_courses(search_term)
    
    
    
    
    
    
    
    
    
    
    
    
    
# OLD CODE - Uncomment if needed
    
#     from SRC.Services.ExcelManager import ExcelManager
# from SRC.Services.TxtManager import TxtManager
# from SRC.Interfaces.FileManager import FileManager
# from SRC.Services.ScheduleService import ScheduleService
# from SRC.Services.TimeConstraintsService import TimeConstraintsService
# from SRC.Services.ExcelExportManager import ExcelExportManager

# class FileController:
#     def __init__(self, file_type: str, filePath: str = None):
#         self.filePath = filePath
#         if file_type == ".xlsx" or file_type == ".xls":
#             self.file_manager = ExcelManager()
#         elif file_type == ".txt":
#             self.file_manager = TxtManager()
#         else:
#             raise ValueError("Unsupported file type. Use 'excel' or 'txt'.")
#         self.time_constraints_service = TimeConstraintsService()
#         self._injected_constraints = []



#     def get_file_type(self) -> str:
#         return self.file_type

#     def read_courses_from_file(self, file_path: str):
#         return self.file_manager.read_courses_from_file(file_path)

#     def write_courses(self, file_path: str, courses):
#         self.file_manager.write_courses_to_file(file_path, courses)
       
#      # Function to get the selected courses from the user    
#     def get_selected_courses(self, file_path):
#         dataManager = FileManager()
#         return dataManager.read_course_numbers_from_file(file_path)   
#     # Function to get the selected courses info from the repository
#     def selected_courses_info(self, courses_info, selected_courses):
#         selected_courses_info = []
#         for course in courses_info:
#             if course.code in selected_courses:
#                 selected_courses_info.append(course)
#         return selected_courses_info
    
#     # Function to create the schedual from selected courses file
#     def create_selected_courses_file(self, selected_courses, file_path):
#         dataManager = FileManager()
#         dataManager.write_course_numbers_to_file(file_path, selected_courses)
      
        
#     # Function to create the schedules based on the selected courses
#     def create_schedules(self, selected_courses):
        
#         scheduleService = ScheduleService()
#         return scheduleService.generate_schedules(selected_courses, limit=1000)
  

#     def get_all_options(self, file_path1, file_path2, batch_size=100):
#         """
#         Returns batches of timetables instead of individual timetables
#         This replaces the old method that returned individual timetables
#         """

#         courses_info = self.read_courses_from_file(file_path1)[0]  # Get the first element which is the courses info
#         selected_courses = self.get_selected_courses(file_path2)
#         selected_courses_info = self.selected_courses_info(courses_info, selected_courses)
        
#         # Optional: Include dummy blocked courses if added earlier
#         if hasattr(self, "_injected_constraints"):
#             selected_courses_info.extend(self._injected_constraints)


#         try:
#             schedule_service = ScheduleService()
            
#             # Get the progressive generator (no limit)
#             schedule_generator = schedule_service.generate_schedules_progressive(
#                 selected_courses_info,  
#                 limit=None # No limit, to get all possible schedules
#             )
            
#             # Collect into batches
#             batch = []
#             for timetable in schedule_generator:
#                 batch.append(timetable)
                
#                 # When batch is full, yield it
#                 if len(batch) >= batch_size:
#                     yield batch
#                     batch = []  # Reset for next batch
                    
#             # Yield final batch if it has any items
#             if batch:
#                 yield batch
                            
#         except Exception as e:
#             print(f"Error in batch generator: {str(e)}")
#             return []  # החזר רשימה ריקה במקום 

#     def save_courses_to_file(self, file_path: str, courses : list):
#         """
#         Save the courses to a file.
#         This method will save the courses to the specified file path.
#         """
#         export_manager = ExcelExportManager()
#         # ייצוא בסיסי
#         export_manager.export_courses_to_excel(courses, file_path)
    
       
#     def handle_exit(self):
#         """
#         Handle the exit of the application.
#         This method is called when the application is about to exit.
#         delete the temporary files
        
#         """
#         # file_path1 = self.filePath
#         # file_path2 = "Data/courses.xlsx"
#         # file_path2 = "Data/selected_courses.txt"
#         files = ["Data/courses.xlsx", "Data/selected_courses.txt", self.filePath]
#         dataManager = FileManager()
#         dataManager.delete_temp_files(files)

#     def apply_time_constraints(self, constraints: list[dict]):
#         """Set the dummy courses to be injected as blocked time slots."""
#         self._injected_constraints = self.time_constraints_service.generate_busy_slots(constraints)

#     def clear_time_constraints(self):
#         """Clear any previously set time constraints (remove dummy courses)."""
#         self._injected_constraints = []
