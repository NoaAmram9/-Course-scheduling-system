

# #############################
# # Sixth try
# #############################
# from itertools import product
# from SRC.Interfaces.IScheduleService import IScheduleService
# from SRC.Models.TimeTable import TimeTable
# from SRC.Models.Course import Course
# from SRC.Services.PreferencesService import PreferencesService

# class ScheduleService(IScheduleService):
#     def generate_schedules(self, courses: list, limit: int = 1000) -> list:
#         """Original method - kept for backward compatibility"""
#         self.possible_timetables = []
#         self.limit = limit
        
#         self.preferencesService = PreferencesService()


#         # צור את כל הקומבינציות האפשריות עבור כל קורס
#         course_combinations = []
#         for course in courses:
#             lectures = course._lectures or [None]
#             exercises = course._exercises or [None]
#             labs = course._labs or [None]
#             departmentHours = getattr(course, "_departmentHours", None) or [None]
#             reinforcement = getattr(course, "_reinforcement", None) or [None]
#             training = getattr(course, "_training", None) or [None]

#             course_combinations.append([
#                 (
#                     course._name, course._code,
#                     lec, ex, lab, dept, reinf, train
#                 )
#                 for lec, ex, lab, dept, reinf, train in product(
#                     lectures, exercises, labs,
#                     departmentHours, reinforcement, training
#                 )
#             ])


#         self._build_valid_schedules(course_combinations, 0, [], [])
#         return self.possible_timetables

#     def generate_schedules_progressive(self, courses: list, limit: int = None):
#         """
#         Generator version - yields TimeTable objects one by one
#         Much more memory efficient for large numbers of combinations
#         """
#         self.preferencesService = PreferencesService()

#         # צור את כל הקומבינציות האפשריות עבור כל קורס
#         course_combinations = []
#         for course in courses:
#             lectures = course._lectures or [None]
#             exercises = course._exercises or [None]
#             labs = course._labs or [None]
#             departmentHours = getattr(course, "_departmentHours", None) or [None]
#             reinforcement = getattr(course, "_reinforcement", None) or [None]
#             training = getattr(course, "_training", None) or [None]

#             course_combinations.append([
#                 (
#                     course._name, course._code,
#                     lec, ex, lab, dept, reinf, train
#                 )
#                 for lec, ex, lab, dept, reinf, train in product(
#                     lectures, exercises, labs,
#                     departmentHours, reinforcement, training
#                 )
#             ])


#         # Use generator version of the recursive function
#         count = 0
#         for timetable in self._build_valid_schedules_generator(course_combinations, 0, [], []):
#             yield timetable
#             count += 1
#             # רק אם יש limit, בדוק אותו
#             if limit is not None and count >= limit:
#                 break

#     def _build_valid_schedules_generator(self, combinations, index, current_courses, current_lessons):
#         """
#         Generator version of the recursive schedule building function
#         Yields valid TimeTable objects as they are found
#         """
#         if index == len(combinations):
#             # Instead of appending to a list, yield the TimeTable
#             timetable = TimeTable(current_courses.copy())
#             self.preferencesService.apply_preferences(timetable)  # call to apply preferences
#             yield timetable
#             return

#         for combo in combinations[index]:
#             name, code, lec, ex, lab, dept, reinf, train = combo
#             new_lessons = [l for l in (lec, ex, lab, dept, reinf, train) if l]

#             # בדיקת התנגשויות עם מה שכבר נבחר
#             if any(self._is_conflicting(l1, l2) for l1 in current_lessons for l2 in new_lessons):
#                 continue

#             new_course = Course(
#                 name=name,
#                 code=code,
#                 lectures=[lec] if lec else [],
#                 exercises=[ex] if ex else [],
#                 labs=[lab] if lab else [],
#                 departmentHours=[dept] if dept else [],
#                 reinforcement=[reinf] if reinf else [],
#                 training=[train] if train else []
#             )

#             # Recursively yield from the next level
#             yield from self._build_valid_schedules_generator(
#                 combinations,
#                 index + 1,
#                 current_courses + [new_course],
#                 current_lessons + new_lessons
#             )

#     def _build_valid_schedules(self, combinations, index, current_courses, current_lessons):
#         """Original recursive method - kept for backward compatibility"""
#         if len(self.possible_timetables) >= self.limit:
#             return

#         if index == len(combinations):
#             timetable = TimeTable(current_courses.copy())
#             self.possible_timetables.append(timetable)
#             self.preferencesService.apply_preferences(timetable)  # קריאה להעדפות
#             #קריאה להעדפות#########################
#             return

#         for combo in combinations[index]:
#             name, code, lec, ex, lab, dept, reinf, train = combo
#             new_lessons = [l for l in (lec, ex, lab, dept, reinf, train) if l]

#             # בדיקת התנגשויות עם מה שכבר נבחר
#             if any(self._is_conflicting(l1, l2) for l1 in current_lessons for l2 in new_lessons):
#                 continue

#             new_course = Course(
#                 name=name,
#                 code=code,
#                 lectures=[lec] if lec else [],
#                 exercises=[ex] if ex else [],
#                 labs=[lab] if lab else [],
#                 departmentHours=[dept] if dept else [],
#                 reinforcement=[reinf] if reinf else [],
#                 training=[train] if train else []
#             )

#             self._build_valid_schedules(
#                 combinations,
#                 index + 1,
#                 current_courses + [new_course],
#                 current_lessons + new_lessons
#             )

#     def _is_conflicting(self, lesson1, lesson2):
#         """Check if two lessons conflict in time"""
#         if not lesson1 or not lesson2:  # הוסף בדיקה אם אחד מהשיעורים הוא None
#             return False
            
#         if not hasattr(lesson1, '_time') or not hasattr(lesson2, '_time'):
#             return False
            
#         if lesson1._time._day != lesson2._time._day:
#             return False
            
#         return not (
#             lesson1._time._end_hour <= lesson2._time._start_hour or
#             lesson2._time._end_hour <= lesson1._time._start_hour
#         )




################################################333

# from itertools import product
# from SRC.Interfaces.IScheduleService import IScheduleService
# from SRC.Models.TimeTable import TimeTable
# from SRC.Models.Course import Course
# from SRC.Services.PreferencesService import PreferencesService

# class ScheduleService(IScheduleService):
#     def generate_schedules(self, courses: list, limit: int = 1000) -> list:
#         """Original method - kept for backward compatibility"""
#         self.possible_timetables = []
#         self.limit = limit
        
#         self.preferencesService = PreferencesService()

#         # סינון קורסים תקפים לפי החוקים החדשים
#         valid_courses = self._filter_valid_courses(courses)
#         if not valid_courses:
#             return []

#         # צור את כל הקומבינציות האפשריות עבור כל קורס
#         course_combinations = []
#         for course in valid_courses:
#             valid_combinations = self._get_valid_course_combinations(course)
#             if not valid_combinations:
#                 continue
#             course_combinations.append(valid_combinations)

#         if not course_combinations:
#             return []

#         self._build_valid_schedules(course_combinations, 0, [], [])
#         return self.possible_timetables

#     def generate_schedules_progressive(self, courses: list, limit: int = None):
#         """
#         Generator version - yields TimeTable objects one by one
#         Much more memory efficient for large numbers of combinations
#         """
#         self.preferencesService = PreferencesService()

#         # סינון קורסים תקפים לפי החוקים החדשים
#         valid_courses = self._filter_valid_courses(courses)
#         if not valid_courses:
#             return

#         # צור את כל הקומבינציות האפשריות עבור כל קורס
#         course_combinations = []
#         for course in valid_courses:
#             valid_combinations = self._get_valid_course_combinations(course)
#             if not valid_combinations:
#                 continue
#             course_combinations.append(valid_combinations)

#         if not course_combinations:
#             return

#         # Use generator version of the recursive function
#         count = 0
#         for timetable in self._build_valid_schedules_generator(course_combinations, 0, [], []):
#             yield timetable
#             count += 1
#             # רק אם יש limit, בדוק אותו
#             if limit is not None and count >= limit:
#                 break

#     def _filter_valid_courses(self, courses: list) -> list:
#         """
#         מסנן קורסים שעומדים בחוקים החדשים:
#         1. אם יש הרצאה - חייב להיות גם תרגול
#         2. אי אפשר תרגול בלי הרצאה
#         3. מעבדה יכולה להיות לבד
#         """
#         valid_courses = []
        
#         for course in courses:
#             lectures = course._lectures or []
#             exercises = course._exercises or []
#             labs = course._labs or []
#             departmentHours = getattr(course, "_departmentHours", None) or []
#             reinforcement = getattr(course, "_reinforcement", None) or []
#             training = getattr(course, "_training", None) or []
            
#             has_lectures = len(lectures) > 0
#             has_exercises = len(exercises) > 0
#             has_labs = len(labs) > 0
#             has_others = len(departmentHours) > 0 or len(reinforcement) > 0 or len(training) > 0
            
#             # בדיקת חוקים:
#             # אם יש הרצאות, חייב להיות גם תרגולים
#             if has_lectures and not has_exercises:
#                 print(f"קורס {course._name} נדחה: יש הרצאה אבל אין תרגול")
#                 continue
            
#             # אם יש תרגולים, חייב להיות גם הרצאות (אלא אם כן יש מעבדה או אחר)
#             if has_exercises and not has_lectures and not has_labs and not has_others:
#                 print(f"קורס {course._name} נדחה: יש תרגול בלבד ללא הרצאה")
#                 continue
            
#             # חייב להיות לפחות סוג אחד של שיעור
#             if not (has_lectures or has_exercises or has_labs or has_others):
#                 print(f"קורס {course._name} נדחה: אין שיעורים")
#                 continue
            
#             valid_courses.append(course)
        
#         return valid_courses

#     def _get_valid_course_combinations(self, course) -> list:
#         """
#         יוצר קומבינציות תקפות של שיעורים עבור קורס אחד
#         """
#         lectures = course._lectures or []
#         exercises = course._exercises or []
#         labs = course._labs or []
#         departmentHours = getattr(course, "_departmentHours", None) or []
#         reinforcement = getattr(course, "_reinforcement", None) or []
#         training = getattr(course, "_training", None) or []
        
#         valid_combinations = []
        
#         # אם יש הרצאות ותרגולים - חייב לפחות אחד מכל סוג
#         if lectures and exercises:
#             for lec in lectures:
#                 for ex in exercises:
#                     # קומבינציה בסיסית: הרצאה + תרגול
#                     base_combo = (course._name, course._code, lec, ex, None, None, None, None)
#                     valid_combinations.append(base_combo)
                    
#                     # הוסף מעבדות אם יש
#                     for lab in labs:
#                         combo_with_lab = (course._name, course._code, lec, ex, lab, None, None, None)
#                         valid_combinations.append(combo_with_lab)
                    
#                     # הוסף שעות מחלקה אם יש
#                     for dept in departmentHours:
#                         combo_with_dept = (course._name, course._code, lec, ex, None, dept, None, None)
#                         valid_combinations.append(combo_with_dept)
                    
#                     # הוסף חיזוק אם יש
#                     for reinf in reinforcement:
#                         combo_with_reinf = (course._name, course._code, lec, ex, None, None, reinf, None)
#                         valid_combinations.append(combo_with_reinf)
                    
#                     # הוסף אימונים אם יש
#                     for train in training:
#                         combo_with_train = (course._name, course._code, lec, ex, None, None, None, train)
#                         valid_combinations.append(combo_with_train)
        
#         # אם יש רק מעבדות (בלי הרצאה ותרגול)
#         elif labs and not lectures and not exercises:
#             for lab in labs:
#                 combo = (course._name, course._code, None, None, lab, None, None, None)
#                 valid_combinations.append(combo)
        
#         # אם יש רק שעות מחלקה/חיזוק/אימונים (בלי הרצאה ותרגול)
#         elif not lectures and not exercises and not labs:
#             # שעות מחלקה
#             for dept in departmentHours:
#                 combo = (course._name, course._code, None, None, None, dept, None, None)
#                 valid_combinations.append(combo)
            
#             # חיזוק
#             for reinf in reinforcement:
#                 combo = (course._name, course._code, None, None, None, None, reinf, None)
#                 valid_combinations.append(combo)
            
#             # אימונים
#             for train in training:
#                 combo = (course._name, course._code, None, None, None, None, None, train)
#                 valid_combinations.append(combo)
        
#         # אם יש תרגולים עם מעבדות (בלי הרצאה) - זה תקף
#         elif exercises and labs and not lectures:
#             for ex in exercises:
#                 for lab in labs:
#                     combo = (course._name, course._code, None, ex, lab, None, None, None)
#                     valid_combinations.append(combo)
        
#         return valid_combinations

#     def _build_valid_schedules_generator(self, combinations, index, current_courses, current_lessons):
#         """
#         Generator version of the recursive schedule building function
#         Yields valid TimeTable objects as they are found
#         """
#         if index == len(combinations):
#             # Instead of appending to a list, yield the TimeTable
#             timetable = TimeTable(current_courses.copy())
#             self.preferencesService.apply_preferences(timetable)  # call to apply preferences
#             yield timetable
#             return

#         for combo in combinations[index]:
#             name, code, lec, ex, lab, dept, reinf, train = combo
#             new_lessons = [l for l in (lec, ex, lab, dept, reinf, train) if l]

#             # בדיקת התנגשויות עם מה שכבר נבחר
#             if any(self._is_conflicting(l1, l2) for l1 in current_lessons for l2 in new_lessons):
#                 continue

#             new_course = Course(
#                 name=name,
#                 code=code,
#                 lectures=[lec] if lec else [],
#                 exercises=[ex] if ex else [],
#                 labs=[lab] if lab else [],
#                 departmentHours=[dept] if dept else [],
#                 reinforcement=[reinf] if reinf else [],
#                 training=[train] if train else []
#             )

#             # Recursively yield from the next level
#             yield from self._build_valid_schedules_generator(
#                 combinations,
#                 index + 1,
#                 current_courses + [new_course],
#                 current_lessons + new_lessons
#             )

#     def _build_valid_schedules(self, combinations, index, current_courses, current_lessons):
#         """Original recursive method - kept for backward compatibility"""
#         if len(self.possible_timetables) >= self.limit:
#             return

#         if index == len(combinations):
#             timetable = TimeTable(current_courses.copy())
#             self.possible_timetables.append(timetable)
#             self.preferencesService.apply_preferences(timetable)  # קריאה להעדפות
#             return

#         for combo in combinations[index]:
#             name, code, lec, ex, lab, dept, reinf, train = combo
#             new_lessons = [l for l in (lec, ex, lab, dept, reinf, train) if l]

#             # בדיקת התנגשויות עם מה שכבר נבחר
#             if any(self._is_conflicting(l1, l2) for l1 in current_lessons for l2 in new_lessons):
#                 continue

#             new_course = Course(
#                 name=name,
#                 code=code,
#                 lectures=[lec] if lec else [],
#                 exercises=[ex] if ex else [],
#                 labs=[lab] if lab else [],
#                 departmentHours=[dept] if dept else [],
#                 reinforcement=[reinf] if reinf else [],
#                 training=[train] if train else []
#             )

#             self._build_valid_schedules(
#                 combinations,
#                 index + 1,
#                 current_courses + [new_course],
#                 current_lessons + new_lessons
#             )

#     def _is_conflicting(self, lesson1, lesson2):
#         """Check if two lessons conflict in time"""
#         if not lesson1 or not lesson2:  # הוסף בדיקה אם אחד מהשיעורים הוא None
#             return False
            
#         if not hasattr(lesson1, '_time') or not hasattr(lesson2, '_time'):
#             return False
            
#         if lesson1._time._day != lesson2._time._day:
#             return False
            
#         return not (
#             lesson1._time._end_hour <= lesson2._time._start_hour or
#             lesson2._time._end_hour <= lesson1._time._start_hour
#         )


#########################################3
#WWOOORKKKKK
# from itertools import product
# from SRC.Interfaces.IScheduleService import IScheduleService
# from SRC.Models.TimeTable import TimeTable
# from SRC.Models.Course import Course
# from SRC.Services.PreferencesService import PreferencesService

# class ScheduleService(IScheduleService):
#     def generate_schedules(self, courses: list, limit: int = 1000) -> list:
#         """Original method - kept for backward compatibility"""
#         self.possible_timetables = []
#         self.limit = limit
        
#         self.preferencesService = PreferencesService()

#         # סינון קורסים תקפים לפי החוקים החדשים
#         valid_courses = self._filter_valid_courses(courses)
#         if not valid_courses:
#             return []

#         # צור את כל הקומבינציות האפשריות עבור כל קורס
#         course_combinations = []
#         for course in valid_courses:
#             valid_combinations = self._get_valid_course_combinations(course)
#             if not valid_combinations:
#                 continue
#             course_combinations.append(valid_combinations)

#         if not course_combinations:
#             return []

#         self._build_valid_schedules(course_combinations, 0, [], [])
#         return self.possible_timetables

#     def generate_schedules_progressive(self, courses: list, limit: int = None):
#         """
#         Generator version - yields TimeTable objects one by one
#         Much more memory efficient for large numbers of combinations
#         """
#         self.preferencesService = PreferencesService()

#         # סינון קורסים תקפים לפי החוקים החדשים
#         valid_courses = self._filter_valid_courses(courses)
#         if not valid_courses:
#             return

#         # צור את כל הקומבינציות האפשריות עבור כל קורס
#         course_combinations = []
#         for course in valid_courses:
#             valid_combinations = self._get_valid_course_combinations(course)
#             if not valid_combinations:
#                 continue
#             course_combinations.append(valid_combinations)

#         if not course_combinations:
#             return

#         # Use generator version of the recursive function
#         count = 0
#         for timetable in self._build_valid_schedules_generator(course_combinations, 0, [], []):
#             yield timetable
#             count += 1
#             # רק אם יש limit, בדוק אותו
#             if limit is not None and count >= limit:
#                 break

#     def _filter_valid_courses(self, courses: list) -> list:
#         """
#         מסנן קורסים שעומדים בחוקים החדשים:
#         1. אם יש הרצאה - חייב להיות גם תרגול
#         2. reinforcement חייב הרצאה + תרגול
#         3. training יכול להיות רק עם reinforcement
#         4. departmentHours יכול להיות לבד
#         5. מעבדה יכולה להיות לבד או עם הכל
#         """
#         valid_courses = []
        
#         for course in courses:
#             lectures = course._lectures or []
#             exercises = course._exercises or []
#             labs = course._labs or []
#             departmentHours = getattr(course, "_departmentHours", None) or []
#             reinforcement = getattr(course, "_reinforcement", None) or []
#             training = getattr(course, "_training", None) or []
            
#             has_lectures = len(lectures) > 0
#             has_exercises = len(exercises) > 0
#             has_reinforcement = len(reinforcement) > 0
#             has_training = len(training) > 0
            
#             # בדיקת חוקים:
#             # אם יש הרצאות, חייב להיות גם תרגולים
#             if has_lectures and not has_exercises:
#                 print(f"קורס {course._name} נדחה: יש הרצאה אבל אין תרגול")
#                 continue
            
#             # # אם יש reinforcement, חייב הרצאה + תרגול
#             # if has_reinforcement and (not has_lectures or not has_exercises):
#             #     print(f"קורס {course._name} נדחה: יש reinforcement אבל חסרה הרצאה או תרגול")
#             #     continue
                
#             # אם יש training לבד (בלי reinforcement), זה לא תקף
#             if has_training and not has_reinforcement:
#                 print(f"קורס {course._name} נדחה: יש training בלי reinforcement !!!!!!! {reinforcement} ")
#                 continue
            
#             # חייב להיות לפחות סוג אחד של שיעור
#             if not (has_lectures or has_exercises or len(labs) > 0 or len(departmentHours) > 0 or has_reinforcement or has_training):
#                 print(f"קורס {course._name} נדחה: אין שיעורים")
#                 continue
            
#             valid_courses.append(course)
        
#         return valid_courses

#     def _get_valid_course_combinations(self, course) -> list:
#         """
#         יוצר קומבינציות תקפות של שיעורים עבור קורס אחד
#         חוקים:
#         1. הרצאה + תרגול: כל הרצאה עם כל תרגול
#         2. departmentHours: יכול להיות לבד
#         3. reinforcement: חייב הרצאה + תרגול, ואפשר גם מעבדה
#         4. training: יכול להיות רק עם reinforcement
#         5. מעבדה: יכולה להיות לבד או עם הכל
#         """
#         lectures = course._lectures or []
#         exercises = course._exercises or []
#         labs = course._labs or []
#         departmentHours = getattr(course, "_departmentHours", None) or []
#         reinforcement = getattr(course, "_reinforcement", None) or []
#         training = getattr(course, "_training", None) or []
        
#         valid_combinations = []
        
#         # מקרה 1: יש הרצאות ותרגולים
#         if lectures and exercises:
#             # כל הרצאה עם כל תרגול
#             for lec in lectures:
#                 for ex in exercises:
#                     # קומבינציה בסיסית: הרצאה + תרגול
#                     base_combo = (course._name, course._code, lec, ex, None, None, None, None)
#                     valid_combinations.append(base_combo)
                    
#                     # הוסף מעבדות אם יש (כל אחת בנפרד)
#                     for lab in labs:
#                         combo_with_lab = (course._name, course._code, lec, ex, lab, None, None, None)
#                         valid_combinations.append(combo_with_lab)
                    
#                     # הוסף reinforcement אם יש (כל אחד בנפרד)
#                     for reinf in reinforcement:
#                         combo_with_reinf = (course._name, course._code, lec, ex, None, None, reinf, None)
#                         valid_combinations.append(combo_with_reinf)
                        
#                         # reinforcement + מעבדה
#                         for lab in labs:
#                             combo_reinf_lab = (course._name, course._code, lec, ex, lab, None, reinf, None)
#                             valid_combinations.append(combo_reinf_lab)
                        
#                         # reinforcement + training
#                         for train in training:
#                             combo_reinf_train = (course._name, course._code, lec, ex, None, None, reinf, train)
#                             valid_combinations.append(combo_reinf_train)
                            
#                             # reinforcement + training + מעבדה
#                             for lab in labs:
#                                 combo_all = (course._name, course._code, lec, ex, lab, None, reinf, train)
#                                 valid_combinations.append(combo_all)
        
#         # מקרה 2: יש רק מעבדות (בלי הרצאה ותרגול)
#         if labs and not lectures and not exercises:
#             for lab in labs:
#                 combo = (course._name, course._code, None, None, lab, None, None, None)
#                 valid_combinations.append(combo)
        
#         # מקרה 3: יש רק departmentHours (יכול להיות לבד)
#         if departmentHours:
#             for dept in departmentHours:
#                 combo = (course._name, course._code, None, None, None, dept, None, None)
#                 valid_combinations.append(combo)
        
#         # מקרה 4: אם יש רק תרגולים עם מעבדות (בלי הרצאה)
#         if exercises and labs and not lectures:
#             for ex in exercises:
#                 for lab in labs:
#                     combo = (course._name, course._code, None, ex, lab, None, None, None)
#                     valid_combinations.append(combo)
        
#         # מקרה 5: אם יש רק תרגולים (בלי הרצאה ובלי מעבדה) - עם departmentHours
#         if exercises and not lectures and not labs and departmentHours:
#             for ex in exercises:
#                 for dept in departmentHours:
#                     combo = (course._name, course._code, None, ex, None, dept, None, None)
#                     valid_combinations.append(combo)
        
#         # מקרה 6: reinforcement + training בלבד (בלי הרצאה ותרגול)
#         if reinforcement and training and not lectures and not exercises:
#             for reinf in reinforcement:
#                 for train in training:
#                     combo = (course._name, course._code, None, None, None, None, reinf, train)
#                     valid_combinations.append(combo)
        
#         return valid_combinations

#     def _build_valid_schedules_generator(self, combinations, index, current_courses, current_lessons):
#         """
#         Generator version of the recursive schedule building function
#         Yields valid TimeTable objects as they are found
#         """
#         if index == len(combinations):
#             # Instead of appending to a list, yield the TimeTable
#             timetable = TimeTable(current_courses.copy())
#             self.preferencesService.apply_preferences(timetable)  # call to apply preferences
#             yield timetable
#             return

#         for combo in combinations[index]:
#             name, code, lec, ex, lab, dept, reinf, train = combo
#             new_lessons = [l for l in (lec, ex, lab, dept, reinf, train) if l]

#             # בדיקת התנגשויות עם מה שכבר נבחר
#             if any(self._is_conflicting(l1, l2) for l1 in current_lessons for l2 in new_lessons):
#                 continue

#             new_course = Course(
#                 name=name,
#                 code=code,
#                 lectures=[lec] if lec else [],
#                 exercises=[ex] if ex else [],
#                 labs=[lab] if lab else [],
#                 departmentHours=[dept] if dept else [],
#                 reinforcement=[reinf] if reinf else [],
#                 training=[train] if train else []
#             )

#             # Recursively yield from the next level
#             yield from self._build_valid_schedules_generator(
#                 combinations,
#                 index + 1,
#                 current_courses + [new_course],
#                 current_lessons + new_lessons
#             )
          

#     def _build_valid_schedules(self, combinations, index, current_courses, current_lessons):
#         """Original recursive method - kept for backward compatibility"""
#         if len(self.possible_timetables) >= self.limit:
#             return

#         if index == len(combinations):
#             timetable = TimeTable(current_courses.copy())
#             self.possible_timetables.append(timetable)
#             self.preferencesService.apply_preferences(timetable)  # קריאה להעדפות
#             return

#         for combo in combinations[index]:
#             name, code, lec, ex, lab, dept, reinf, train = combo
#             new_lessons = [l for l in (lec, ex, lab, dept, reinf, train) if l]

#             # בדיקת התנגשויות עם מה שכבר נבחר
#             if any(self._is_conflicting(l1, l2) for l1 in current_lessons for l2 in new_lessons):
#                 continue

#             new_course = Course(
#                 name=name,
#                 code=code,
#                 lectures=[lec] if lec else [],
#                 exercises=[ex] if ex else [],
#                 labs=[lab] if lab else [],
#                 departmentHours=[dept] if dept else [],
#                 reinforcement=[reinf] if reinf else [],
#                 training=[train] if train else []
#             )

#             self._build_valid_schedules(
#                 combinations,
#                 index + 1,
#                 current_courses + [new_course],
#                 current_lessons + new_lessons
#             )

#     def _is_conflicting(self, lesson1, lesson2):
#         """Check if two lessons conflict in time"""
#         if not lesson1 or not lesson2:  # הוסף בדיקה אם אחד מהשיעורים הוא None
#             return False
            
#         if not hasattr(lesson1, '_time') or not hasattr(lesson2, '_time'):
#             return False
            
#         if lesson1._time._day != lesson2._time._day:
#             return False
            
#         return not (
#             lesson1._time._end_hour <= lesson2._time._start_hour or
#             lesson2._time._end_hour <= lesson1._time._start_hour
#         )

#########################
from itertools import product
from SRC.Interfaces.IScheduleService import IScheduleService
from SRC.Models.TimeTable import TimeTable
from SRC.Models.Course import Course
from SRC.Services.TimetableMetricsService import TimetableMetricsService

class ScheduleService(IScheduleService):
    def __init__(self):
        """יצירה פעם אחת של שירות ההעדפות"""
        self.timetable_metrics_service = TimetableMetricsService()
    
    def generate_schedules(self, courses: list, limit: int = 1000) -> list:
        """
        לכמויות קטנות-בינוניות - מחזיר רשימה מלאה
        מתאים כשצריך לדעת כמה תוצאות יש או לגשת אליהן מספר פעמים
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
        לכמויות גדולות - Generator יעיל בזיכרון
        מתאים כשיש אלפים/מיליוני אפשרויות
        """
        count = 0
        for timetable in self._generate_schedules_core(courses):
            yield timetable
            count += 1
            if limit is not None and count >= limit:
                break

    def _generate_schedules_core(self, courses: list):
        """
        הלוגיקה המרכזית - פונקציה אחת בלבד!
        מחזירה generator תמיד לחיסכון בזיכרון
        """
        # סינון קורסים תקפים לפי החוקים החדשים
        valid_courses = self._filter_valid_courses(courses)
        if not valid_courses:
            return

        # צור את כל הקומבינציות האפשריות עבור כל קורס
        course_combinations = []
        for course in valid_courses:
            valid_combinations = self._get_valid_course_combinations(course)
            if not valid_combinations:
                continue
            course_combinations.append(valid_combinations)

        if not course_combinations:
            return

        # קריאה לפונקציה הרקורסיבית היחידה
        yield from self._build_valid_schedules_recursive(course_combinations, 0, [], [])

    def _filter_valid_courses(self, courses: list) -> list:
        """
        מסנן קורסים שעומדים בחוקים החדשים:
        1. אם יש הרצאה - חייב להיות גם תרגול
        2. reinforcement חייב הרצאה + תרגול
        3. training יכול להיות רק עם reinforcement
        4. departmentHours יכול להיות לבד
        5. מעבדה יכולה להיות לבד או עם הכל
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
            
            # בדיקת חוקים:
            # אם יש הרצאות, חייב להיות גם תרגולים
            # if has_lectures and not has_exercises:
            #     print(f"קורס {course._name} נדחה: יש הרצאה אבל אין תרגול")
            #     continue
            
            # # אם יש reinforcement, חייב הרצאה + תרגול
            # if has_reinforcement and (not has_lectures or not has_exercises):
            #     print(f"קורס {course._name} נדחה: יש reinforcement אבל חסרה הרצאה או תרגול")
            #     continue
                
            # אם יש training לבד (בלי reinforcement), זה לא תקף
            if has_training and not has_reinforcement:
                print(f"קורס {course._name} נדחה: יש training בלי reinforcement !!!!!!! {reinforcement} ")
                continue
            
            # חייב להיות לפחות סוג אחד של שיעור
            if not (has_lectures or has_exercises or len(labs) > 0 or len(departmentHours) > 0 or has_reinforcement or has_training):
                print(f"קורס {course._name} נדחה: אין שיעורים")
                continue
            
            valid_courses.append(course)
        
        return valid_courses

    def _get_valid_course_combinations(self, course) -> list:
        """
        יוצר קומבינציות תקפות של שיעורים עבור קורס אחד
        חוקים:
        1. הרצאה + תרגול: כל הרצאה עם כל תרגול
        2. departmentHours: יכול להיות לבד
        3. reinforcement: חייב הרצאה + תרגול, ואפשר גם מעבדה
        4. training: יכול להיות רק עם reinforcement
        5. מעבדה: יכולה להיות לבד או עם הכל
        """
        lectures = course._lectures or []
        exercises = course._exercises or []
        labs = course._labs or []
        departmentHours = getattr(course, "_departmentHours", None) or []
        reinforcement = getattr(course, "_reinforcement", None) or []
        training = getattr(course, "_training", None) or []
        
        valid_combinations = []
        
        # מקרה 1: יש הרצאות ותרגולים
        if lectures and exercises:
            # כל הרצאה עם כל תרגול
            for lec in lectures:
                for ex in exercises:
                    # קומבינציה בסיסית: הרצאה + תרגול
                    base_combo = (course._name, course._code, lec, ex, None, None, None, None)
                    valid_combinations.append(base_combo)
                    
                    # הוסף מעבדות אם יש (כל אחת בנפרד)
                    for lab in labs:
                        combo_with_lab = (course._name, course._code, lec, ex, lab, None, None, None)
                        valid_combinations.append(combo_with_lab)
                    
                    # הוסף reinforcement אם יש (כל אחד בנפרד)
                    for reinf in reinforcement:
                        combo_with_reinf = (course._name, course._code, lec, ex, None, None, reinf, None)
                        valid_combinations.append(combo_with_reinf)
                        
                        # reinforcement + מעבדה
                        for lab in labs:
                            combo_reinf_lab = (course._name, course._code, lec, ex, lab, None, reinf, None)
                            valid_combinations.append(combo_reinf_lab)
                        
                        # reinforcement + training
                        for train in training:
                            combo_reinf_train = (course._name, course._code, lec, ex, None, None, reinf, train)
                            valid_combinations.append(combo_reinf_train)
                            
                            # reinforcement + training + מעבדה
                            for lab in labs:
                                combo_all = (course._name, course._code, lec, ex, lab, None, reinf, train)
                                valid_combinations.append(combo_all)
        
        # מקרה 2: יש רק מעבדות (בלי הרצאה ותרגול)
        if labs and not lectures and not exercises:
            for lab in labs:
                combo = (course._name, course._code, None, None, lab, None, None, None)
                valid_combinations.append(combo)
        
        # מקרה 3: יש רק departmentHours (יכול להיות לבד)
        if departmentHours:
            for dept in departmentHours:
                combo = (course._name, course._code, None, None, None, dept, None, None)
                valid_combinations.append(combo)
        
        # מקרה 4: אם יש רק תרגולים עם מעבדות (בלי הרצאה)
        if exercises and labs and not lectures:
            for ex in exercises:
                for lab in labs:
                    combo = (course._name, course._code, None, ex, lab, None, None, None)
                    valid_combinations.append(combo)
        
        # מקרה 5: אם יש רק תרגולים (בלי הרצאה ובלי מעבדה) - עם departmentHours
        if exercises and not lectures and not labs and departmentHours:
            for ex in exercises:
                for dept in departmentHours:
                    combo = (course._name, course._code, None, ex, None, dept, None, None)
                    valid_combinations.append(combo)
        
        # מקרה 6: reinforcement + training בלבד (בלי הרצאה ותרגול)
        if reinforcement and training and not lectures and not exercises:
            for reinf in reinforcement:
                for train in training:
                    combo = (course._name, course._code, None, None, None, None, reinf, train)
                    valid_combinations.append(combo)
        
        return valid_combinations

    def _build_valid_schedules_recursive(self, combinations, index, current_courses, current_lessons):
        """
        פונקציה רקורסיבית יחידה לבניית מערכות שעות תקפות
        מחזירה generator לחיסכון בזיכרון
        """
        if index == len(combinations):
            # יצירת מערכת שעות שלמה
            timetable = TimeTable(current_courses.copy())
            
            # *** המקום הנכון והיחיד לקריאה להעדפות! ***
            # רק כאן, אחרי שהמערכת מוכנה לחלוטין עם כל הקורסים
            self.timetable_metrics_service.generate_metrics(timetable)
            
            yield timetable
            return

        for combo in combinations[index]:
            name, code, lec, ex, lab, dept, reinf, train = combo
            new_lessons = [l for l in (lec, ex, lab, dept, reinf, train) if l]

            # בדיקת התנגשויות עם מה שכבר נבחר
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

            # המשך רקורסיבי
            yield from self._build_valid_schedules_recursive(
                combinations,
                index + 1,
                current_courses + [new_course],
                current_lessons + new_lessons
            )

    def _is_conflicting(self, lesson1, lesson2):
        """Check if two lessons conflict in time"""
        if not lesson1 or not lesson2:  # הוסף בדיקה אם אחד מהשיעורים הוא None
            return False
            
        if not hasattr(lesson1, '_time') or not hasattr(lesson2, '_time'):
            return False
            
        if lesson1._time._day != lesson2._time._day:
            return False
            
        return not (
            lesson1._time._end_hour <= lesson2._time._start_hour or
            lesson2._time._end_hour <= lesson1._time._start_hour
        )
