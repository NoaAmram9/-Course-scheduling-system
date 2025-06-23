import sqlite3
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from SRC.Models.Course import Course
from SRC.Models.Lesson import Lesson
from SRC.Models.LessonTimes import LessonTimes
from SRC.Models.ValidationError import ValidationError


class DatabaseManager:
    def __init__(self, db_path: str = "courses.db"):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create courses table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS courses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        code TEXT NOT NULL,
                        semester INTEGER NOT NULL,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(code, name)
                    )
                ''')
                
                # Create lessons table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS lessons (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        course_id INTEGER NOT NULL,
                        lesson_type TEXT NOT NULL,
                        start_hour INTEGER NOT NULL,
                        end_hour INTEGER NOT NULL,
                        day INTEGER NOT NULL,
                        building TEXT,
                        room TEXT,
                        instructors TEXT,  -- JSON array of instructors
                        credit_points REAL DEFAULT 0,
                        weekly_hours REAL DEFAULT 0,
                        group_code INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
                    )
                ''')
                
                # Create indexes for better performance
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_courses_code ON courses(code)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_courses_semester ON courses(semester)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_lessons_course_id ON lessons(course_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_lessons_type ON lessons(lesson_type)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_lessons_day ON lessons(day)')
                
                conn.commit()
                print(f"Database initialized successfully at: {self.db_path}")
                
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            raise
    
    def clear_all_data(self) -> bool:
        """
        Clear all data from database (keep structure)
        
        Returns:
            bool: True if successful
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM lessons')
                cursor.execute('DELETE FROM courses')
                cursor.execute('DELETE FROM sqlite_sequence WHERE name IN ("courses", "lessons")')
                conn.commit()
                print("All data cleared from database")
                return True
        except sqlite3.Error as e:
            print(f"Error clearing database: {e}")
            return False
    
    def drop_database(self) -> bool:
        """
        Drop all tables (complete reset)
        
        Returns:
            bool: True if successful
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DROP TABLE IF EXISTS lessons')
                cursor.execute('DROP TABLE IF EXISTS courses')
                conn.commit()
                print("Database tables dropped")
                # Reinitialize
                self.init_database()
                return True
        except sqlite3.Error as e:
            print(f"Error dropping database: {e}")
            return False
    
    def import_courses_from_list(self, courses: List[Course]) -> tuple[int, List[ValidationError]]:
        """
        Import courses from list (from Excel parser)
        
        Args:
            courses: List of Course objects
            
        Returns:
            tuple: (number of courses imported, list of errors)
        """
        imported_count = 0
        errors = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for course in courses:
                    try:
                        # Insert course
                        cursor.execute('''
                            INSERT OR REPLACE INTO courses (name, code, semester, notes, updated_at)
                            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                        ''', (course.name, course.code, course.semester, course._notes or ''))
                        
                        course_id = cursor.lastrowid
                        if cursor.rowcount == 0:  # Was replaced, get existing ID
                            cursor.execute('SELECT id FROM courses WHERE code = ? AND name = ?', 
                                         (course.code, course.name))
                            result = cursor.fetchone()
                            if result:
                                course_id = result[0]
                                # Clear existing lessons for this course
                                cursor.execute('DELETE FROM lessons WHERE course_id = ?', (course_id,))
                        
                        # Insert all lessons
                        all_lessons = (
                            [(lesson, 'lecture') for lesson in course.lectures] +
                            [(lesson, 'exercise') for lesson in course.exercises] +
                            [(lesson, 'lab') for lesson in course.labs] +
                            [(lesson, 'departmentHours') for lesson in course.departmentHours] +
                            [(lesson, 'reinforcement') for lesson in course.reinforcement] +
                            [(lesson, 'training') for lesson in course.training]
                        )
                        
                        for lesson, lesson_type in all_lessons:
                            instructors_json = json.dumps(lesson.instructors) if lesson.instructors else '[]'
                            
                            cursor.execute('''
                                INSERT INTO lessons (
                                    course_id, lesson_type, start_hour, end_hour, day,
                                    building, room, instructors, credit_points, 
                                    weekly_hours, group_code
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                course_id, lesson_type,
                                lesson.time.start_hour, lesson.time.end_hour, lesson.time.day,
                                lesson.building or '', lesson.room or '',
                                instructors_json,
                                getattr(lesson, 'creditPoints', 0),
                                getattr(lesson, 'weeklyHours', 0),
                                getattr(lesson, 'groupCode', 0)
                            ))
                        
                        imported_count += 1
                        
                    except sqlite3.Error as e:
                        errors.append(ValidationError(
                            f"Database error for course {course.name}: {e}",
                            context={"course": course.name, "code": course.code}
                        ))
                
                conn.commit()
                
                
        except sqlite3.Error as e:
            errors.append(ValidationError(f"Database connection error: {e}"))
        
        return imported_count, errors
    
    def get_all_courses(self) -> List[Course]:
        """
        Get all courses from database
        
        Returns:
            List[Course]: List of all courses with their lessons
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get all courses
                cursor.execute('''
                    SELECT id, name, code, semester, notes 
                    FROM courses 
                    ORDER BY code, name
                ''')
                
                courses = []
                for row in cursor.fetchall():
                    course_id, name, code, semester, notes = row
                    course = Course(name=name, code=code, semester=semester, notes=notes)
                    
                    # Get lessons for this course
                    cursor.execute('''
                        SELECT lesson_type, start_hour, end_hour, day, building, room,
                               instructors, credit_points, weekly_hours, group_code
                        FROM lessons 
                        WHERE course_id = ?
                        ORDER BY lesson_type, day, start_hour
                    ''', (course_id,))
                    
                    for lesson_row in cursor.fetchall():
                        (lesson_type, start_hour, end_hour, day, building, room,
                         instructors_json, credit_points, weekly_hours, group_code) = lesson_row
                        
                        instructors = json.loads(instructors_json) if instructors_json else []
                        
                        lesson = Lesson(
                            time=LessonTimes(start_hour, end_hour, day),
                            lesson_type=lesson_type,
                            building=building or '',
                            room=room or '',
                            instructors=instructors,
                            creditPoints=credit_points,
                            weeklyHours=weekly_hours,
                            groupCode=group_code
                        )
                        
                        # Add lesson to appropriate list
                        if lesson_type == 'lecture':
                            course.lectures.append(lesson)
                        elif lesson_type == 'exercise':
                            course.exercises.append(lesson)
                        elif lesson_type == 'lab':
                            course.labs.append(lesson)
                        elif lesson_type == 'departmentHours':
                            course.departmentHours.append(lesson)
                        elif lesson_type == 'reinforcement':
                            course.reinforcement.append(lesson)
                        elif lesson_type == 'training':
                            course.training.append(lesson)
                    
                    courses.append(course)
                
                return courses
                
        except sqlite3.Error as e:
            print(f"Error getting courses: {e}")
            return []
    
    def get_courses_by_semester(self, semester: int) -> List[Course]:
        """Get courses filtered by semester"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM courses WHERE semester = ?', (semester,))
                course_ids = [row[0] for row in cursor.fetchall()]
                
                if not course_ids:
                    return []
                
                # Get full courses data
                all_courses = self.get_all_courses()
                return [course for course in all_courses if course.semester == semester]
                
        except sqlite3.Error as e:
            print(f"Error getting courses by semester: {e}")
            return []
    
    def search_courses(self, search_term: str) -> List[Course]:
        """Search courses by name or code"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id FROM courses 
                    WHERE name LIKE ? OR code LIKE ?
                ''', (f'%{search_term}%', f'%{search_term}%'))
                
                course_ids = [row[0] for row in cursor.fetchall()]
                
                if not course_ids:
                    return []
                
                # Get full courses data
                all_courses = self.get_all_courses()
                return [course for course in all_courses 
                       if search_term.lower() in course.name.lower() or 
                          search_term in course.code]
                
        except sqlite3.Error as e:
            print(f"Error searching courses: {e}")
            return []
    
    def delete_course(self, course_code: str, course_name: str = None) -> bool:
        """
        Delete course and all its lessons
        
        Args:
            course_code: Course code to delete
            course_name: Optional course name for additional verification
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if course_name:
                    cursor.execute('DELETE FROM courses WHERE code = ? AND name = ?', 
                                 (course_code, course_name))
                else:
                    cursor.execute('DELETE FROM courses WHERE code = ?', (course_code,))
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                if deleted_count > 0:
                    print(f"Deleted {deleted_count} course(s) with code {course_code}")
                    return True
                else:
                    print(f"No course found with code {course_code}")
                    return False
                    
        except sqlite3.Error as e:
            print(f"Error deleting course: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count courses
                cursor.execute('SELECT COUNT(*) FROM courses')
                total_courses = cursor.fetchone()[0]
                
                # Count lessons
                cursor.execute('SELECT COUNT(*) FROM lessons')
                total_lessons = cursor.fetchone()[0]
                
                # Count by semester
                cursor.execute('SELECT semester, COUNT(*) FROM courses GROUP BY semester')
                semester_counts = dict(cursor.fetchall())
                
                # Count by lesson type
                cursor.execute('SELECT lesson_type, COUNT(*) FROM lessons GROUP BY lesson_type')
                lesson_type_counts = dict(cursor.fetchall())
                
                return {
                    'total_courses': total_courses,
                    'total_lessons': total_lessons,
                    'courses_by_semester': semester_counts,
                    'lessons_by_type': lesson_type_counts,
                    'database_path': self.db_path
                }
                
        except sqlite3.Error as e:
            print(f"Error getting database stats: {e}")
            return {}

   
