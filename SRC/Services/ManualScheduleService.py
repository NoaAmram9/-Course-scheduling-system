from collections import defaultdict
from SRC.Models.Course import Course
from SRC.Models.TimeTable import TimeTable
from SRC.Services.TimetableMetricsService import TimetableMetricsService

 
DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
HOURS = list(range(8, 22))  # 8:00 to 21:00

class ManualScheduleService:
    """
    Service for managing manual schedules.
    """
    MAX_UNDO_STACK_SIZE = 15  # Maximum size of the undo stack
            
    def __init__(self, repository):
        self.repository = {course.code: course for course in repository}
        self.schedule = [] # Initialize an empty schedule - this will hold the lessons added to the schedule
        self.undo_stack = [] # Initialize an empty undo stack
        self.lesson_type_map = {
            "lecture": "_lectures",
            "exercise": "_exercises",
            "lab": "_labs",
            "department hours": "_departmentHours",
            "reinforcement": "_reinforcement",
            "training": "_training",
        }

    def extract_courses_with_required_lessons(self):
        """
        Returns a list of dictionaries where each dict represents a course and includes:
        - course_name
        - course_id
        - available_lesson_types: list of non-empty lesson type names
        """

        result = []
        for course_id, course in self.repository.items():
            required_lessons = []

            for display_name, attr_name in self.lesson_type_map.items():
                lessons = getattr(course, attr_name, []) or []
                if lessons:
                    required_lessons.append(display_name)

            result.append({
                "course_name": getattr(course, "name", "Unknown"),
                "course_id": getattr(course, "code", None),
                "required_lessons": required_lessons
            })

        return result
    
    def extract_available_lessons_by_course(self, course_id, lesson_type):
        """
        Returns a list of available lessons for a given course ID and lesson type.
        """
        for course_code, course in self.repository.items():
            if course.code == course_id:
                attr_name = self.lesson_type_map.get(lesson_type)
                lessons = getattr(course, attr_name, []) or []
                return self.prevent_collision(lessons)
        return None

    def extract_all_available_lessons(self):
        self.slot_map = defaultdict(list)  # Initialize an empty slot map
        
        for course_id, course in self.repository.items():
            for lesson_type, attr_name in self.lesson_type_map.items():
                lessons = getattr(course, attr_name, [])
                if lessons:
                    for lesson in lessons:
                        day = DAYS[lesson.time.day - 1]
                        start = lesson.time.start_hour
                        end = lesson.time.end_hour

                        for hour in range(start, end):
                            self.slot_map[(day, hour)].append({
                                "name": course.name,
                                "code": course.code,
                                "type": lesson_type,
                                "location": f"{lesson.building}-{lesson.room}"
                            })
                        
                        # # Store lessons in the slot map by day and start_hour
                        # key = (lesson.time.day, lesson.time.start_hour)
                        # self.slot_map[key].append({
                        #     "course_name": course.name,
                        #     "course_id": course.code,
                        #     "lesson": lesson
                        # })
        
         # Print the slot map in a nicely formatted way
        for (day, hour), lessons in self.slot_map.items():
            print(f"Day: {day}, Hour: {hour}")
            for lesson in lessons:
                print(f"  - Name: {lesson['name']}, Code: {lesson['code']}, "
                    f"Type: {lesson['type']}, Location: {lesson['location']}")
        
        return self.slot_map

    def prevent_collision(self, lessons):
        """
        Filters out lessons that collide with already selected lessons in the schedule.
        Returns a list of non-colliding lessons.
        """
        non_colliding = []

        for lesson in lessons:
            collides = False
            for _, selected_lesson in self.schedule:
                if lesson.time.day != selected_lesson.time.day:
                    continue  # different day, no collision

                if not (lesson.time.end_hour <= selected_lesson.time.start_hour or
                        lesson.time.start_hour >= selected_lesson.time.end_hour):
                    # Overlap in time on same day
                    collides = True
                    break
            
            if not collides:
                non_colliding.append(lesson)

        return non_colliding
    
    def add_lesson_to_schedule(self, course_id, lesson):
        """
        Adds a lesson to the schedule and manages the undo stack.
        """
        if len(self.undo_stack) >= self.MAX_UNDO_STACK_SIZE:
            self.undo_stack.pop(0) # Remove the oldest action if stack is full
        self.undo_stack.append((course_id, lesson)) # Add the lesson to the undo stack
        self.schedule.append((course_id, lesson)) # Add the lesson to the schedule
    
    def undo_last_action(self):
        """        
        Undoes the last action by removing the last lesson from the schedule and undo stack.
        """        
        if self.undo_stack:
            course_id, last_lesson = self.undo_stack.pop()
            self.schedule.remove((course_id, last_lesson))

    def create_schedule(self):
        """
        Creates a timetable object based on the lessons added to the schedule.
        Returns the final schedule.
        """
        # שלב 1: קיבוץ לפי קוד קורס וסוג שיעור
        grouped_lessons = defaultdict(lambda: defaultdict(list))  
        for course_id, lesson in self.schedule:
            grouped_lessons[course_id][lesson.lesson_type].append(lesson)

        result_courses = []
        # שלב 2: עבור כל קורס שבוצעה בו בחירה
        for course_id, lessons_by_type in grouped_lessons.items():
            # מצא את הקורס ברפוזיטורי
            course_data = self.repository[course_id]
            if not course_data:
                continue

            # בנה קורס חדש עם אותם פרטים אך רק עם השיעורים שנבחרו
            new_course = Course(
                name=course_data._name,
                code=course_data._code,
                semester=course_data._semester,
                lectures=lessons_by_type.get("lectures", []),
                exercises=lessons_by_type.get("exercises", []),
                labs=lessons_by_type.get("labs", []),
                departmentHours=lessons_by_type.get("department hours", []),
                reinforcement=lessons_by_type.get("reinforcement", []),
                training=lessons_by_type.get("training", []),
                notes=course_data._notes
            )
            result_courses.append(new_course)

        timetable = TimeTable(result_courses)
        metricsService = TimetableMetricsService()
        metricsService.generate_metrics(timetable)  # Generate metrics for the timetable
        return timetable















# def main():
#     """
#     Main function to demonstrate the usage of ManualScheduleService.
#     """
#     # Example repository with dummy data
#     class Course:
#         def __init__(self, code, name, lectures, exercises, labs, departmentHours, reinforcement, training):
#             self.code = code
#             self.name = name
#             self._lectures = lectures
#             self._exercises = exercises
#             self._labs = labs
#             self._departmentHours = departmentHours
#             self._reinforcement = reinforcement
#             self._training = training

#     repository = [
#         Course("CS101", "Computer Science 101", ["Lecture 1", "Lecture 2"], ["Exercise 1"], [], [], [], []),
#         Course("MATH101", "Mathematics 101", ["Lecture 1"], ["Exercise 1", "Exercise 2"], ["Lab 1"], [], [], []),
#     ]

#     service = ManualScheduleService(repository)
#     courses_info = service.extract_courses_with_required_lessons()
#     print(courses_info)
#     for course in courses_info:
#         lessons = service.extract_available_lessons_by_course(course['course_id'], 'lectures')
#         print(f"Course: {course['course_name']}, lessons: {lessons}")
    
# def main():
#     """
#     Test the ManualScheduleService using actual Lesson model structure.
#     """
#     # Create LessonTimes objects
#     time1 = LessonTimes(day=1, start_time="09:00", end_time="10:00")
#     time2 = LessonTimes(day=3, start_time="11:00", end_time="12:00")
#     time3 = LessonTimes(day=4, start_time="14:00", end_time="15:00")

#     # Create Lesson objects using your model
#     cs_lecture = Lesson(time=time1, lesson_type="lectures", building=1, room=101, instructors=["Dr. A"], creditPoints=3, weeklyHours=2.0, groupCode=1)
#     cs_exercise = Lesson(time=time2, lesson_type="exercises", building=1, room=102, instructors=["TA B"], creditPoints=1, weeklyHours=1.0, groupCode=2)
#     math_lab = Lesson(time=time3, lesson_type="labs", building=2, room=201, instructors=["Prof. C"], creditPoints=2, weeklyHours=1.5, groupCode=3)

#     # Create Course objects
#     course_cs = Course(code="CS101", name="Intro to CS", semester=1,
#                        lectures=[cs_lecture], exercises=[cs_exercise],
#                        labs=[], departmentHours=[], reinforcement=[], training=[])

#     course_math = Course(code="MATH101", name="Math Basics", semester=1,
#                          lectures=[], exercises=[], labs=[math_lab],
#                          departmentHours=[], reinforcement=[], training=[])

#     repository = [course_cs, course_math]
#     service = ManualScheduleService(repository)

#     print("== Courses and Available Lesson Types ==")
#     for course_info in service.extract_courses_with_required_lessons():
#         print(course_info)

#     # Simulate manual selections
#     service.add_lesson_to_schedule("CS101", cs_lecture)
#     service.add_lesson_to_schedule("CS101", cs_exercise)
#     service.add_lesson_to_schedule("MATH101", math_lab)

#     # Generate timetable
#     timetable = service.create_schedule()

#     print("\n== Final Schedule ==")
#     for course in timetable.courses:
#         print(f"\nCourse: {course._name} ({course._code})")
#         print(f"  Lectures: {[l.time.to_string() for l in course._lectures]}")
#         print(f"  Exercises: {[l.time.to_string() for l in course._exercises]}")
#         print(f"  Labs: {[l.time.to_string() for l in course._labs]}")
#         print(f"  Notes: {course._notes}")
            
# if __name__ == "__main__":
#     main()
