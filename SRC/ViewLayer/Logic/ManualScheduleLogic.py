from SRC.ViewLayer.Logic.TimeTable import map_courses_to_slots
from SRC.Controller.ManualScheduleController import ManualScheduleController

class ManualScheduleLogic:
    def __init__(self, controller, file_path, courses_data):
        self.courses_repo = controller.get_selected_courses_info(file_path, "Data/selected_courses.txt", courses_data)
        self.controller = ManualScheduleController(self.courses_repo)  # Initialize the controller with the courses repository
        self.file_path = file_path
        self.limited_courses_info = self.get_selected_courses_info() # limited course information for list of courses and thier requierd lessons
        self.all_lessons_slot_map = self.get_available_lessons_slot_map() # all available lessons slot map. each slot has a list of lessons available in that slot
        self.occupied_windows = self.get_occupied_windows() # map of (day,hour) and lesson information for occupied slots - this is used to display the timetable
        self.focused_lessons_by_slot = {}  # (day, hour) -> lesson dict
        self.focused_course_id = None
        self.focused_lesson_type = None


    def handle_lesson_type_click(self, course_id, lesson_type):
        # print(f"Lesson type clicked: course_id={course_id}, type={lesson_type}")
        # # self.occupied_windows = self.controller.get_available_lessons_by_course(course_id, lesson_type)
        # # self.update_view()
        # # self.occupied_windows = self.controller.get_occupied_windows(course_id, lesson_type)
        # self.occupied_windows = self.controller.get_occupied_windows(course_id, lesson_type)
        # # self.focused_lessons_by_slot = self.controller.get_available_lessons_by_course(course_id, lesson_type)
        # self.focused_lessons_by_slot = {
        #     slot: data["lesson"] for slot, data in self.controller.get_available_lessons_by_course(course_id, lesson_type).items()
        # }
        if self.focused_course_id == course_id and self.focused_lesson_type == lesson_type:
            self.clear_lesson_type_focus()
            return        
        # עדכון המצב (focus)
        self.focused_course_id = course_id
        self.focused_lesson_type = lesson_type

        # חישוב החלונות המסומנים לממשק
        self.occupied_windows = self.controller.get_occupied_windows(course_id, lesson_type)
        
        self.focused_lessons_by_slot = self.controller.get_available_lessons_by_course(course_id, lesson_type)
       
    def handle_course_click(self, course_id):
        pass
        # print(f"Course clicked: {course_id}")
    
    def handle_lesson_click(self, course_id, lesson):
        self.controller.remove_lesson_from_schedule(course_id, lesson)
        self.update_view()
    
    def get_selected_courses_info(self):
        # """Retrieve selected courses information from the controller."""
        # limited_courses_info = self.controller.get_selected_courses_limited_info(self.file_path, "Data/selected_courses.txt")
        # for course in limited_courses_info:
        #     course['in_schedule'] = False  # Initialize 'added' attribute for each course
        # return limited_courses_info
        return self.controller.get_selected_courses_limited_info()
        
    def get_available_lessons_slot_map(self):
        slot_map = self.controller.get_available_lessons()
        return slot_map
    
    def get_occupied_windows(self):
        return self.controller.get_occupied_windows()
        
    def get_available_lessons_by_time(self, day, hour):
        return self.controller.get_available_lessons_by_time(day, hour)
        # return self.all_lessons_slot_map[(day, hour)] if (day, hour) in self.all_lessons_slot_map else {}
    
    def get_available_lessons_by_course(self, course_id, lesson_type):
        """Retrieve available courses based on course ID and lesson type."""
        return self.controller.get_available_lessons_by_course(course_id, lesson_type)

    def add_lesson_to_schedule(self, day, hour, course_id, lesson):
        self.controller.add_lesson_to_schedule(course_id = course_id ,lesson = lesson)
        self.update_view()
    
    def get_dynamic_schedule(self):
       return self.controller.get_dynamic_schedule()
    
    def save_schedule(self):
        if not len(self.get_dynamic_schedule()) == self.count_total_required_lessons():
            print("sorry, no can do yet")
            return {}
        else:
            timetable = self.controller.save_schedule()
            print(f"Schedule saved {timetable}")
            return timetable
    
    def undo_last_action(self):
        """Undo the last action in the schedule."""
        self.controller.undo_last_action()
        # print("Logic: Last action undone")
        self.update_view()
    
    def reset(self):
        self.controller.reset_schedule()
        self.update_view()
    
    def update_view(self):
        """Update the view with the current schedule."""
        self.occupied_windows = self.get_occupied_windows()
    
    def has_focus(self):
        return self.focused_course_id is not None and self.focused_lesson_type is not None

      
    def clear_lesson_type_focus(self):
        self.focused_course_id = None
        self.focused_lesson_type = None
        self.occupied_windows = self.controller.get_occupied_windows()
        self.focused_lessons_by_slot = {}
        
    def count_total_required_lessons(self):
        """Calculate total number of required lesson types across all courses."""
        courses_info = self.limited_courses_info
        return sum(len(course["required_lessons"]) for course in courses_info)

    def get_schedule_progress(self):
        selected = self.get_dynamic_schedule()
        selected_count = len(selected)
        total_required = self.count_total_required_lessons()
        return selected_count, total_required

    
    def move_to_next_page(self, timetable):
        print("moved")
        self.show_timetables_page(timetable)
    
    def show_timetables_page(self, timetable, instance):
        """Show the timetables page"""
        # Import the PyQt5 timetables page
        from SRC.ViewLayer.View.Timetables_qt5 import TimetablesPageQt5
        
        # Create callback function to return to course selection
        def go_back_to_selection():
            if self.timetables_window:
                self.timetables_window.close()
                self.timetables_window = None
            instance.show()  # Show the course selection window again
        
        # Hide the current window
        instance.hide()
        
        # # Create the timetables window
        # self.timetables_window = TimetablesPageQt5(
        #     go_back_callback=go_back_to_selection,
        #     timetable=timetable
        # )
        
        # # Show the timetables window
        # self.timetables_window.show()  
    