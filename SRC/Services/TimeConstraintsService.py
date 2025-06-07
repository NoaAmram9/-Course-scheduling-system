from SRC.Models.Course import Course
from SRC.Models.Lesson import Lesson
from SRC.Models.LessonTimes import LessonTimes

class TimeConstraintsService:
    def __init__(self):
        self.block_counter = 1  # To assign unique dummy course codes

    def generate_busy_slots(self, constraints: list[dict]) -> list[Course]:
        """
        Create dummy Course objects that block given time ranges.
        Each constraint is a dict like {"day": 2, "start": 10, "end": 12}
        """
        busy_courses = []
        


        for constraint in constraints:
            day = constraint["day"]
            start = constraint["start"]
            end = constraint["end"]

            # Create a dummy LessonTimes and Lesson
            time = LessonTimes(start_hour=start, end_hour=end, day=day)
            dummy_lesson = Lesson(
                time=time,
                lesson_type="Blocked",      # Use valid type expected by generator
                building="",
                room="",
                instructors=[],
                creditPoints=0,
                weeklyHours=0,
                groupCode=0
            )

            dummy_course = Course(
                name = "Unavailable Time",
                code=f"BLOCKED_{self.block_counter}",
                semester=0,
                lectures=[dummy_lesson],
                exercises=[dummy_lesson],
                notes="User-defined time block"
            )

            busy_courses.append(dummy_course)
            self.block_counter += 1

        return busy_courses
