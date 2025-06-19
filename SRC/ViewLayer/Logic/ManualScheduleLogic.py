from SRC.ViewLayer.Logic.TimeTable import map_courses_to_slots

class ManualScheduleLogic:
    def __init__(self, controller, file_path):
        self.controller = controller
        self.file_path = file_path
        # self.blocked_slots = 0
        self.courses_info = self.get_selected_courses_info()
        self.all_lessons_slot_map = self.get_available_lessons_slot_map()
        self.occupied_windows = self.get_occupied_windows()


    def handle_lesson_type_click(self, course_id, lesson_type):
        print(f"Lesson type clicked: course_id={course_id}, type={lesson_type}")
       
    def handle_course_click(self, course_id):
        print(f"Course clicked: {course_id}")
    
    def get_selected_courses_info(self):
        """Retrieve selected courses information from the controller."""
        return self.controller.get_selected_courses_limited_info(self.file_path, "Data/selected_courses.txt")
    
    def get_available_lessons_slot_map(self):
        slot_map = self.controller.get_available_lessons()
        return slot_map
    
    def get_occupied_windows(self):
        occupied_windows = {}
        for (day, hour), lessons in self.all_lessons_slot_map.items():
            occupied_windows[(day, hour)] = {"name": " ", "code": " ",
                                             "type": "available", "location": " "}
        return occupied_windows
        
    
    def get_available_lessons_by_course(self, course_id, lesson_type):
        """Retrieve available courses based on course ID and lesson type."""
        return self.controller.get_available_lessons_by_course(course_id, lesson_type)

    def save_schedule(self):
        """Save the current schedule to a file."""
        # self.controller.save_schedule(self.file_path, self.slot_map)
        print(f"Schedule saved ")
    
    def undo_last_action(self):
        """Undo the last action in the schedule."""
        # self.controller.undo_last_action(self.file_path)
        print("Logic: Last action undone")
    
    def is_schedule_empty(self):
        """Check if the current schedule is empty."""
        return len(self.slot_map) == self.blocked_slots
    