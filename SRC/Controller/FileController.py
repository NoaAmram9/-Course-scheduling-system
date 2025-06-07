from SRC.Services.ExcelManager import ExcelManager
from SRC.Services.TxtManager import TxtManager
from SRC.Interfaces.FileManager import FileManager
from SRC.Services.ScheduleService import ScheduleService
from SRC.Services.TimeConstraintsService import TimeConstraintsService

class FileController:
    def __init__(self, file_type: str):
        if file_type == ".xlsx" or file_type == ".xls":
            self.file_manager = ExcelManager()
        elif file_type == ".txt":
            self.file_manager = TxtManager()
        else:
            raise ValueError("Unsupported file type. Use 'excel' or 'txt'.")
        self.time_constraints_service = TimeConstraintsService()

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
    #DEBUGGGGGGG 
    
    # def get_all_options(self, file_path1, file_path2, batch_size=100):
    #     """
    #     Returns batches of timetables instead of individual timetables
    #     This replaces the old method that returned individual timetables
    #     """
    #     try:
    #         print("Starting get_all_options...")
    #         courses_info = self.read_courses_from_file(file_path1)
    #         print(f"Read {len(courses_info)} courses from file")
            
    #         selected_courses = self.get_selected_courses(file_path2)
    #         print(f"Selected {len(selected_courses)} courses")
            
    #         selected_courses_info = self.selected_courses_info(courses_info, selected_courses)
    #         print(f"Found {len(selected_courses_info)} matching courses")
            
    #         schedule_service = ScheduleService()
    #         print("Created ScheduleService")
            
    #         # Get the progressive generator (no limit)
    #         schedule_generator = schedule_service.generate_schedules_progressive(
    #             selected_courses_info,  
    #             limit=None # No limit, to get all possible schedules
    #         )
    #         print("Created schedule generator")
            
    #         # Collect into batches
    #         batch = []
    #         count = 0
            
    #         for timetable in schedule_generator:
    #             try:
    #                 batch.append(timetable)
    #                 count += 1
                    
    #                 if count % 100 == 0:  # Progress tracking
    #                     print(f"Processed {count} timetables")
                    
    #                 # When batch is full, yield it
    #                 if len(batch) >= batch_size:
    #                     print(f"Yielding batch of {len(batch)} timetables")
    #                     yield batch
    #                     batch = []  # Reset for next batch
                        
    #             except ZeroDivisionError as zde:
    #                 print(f"ZeroDivisionError at timetable {count}: {str(zde)}")
    #                 print(f"Timetable details: {timetable}")
    #                 raise zde
    #             except Exception as e:
    #                 print(f"Error processing timetable {count}: {str(e)}")
    #                 continue  # Skip this timetable and continue
                    
    #         # Yield final batch if it has any items
    #         if batch:
    #             print(f"Yielding final batch of {len(batch)} timetables")
    #             yield batch
                
    #         print(f"Completed processing {count} total timetables")
                            
    #     except ZeroDivisionError as zde:
    #         print(f"ZeroDivisionError in get_all_options: {str(zde)}")
    #         import traceback
    #         traceback.print_exc()
    #         return []
    #     except Exception as e:
    #         print(f"General error in get_all_options: {str(e)}")
    #         import traceback
    #         traceback.print_exc()
    #         return []

    def get_all_options(self, file_path1, file_path2, batch_size=100):
        """
        Returns batches of timetables instead of individual timetables
        This replaces the old method that returned individual timetables
        """
        print(">>> get_all_options called")
        
        courses_info = self.read_courses_from_file(file_path1)
        selected_courses = self.get_selected_courses(file_path2)
        selected_courses_info = self.selected_courses_info(courses_info, selected_courses)
        
        
        # STEP 1: Define time constraints (can be hardcoded or passed later)
        constraints = [
            {"day": 5, "start": 17, "end": 18},
        ]

        # STEP 2: Generate dummy courses for busy time blocks
        busy_slots = self.time_constraints_service.generate_busy_slots(constraints)

        # STEP 3: Inject them into selected_courses_info
        selected_courses_info.extend(busy_slots)

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
        file_path1 = "Data/selected_courses.txt"
        file_path2 = "Data/courses.xlsx"
        dataManager = FileManager()
        dataManager.delete_temp_files(file_path1, file_path2)

    