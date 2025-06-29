from SRC.DataBase.DataBaseManager import DatabaseManager


class LessonEditService:
    def get_alternative_lessons(self, course_code, selected_lesson):
        courses = DatabaseManager().search_courses(course_code)
        if not courses:
            print("No course found in database.")
            return []
        course = courses[0]

        if not course:
            print("No course found containing the lesson.")
            return []

        type_map = {
            "lecture": course.lectures,
            "exercise": course.exercises,
            "lab": course.labs,
            "reinforcement": course.reinforcement,
            "training": course.training,
            "departmentHours": course.departmentHours
        }

        same_type_lessons = type_map.get(selected_lesson.lesson_type, [])

        print("Same type lessons found:", len(same_type_lessons))
        for l in same_type_lessons:
            print("Lesson:", l.time.day, l.time.start_hour, l.groupCode)

        return same_type_lessons  # for now, skip filtering



    def replace_lesson(self, timetable, old_lesson, new_lesson):
        if self.has_conflict(timetable, new_lesson, exclude=old_lesson):
            return False
        for course in timetable.courses:
            lesson_lists = [
                course.lectures,
                course.exercises,
                course.labs,
                course.reinforcement,
                course.training,
                course.departmentHours
            ]
            for lesson_list in lesson_lists:
                for i, lesson in enumerate(lesson_list):
                    if lesson == old_lesson:
                        lesson_list[i] = new_lesson
                        return True  # Successfully replaced

        return False  # Not found


    def has_conflict(self, timetable, new_lesson, exclude=None):
        return any(
            l.time.day == new_lesson.time.day and
            not (l.time.end_hour <= new_lesson.time.start_hour or l.time.start_hour >= new_lesson.time.end_hour)
            for l in self.get_all_lessons(timetable)
            if l != exclude  
        )


    def get_all_lessons(self, timetable):
        all_lessons = []
        for course in timetable.courses:
            all_lessons.extend(course.lectures)
            all_lessons.extend(course.exercises)
            all_lessons.extend(course.labs)
            all_lessons.extend(course.reinforcement)
            all_lessons.extend(course.training)
            all_lessons.extend(course.departmentHours)
        return all_lessons


