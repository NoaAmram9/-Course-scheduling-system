from itertools import product
from SRC.Interfaces.IScheduleService import IScheduleService
from SRC.Models.TimeTable import TimeTable
from SRC.Models.Course import Course
from SRC.Services.TimetableMetricsService import TimetableMetricsService

class ScheduleService(IScheduleService):
    def __init__(self):
        """Create a single instance of the preferences service"""
        self.timetable_metrics_service = TimetableMetricsService()
    
    def generate_schedules(self, courses: list, limit: int = 1000) -> list:
        """
        For small to medium-sized sets - returns a full list.
        Suitable when you need to know the number of results or access them multiple times.
        """
        schedules = []
        count = 0
        
        for timetable in self._generate_schedules_core(courses):
            schedules.append(timetable)
            count += 1
            if count >= limit:
                break
                
        return schedules

    def generate_schedules_progressive(self, courses: list, limit: int = None):
        """
        For large amounts - memory-efficient generator.
        Suitable for thousands/millions of possible combinations.
        """
        count = 0
        for timetable in self._generate_schedules_core(courses):
            yield timetable
            count += 1
            if limit is not None and count >= limit:
                break

    def _generate_schedules_core(self, courses: list):
        """
        Core logic - single function only!
        Always returns a generator to save memory.
        """
        # Filter courses that comply with the new rules
        valid_courses = self._filter_valid_courses(courses)
        if not valid_courses:
            return

        # Create all possible combinations for each course
        course_combinations = []
        for course in valid_courses:
            valid_combinations = self._get_valid_course_combinations(course)
            if not valid_combinations:
                continue
            course_combinations.append(valid_combinations)

        if not course_combinations:
            return

        # Call the single recursive function
        yield from self._build_valid_schedules_recursive(course_combinations, 0, [], [])

    def _filter_valid_courses(self, courses: list) -> list:
        """
        Filters courses that comply with the new rules:
        1. If there is a lecture - there must also be an exercise.
        2. Reinforcement requires both lecture and exercise.
        3. Training can only exist with reinforcement.
        4. departmentHours can exist alone.
        5. Lab can exist alone or with any other components.
        """
        valid_courses = []
        
        for course in courses:
            lectures = course._lectures or []
            exercises = course._exercises or []
            labs = course._labs or []
            departmentHours = getattr(course, "_departmentHours", None) or []
            reinforcement = getattr(course, "_reinforcement", None) or []
            training = getattr(course, "_training", None) or []
            
            has_lectures = len(lectures) > 0
            has_exercises = len(exercises) > 0
            has_reinforcement = len(reinforcement) > 0
            has_training = len(training) > 0
            
            # Validation rules:
            # If training exists without reinforcement, reject
            if has_training and not has_reinforcement:
                print(f"Course {course._name} rejected: training without reinforcement !!!!!!! {reinforcement} ")
                continue
            
            # At least one type of lesson must exist
            if not (has_lectures or has_exercises or len(labs) > 0 or len(departmentHours) > 0 or has_reinforcement or has_training):
                print(f"Course {course._name} rejected: no lessons")
                continue
            
            valid_courses.append(course)
        
        return valid_courses

    def _get_valid_course_combinations(self, course) -> list:
        """
        Creates valid lesson combinations for a single course.
        Rules:
        1. Lecture + Exercise: each lecture with each exercise.
        2. departmentHours can exist alone.
        3. Reinforcement requires lecture + exercise and optionally lab.
        4. Training only with reinforcement.
        5. Lab can be alone or with any other components.
        """
        lectures = course._lectures or []
        exercises = course._exercises or []
        labs = course._labs or []
        departmentHours = getattr(course, "_departmentHours", None) or []
        reinforcement = getattr(course, "_reinforcement", None) or []
        training = getattr(course, "_training", None) or []
        
        valid_combinations = []
        
        # Case 1: Lectures and exercises exist
        if lectures and exercises:
            for lec in lectures:
                for ex in exercises:
                    base_combo = (course._name, course._code, lec, ex, None, None, None, None)
                    valid_combinations.append(base_combo)
                    
                    for lab in labs:
                        combo_with_lab = (course._name, course._code, lec, ex, lab, None, None, None)
                        valid_combinations.append(combo_with_lab)
                    
                    for reinf in reinforcement:
                        combo_with_reinf = (course._name, course._code, lec, ex, None, None, reinf, None)
                        valid_combinations.append(combo_with_reinf)
                        
                        for lab in labs:
                            combo_reinf_lab = (course._name, course._code, lec, ex, lab, None, reinf, None)
                            valid_combinations.append(combo_reinf_lab)
                        
                        for train in training:
                            combo_reinf_train = (course._name, course._code, lec, ex, None, None, reinf, train)
                            valid_combinations.append(combo_reinf_train)
                            
                            for lab in labs:
                                combo_all = (course._name, course._code, lec, ex, lab, None, reinf, train)
                                valid_combinations.append(combo_all)
        
        # Case 2: Only labs (no lectures/exercises)
        if labs and not lectures and not exercises:
            for lab in labs:
                combo = (course._name, course._code, None, None, lab, None, None, None)
                valid_combinations.append(combo)
        
        # Case 3: Only departmentHours
        if departmentHours:
            for dept in departmentHours:
                combo = (course._name, course._code, None, None, None, dept, None, None)
                valid_combinations.append(combo)
        
        # Case 4: Only exercises and labs (no lecture)
        if exercises and labs and not lectures:
            for ex in exercises:
                for lab in labs:
                    combo = (course._name, course._code, None, ex, lab, None, None, None)
                    valid_combinations.append(combo)
        
        # Case 5: Exercises + departmentHours (no lecture or lab)
        if exercises and not lectures and not labs and departmentHours:
            for ex in exercises:
                for dept in departmentHours:
                    combo = (course._name, course._code, None, ex, None, dept, None, None)
                    valid_combinations.append(combo)
        
        # Case 6: Reinforcement + training only (no lecture/exercise)
        if reinforcement and training and not lectures and not exercises:
            for reinf in reinforcement:
                for train in training:
                    combo = (course._name, course._code, None, None, None, None, reinf, train)
                    valid_combinations.append(combo)
        
        return valid_combinations

    def _build_valid_schedules_recursive(self, combinations, index, current_courses, current_lessons):
        """
        The only recursive function that builds valid timetables.
        Returns a generator for memory efficiency.
        """
        if index == len(combinations):
            timetable = TimeTable(current_courses.copy())
            
            # *** The correct and only place to call preferences ***
            self.timetable_metrics_service.generate_metrics(timetable)
            
            yield timetable
            return

        for combo in combinations[index]:
            name, code, lec, ex, lab, dept, reinf, train = combo
            new_lessons = [l for l in (lec, ex, lab, dept, reinf, train) if l]

            # Check for time conflicts with current lessons
            if any(self._is_conflicting(l1, l2) for l1 in current_lessons for l2 in new_lessons):
                continue

            new_course = Course(
                name=name,
                code=code,
                lectures=[lec] if lec else [],
                exercises=[ex] if ex else [],
                labs=[lab] if lab else [],
                departmentHours=[dept] if dept else [],
                reinforcement=[reinf] if reinf else [],
                training=[train] if train else []
            )

            # Continue recursion
            yield from self._build_valid_schedules_recursive(
                combinations,
                index + 1,
                current_courses + [new_course],
                current_lessons + new_lessons
            )

    def _is_conflicting(self, lesson1, lesson2):
        """Check if two lessons conflict in time"""
        if not lesson1 or not lesson2:
            return False
            
        if not hasattr(lesson1, '_time') or not hasattr(lesson2, '_time'):
            return False
            
        if lesson1._time._day != lesson2._time._day:
            return False
            
        return not (
            lesson1._time._end_hour <= lesson2._time._start_hour or
            lesson2._time._end_hour <= lesson1._time._start_hour
        )
