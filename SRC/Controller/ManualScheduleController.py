from SRC.Services.ManualScheduleService import ManualScheduleService
class ManualScheduleController:
    def __init__(self, courses_repo):
        self.courses_repo = courses_repo
        self.service = ManualScheduleService(self.courses_repo)
    
    # def get_dynamic_schedule(self):
    #     return self.service.get_dynamic_schedule()
    
    def get_selected_courses_limited_info(self):
        return self.service.extract_courses_with_required_lessons()
    
    def get_available_lessons(self):
        return self.service.extract_all_available_lessons()
    
    def get_available_lessons_by_course(self, course_id, lesson_type):
        return self.service.extract_available_lessons_by_course(course_id, lesson_type)
    
    def get_available_lessons_by_time(self, day, hour):
        return self.service.get_available_lessons_by_time(day, hour)
    
    def get_occupied_windows(self):
        return self.service.get_occupied_windows()
        
    def add_lesson_to_schedule(self, course_id, lesson):
        self.service.add_lesson_to_schedule(course_id, lesson)
    
    def reset_schedule(self):
        self.service.reset_schedule()
    
    def undo_last_action(self):
        self.service.undo_last_action()
    
    def save_schedule(self):
        self.service.create_schedule()