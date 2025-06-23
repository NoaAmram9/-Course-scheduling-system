class CourseCalculator:
    """Utility class for performing calculations on course data"""
    
    LESSON_TYPES = ['lectures', 'exercises', 'labs', 'departmentHours', 'reinforcement', 'training']
    
    def calculate_total_credits(self, course):
        """Calculate the total credit points from all lesson types"""
        total = 0
        
        for lesson_type in self.LESSON_TYPES:
            lessons = getattr(course, lesson_type, [])
            for lesson in lessons:
                total += getattr(lesson, 'creditPoints', 0)
        
        return total if total > 0 else 'N/A'

    def count_total_groups(self, course):
        """Count total unique group codes across all lessons"""
        groups = set()
        
        for lesson_type in self.LESSON_TYPES:
            lessons = getattr(course, lesson_type, [])
            for lesson in lessons:
                if hasattr(lesson, 'groupCode') and lesson.groupCode:
                    groups.add(lesson.groupCode)
        
        return len(groups)

    def get_lesson_summary(self, course, lesson_type_attr, display_name):
        """Get a summary for a specific lesson type"""
        lessons = getattr(course, lesson_type_attr, [])
        count = len(lessons)
        
        if count == 0:
            return f"{display_name}: No sessions"

        groups = set()
        instructors = set()
        
        for lesson in lessons:
            if hasattr(lesson, 'groupCode') and lesson.groupCode:
                groups.add(lesson.groupCode)
            if hasattr(lesson, 'instructors') and lesson.instructors:
                instructors.update(lesson.instructors)
        
        summary = f"{display_name}: {count} sessions"
        
        if groups:
            summary += f" | Groups: {', '.join(map(str, sorted(groups)))}"
            
        if instructors:
            instructors_list = list(instructors)
            instructors_short = ', '.join(instructors_list[:2])
            if len(instructors) > 2:
                instructors_short += f" +{len(instructors)-2} more"
            summary += f" | Prof: {instructors_short}"
        
        return summary

    def get_all_lesson_summaries(self, course):
        """Get summaries for all lesson types"""
        lesson_types = [
            ('lectures', 'Lectures'),
            ('exercises', 'Exercises'),
            ('labs', 'Labs'),
            ('departmentHours', 'Department Hours'),
            ('reinforcement', 'Reinforcement'),
            ('training', 'Training')
        ]
        
        summaries = []
        for attr_name, display_name in lesson_types:
            summary = self.get_lesson_summary(course, attr_name, display_name)
            summaries.append(summary)
        
        return summaries