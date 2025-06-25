from SRC.ViewLayer.Logic.TimeTable import map_courses_to_slots
from SRC.Controller.ManualScheduleController import ManualScheduleController

class ManualScheduleLogic:
    def __init__(self, controller, file_path):
        self.courses_repo = controller.get_selected_courses_info(file_path, "Data/selected_courses.txt")
        self.controller = ManualScheduleController(self.courses_repo)  # Initialize the controller with the courses repository
        self.file_path = file_path
        self.limited_courses_info = self.get_selected_courses_info() # limited course information for list of courses and thier requierd lessons
        self.all_lessons_slot_map = self.get_available_lessons_slot_map() # all available lessons slot map. each slot has a list of lessons available in that slot
        self.occupied_windows = self.get_occupied_windows() # map of (day,hour) and lesson information for occupied slots - this is used to display the timetable

    def handle_lesson_type_click(self, course_id, lesson_type):
        print(f"Lesson type clicked: course_id={course_id}, type={lesson_type}")
        # self.occupied_windows = self.controller.get_available_lessons_by_course(course_id, lesson_type)
        # self.update_view()
        self.occupied_windows = self.controller.get_occupied_windows(course_id, lesson_type)
       
    def handle_course_click(self, course_id):
        print(f"Course clicked: {course_id}")
    
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
    
    def save_schedule(self):
        """Save the current schedule to a file."""
        self.controller.save_schedule()
        print(f"Schedule saved ")
    
    def undo_last_action(self):
        """Undo the last action in the schedule."""
        self.controller.undo_last_action()
        print("Logic: Last action undone")
        self.update_view()
    
    def reset(self):
        self.controller.reset_schedule()
        self.update_view()
    
    def update_view(self):
        """Update the view with the current schedule."""
        self.occupied_windows = self.get_occupied_windows()
        
    