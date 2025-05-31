# logic_timetable.py
# This file contains the logic for mapping courses to time slots in a timetable.

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
HOURS = list(range(8, 22))  # 8:00 to 21:00 (the range excludes the upper bound)

def map_courses_to_slots(timetable):
    """Maps each course to its time slots in the form {(day, hour): course}."""
    slot_map = {}
    
    courses = timetable.courses
    
    for course in courses:
        for lesson_type, lesson_list in [("Lecture", course.lectures),
                                         ("Exercise", course.exercises),
                                         ("Lab", course.labs)]:
            for lesson in lesson_list:
                day = DAYS[lesson.time.day - 1]  # Convert day index to string
                start = int(lesson.time.start_hour.split(":")[0])
                end = int(lesson.time.end_hour.split(":")[0])
                
                # Fill in the slots for this lesson
                for hour in range(start, end):
                    slot_map[(day, hour)] = {
                        "name": course.name,
                        "code": course.code,
                        "type": lesson_type,
                        "instructor": course.instructor,
                        "location": f"{lesson.building}-{lesson.room}"
                    }
    
    return slot_map

def get_lesson_type_color_class(lesson_type):
    """Returns the CSS class name for styling based on lesson type."""
    lesson_type_lower = lesson_type.lower()
    
    if lesson_type_lower == "lecture":
        return "lectureCell"
    elif lesson_type_lower == "lab":
        return "labCell"
    elif lesson_type_lower == "exercise":
        return "exerciseCell"
    elif lesson_type_lower == "department hours":
        return "departmentCell"
    elif lesson_type_lower == "reinforcement":
        return "reinforcementCell"
    elif lesson_type_lower == "training":
        return "trainingCell"
    else:
        return "courseCell"  # Default styling

def format_course_info(course_data):
    """Formats course information for display in timetable cells."""
    if not course_data:
        return ""
    
    lines = []
    
    # Course name and code
    if course_data.get("name"):
        lines.append(course_data["name"])
    elif course_data.get("code"):
        lines.append(course_data["code"])
    
    # Course code (if name was added first)
    if course_data.get("name") and course_data.get("code"):
        lines.append(f"({course_data['code']})")
    
    # Lesson type
    if course_data.get("type"):
        lines.append(course_data["type"])
    
    # Location
    if course_data.get("location"):
        lines.append(course_data["location"])
    
    # Instructor (abbreviated for space)
    if course_data.get("instructor"):
        instructor = course_data["instructor"]
        # Abbreviate long instructor names
        if len(instructor) > 15:
            instructor = instructor[:12] + "..."
        lines.append(instructor)
    
    return '\n'.join(lines)

def get_tooltip_text(course_data):
    """Creates detailed tooltip text for course cells."""
    if not course_data:
        return ""
    
    tooltip_parts = []
    
    # Course name
    if course_data.get("name"):
        tooltip_parts.append(f"Course: {course_data['name']}")
    
    # Course code
    if course_data.get("code"):
        tooltip_parts.append(f"Code: {course_data['code']}")
    
    # Lesson type
    if course_data.get("type"):
        tooltip_parts.append(f"Type: {course_data['type']}")
    
    # Instructor
    if course_data.get("instructor"):
        tooltip_parts.append(f"Instructor: {course_data['instructor']}")
    
    # Location
    if course_data.get("location"):
        tooltip_parts.append(f"Location: {course_data['location']}")
    
    return '\n'.join(tooltip_parts)

def get_time_range_string(start_hour, end_hour):
    """Converts hour range to readable time string."""
    return f"{start_hour:02d}:00 - {end_hour:02d}:00"

def is_time_slot_available(slot_map, day, hour):
    """Check if a time slot is available (not occupied by a course)."""
    return (day, hour) not in slot_map

def get_courses_for_day(slot_map, day):
    """Get all courses scheduled for a specific day."""
    day_courses = {}
    for (slot_day, hour), course_data in slot_map.items():
        if slot_day == day:
            day_courses[hour] = course_data
    return day_courses

def get_daily_schedule_summary(slot_map):
    """Get a summary of courses per day."""
    daily_summary = {day: [] for day in DAYS}
    
    for (day, hour), course_data in slot_map.items():
        if course_data not in daily_summary[day]:
            daily_summary[day].append(course_data)
    
    return daily_summary

def validate_timetable_data(timetable):
    """Validate timetable data structure."""
    if not hasattr(timetable, 'courses'):
        return False, "Timetable must have courses attribute"
    
    for course in timetable.courses:
        # Check required course attributes
        required_attrs = ['name', 'code', 'lectures', 'exercises', 'labs']
        for attr in required_attrs:
            if not hasattr(course, attr):
                return False, f"Course missing required attribute: {attr}"
    
    return True, "Valid timetable data"

def get_time_conflicts(slot_map):
    """Detect time conflicts in the timetable."""
    conflicts = []
    time_slots = {}
    
    for (day, hour), course_data in slot_map.items():
        slot_key = (day, hour)
        if slot_key in time_slots:
            # Conflict detected
            conflicts.append({
                'time_slot': slot_key,
                'courses': [time_slots[slot_key], course_data]
            })
        else:
            time_slots[slot_key] = course_data
    
    return conflicts