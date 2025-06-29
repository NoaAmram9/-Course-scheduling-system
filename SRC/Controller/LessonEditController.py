# SRC/Controllers/LessonEditController.py

class LessonEditController:
    def __init__(self, timetable, lesson_edit_service):
        self.timetable = timetable
        self.lesson_edit_service = lesson_edit_service

    def get_alternatives(self, course_code, selected_lesson):
        return self.lesson_edit_service.get_alternative_lessons(course_code, selected_lesson)
    
    def replace_lesson(self, old_lesson, new_lesson):
        success = self.lesson_edit_service.replace_lesson(self.timetable, old_lesson, new_lesson)
        if success:
            # עדכון המטריקות מחדש
            from SRC.Services.TimetableMetricsService import TimetableMetricsService
            TimetableMetricsService().generate_metrics(self.timetable)
        return success
