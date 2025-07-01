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
            "Lecture": "_lectures",
            "Exercise": "_exercises",
            "Lab": "_labs",
            "Department hours": "_departmentHours",
            "Reinforcement": "_reinforcement",
            "Training": "_training",
        }
    
    def get_dynamic_schedule(self):
        """
        Returns the current schedule as a list of tuples (course_id, lesson).
        This is used to get the current schedule from the controller.
        """
        return self.schedule

    def extract_courses_with_required_lessons(self):
        """
        Returns a list of dictionaries where each dict represents a course and includes:
        - course_name
        - course_id
        - available_lesson_types: list of non-empty lesson type names
        - lessons: list of lessons for each type
        """

        result = []
        for course_id, course in self.repository.items():
            required_lesson_type = []
            lesson_options = {}

            for display_name, attr_name in self.lesson_type_map.items():
                lessons = getattr(course, attr_name, []) or []
                if lessons:
                    required_lesson_type.append(display_name)
                    lesson_options[display_name] = lessons

            result.append({
                "course_name": getattr(course, "name", "Unknown"),
                "course_id": getattr(course, "code", None),
                "required_lessons": required_lesson_type,
                "lessons": lesson_options # Store lessons for each type
            })

        return result
    
    def extract_available_lessons_by_course(self, course_id, lesson_type):
        """
        Returns a list of available lessons for a given course ID and lesson type.
        """
        # for course_code, course in self.repository.items():
        #     if course.code == course_id:
        #         attr_name = self.lesson_type_map.get(lesson_type)
        #         lessons = getattr(course, attr_name, []) or []
        #         return self.prevent_collision(lessons)
        # return None
        
        all_courses = self.extract_courses_with_required_lessons()
        lessons = []
        for course in all_courses:
            if course['course_id'] == course_id:
                lessons = course['lessons'].get(lesson_type, [])
                break
                # return lessons if lessons else []
        slot_map = {}
        for lesson in lessons:
            day = DAYS[lesson.time.day - 1]
            start = lesson.time.start_hour
            end = lesson.time.end_hour

            for hour in range(start, end):
                # slot_map[(day, hour)] = lesson
                # lesson.course_id = course_id  # Attach course_id for reverse mapping
                slot_map[(day, hour)] = {
                    "lesson": lesson,
                    "course_id": course_id
                }
        return slot_map
                
        # return []  # Return empty list if no lessons found for the course and type

    def extract_all_available_lessons(self, force_include_lesson_type=False):
        self.slot_map = defaultdict(list)  # Initialize an empty slot map
        
        for course_id, course in self.repository.items():
            for lesson_type, attr_name in self.lesson_type_map.items():
                # Check if this lesson type has already been added to the schedule for this course
                # If it has, skip adding available slots for this type
                if self.is_lesson_type_taken(course_id, lesson_type) and not force_include_lesson_type:
                    continue  # skip adding available slots for this type
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
                                "lesson": lesson,
                                "type": lesson_type,
                                "location": f"{lesson.building}-{lesson.room}",
                                "teachers": lesson.instructors,
                            })
                        
                        # # Store lessons in the slot map by day and start_hour
                        # key = (lesson.time.day, lesson.time.start_hour)
                        # self.slot_map[key].append({
                        #     "course_name": course.name,
                        #     "course_id": course.code,
                        #     "lesson": lesson
                        # })
        
        #  # Print the slot map in a nicely formatted way
        # for (day, hour), lessons in self.slot_map.items():
        #     print(f"Day: {day}, Hour: {hour}")
        #     for lesson in lessons:
        #         print(f"  - Name: {lesson['name']}, Code: {lesson['code']}, "
        #             f"Type: {lesson['type']}, Location: {lesson['location']}")
        
        return self.slot_map
    
    def get_occupied_windows(self, received_course_id=None, lesson_type=None):
        """
        Returns a dictionary of occupied time slots in the schedule.
        Each key is a tuple (day, hour) and value is a lesson (available of fixed) scheduled at that time.
        """
        occupied_windows = defaultdict(list)
        # available_lessons = self.extract_all_available_lessons()  # Get all available lessons as a map
        
        available_lessons = self.extract_all_available_lessons()
            # force_include_lesson_type=bool(received_course_id and lesson_type))
        
        for (day, hour), lessons in available_lessons.items():
            matches_requested_lesson = False
            # If one of the lessons at this time slot belongs to the user's requested lessons (by course and type), mark this time slot as a requested
            # for lesson in lessons:
            #     if lesson.get("code", "") == received_course_id:
            #         if lesson.get("lesson") in available_lessons_by_course:
            #             matches_requested_lesson = True
            occupied_windows[(day, hour)] = {"name": " ", "code": " ",
                                             "type": "available", "location": " ", "matches requested lesson": matches_requested_lesson,
                                             "lessons": lessons}
        
        # Populate occupied windows with lessons from the schedule - the real lessons run over the optional ones
        for course_id, lesson in self.schedule:
            day = DAYS[lesson.time.day - 1]
            start = lesson.time.start_hour
            end = lesson.time.end_hour
            
            matches_requested_lesson = False
        
            # if course_id == received_course_id:
            #     if lesson in available_lessons_by_course:
            #         matches_requested_lesson = True
                    
            for course_code, course in self.repository.items():
                if course_code == course_id:
                    course_name = course.name
                    break
                
            for hour in range(start, end):
                occupied_windows[(day, hour)] = {
                    "name": course_name,
                    "code": course_id,
                    "lesson": lesson,
                    "type": lesson.lesson_type.capitalize(),
                    "location": f"{lesson.building}-{lesson.room}",
                    "teachers": lesson.instructors,
                    "matches requested lesson": matches_requested_lesson,
                }
        if received_course_id and lesson_type:
            available_lessons_by_course = self.extract_available_lessons_by_course(received_course_id, lesson_type) # Tuple: (course_id,list of lessons)
            for (day,hour) in available_lessons_by_course:
                if occupied_windows[(day, hour)]:
                    occupied_windows[(day, hour)]["matches requested lesson"] = True
                else:
                    occupied_windows[(day, hour)] = {"name": " ", "code": " ",
                                             "type": "available", "location": " ", "matches requested lesson": True,
                                             "lessons": []}
            
        # for (day,hour) in occupied_windows:
        #     # print(f"time slot NOT marked: {day, hour}")
        #     if occupied_windows[(day, hour)].get("matches requested lesson", ""):
        #         print(f"time slot marked: {day, hour}")
        return occupied_windows
    
    def get_available_lessons_by_time(self, day, hour):
        all_lessons = self.extract_all_available_lessons()
        return all_lessons.get((day, hour), []) if (day, hour) in all_lessons else []
    
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
        removed_conflicts = []
        for cid, scheduled_lesson in self.schedule[:]:
            if cid == course_id and scheduled_lesson.lesson_type == lesson.lesson_type:
                self.schedule.remove((cid, scheduled_lesson))
                removed_conflicts.append((cid, scheduled_lesson))
        for existing_lesson in self.schedule[:]:
            _, scheduled = existing_lesson
            if self._lessons_overlap(lesson, scheduled):
                removed_conflicts.append(existing_lesson)
                self.schedule.remove(existing_lesson)
        self.schedule.append((course_id, lesson))
        if len(self.undo_stack) >= self.MAX_UNDO_STACK_SIZE:
            self.undo_stack.pop(0)
        self.undo_stack.append({
            "action": "add",
            "added": (course_id, lesson),
            "removed": removed_conflicts
        })

    def remove_lesson_from_schedule(self, course_id, lesson):
        """
        Removes a lesson from the schedule and logs the removal for undo.
        """
        if (course_id, lesson) not in self.schedule:
            return

        self.schedule.remove((course_id, lesson))

        if len(self.undo_stack) >= self.MAX_UNDO_STACK_SIZE:
            self.undo_stack.pop(0)

        self.undo_stack.append({
            "action": "remove",
            "removed": [(course_id, lesson)]
        })

    def undo_last_action(self):
        """
        Undoes the last action, restoring removed lessons or removing added ones.
        """
        if not self.undo_stack:
            return

        last_action = self.undo_stack.pop()

        if last_action["action"] == "add":
            if last_action["added"] in self.schedule:
                self.schedule.remove(last_action["added"])
            self.schedule.extend(last_action["removed"])

        elif last_action["action"] == "remove":
            self.schedule.extend(last_action["removed"])

    def reset_schedule(self):
        self.schedule = []

    def _lessons_overlap(self, l1, l2):
        """
        Returns True if l1 and l2 overlap (even partitial overlaping) in time on the same day.
        """
        return l1.time.day == l2.time.day and not (
            l1.time.end_hour <= l2.time.start_hour or
            l1.time.start_hour >= l2.time.end_hour
        )

    def create_schedule(self):
        """
        Creates a timetable object based on the lessons added to the schedule.
        Returns the final schedule.
        """
        # שלב 1: קיבוץ לפי קוד קורס וסוג שיעור
        grouped_lessons = defaultdict(lambda: defaultdict(list))  
        for course_id, lesson in self.schedule:
            grouped_lessons[course_id][lesson.lesson_type].append(lesson)
            # print(f"Adding lesson {lesson.lesson_type} for course {course_id} to grouped lessons.")

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
                lectures=lessons_by_type.get("lecture", []),
                exercises=lessons_by_type.get("exercise", []),
                labs=lessons_by_type.get("lab", []),
                departmentHours=lessons_by_type.get("departmentHours", []),
                reinforcement=lessons_by_type.get("reinforcement", []),
                training=lessons_by_type.get("training", []),
                notes=course_data._notes
            )
            result_courses.append(new_course)

        timetable = TimeTable(result_courses)
        metricsService = TimetableMetricsService()
        metricsService.generate_metrics(timetable)  # Generate metrics for the timetable
        return timetable

    def is_lesson_type_taken(self, course_id, lesson_type):
        """
        Returns True if a lesson of this type was already selected for this course.
        """
        for cid, lesson in self.schedule:
            if cid == course_id and lesson.lesson_type.capitalize() == lesson_type:
                return True
        return False

    # def add_lesson_to_schedule(self, course_id, lesson):
    #     """
    #     Adds a lesson to the schedule, removes conflicting lessons, and pushes both to the undo stack.
    #     """
    #     removed_conflicts = [] # List to keep track of removed conflicting lessons
    #     for existing_lesson in self.schedule[:]: # Copy the current schedule to avoid modifying it while iterating
    #         _, scheduled = existing_lesson
    #         if self._lessons_overlap(lesson, scheduled):
    #             removed_conflicts.append(existing_lesson)
    #             self.schedule.remove(existing_lesson) # Remove the conflicting lesson from the schedule

    #     self.schedule.append((course_id, lesson))

    #     if len(self.undo_stack) >= self.MAX_UNDO_STACK_SIZE:
    #         self.undo_stack.pop(0) # Remove the oldest action if stack is full

    #     self.undo_stack.append({
    #         "action": "add",
    #         "added": (course_id, lesson),
    #         "removed": removed_conflicts # a list of removed conflicting lessons in format: (course_id, lesson)
    #     })