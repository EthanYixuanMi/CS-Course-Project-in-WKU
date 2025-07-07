class Student:
    def __init__(self, username, password, major=None):
        self.username = username
        self.password = password
        self.major = major
        self.enrolled_courses = {}  # course_name -> grade (None if not yet graded)

    def add_course(self, course_name):
        if course_name not in self.enrolled_courses:
            self.enrolled_courses[course_name] = None

    def drop_course(self, course_name):
        if course_name in self.enrolled_courses:
            del self.enrolled_courses[course_name]

    def set_grade(self, course_name, grade):
        if course_name in self.enrolled_courses:
            self.enrolled_courses[course_name] = grade


class Instructor:
    def __init__(self, username, password):
        # The logic for grading students is written in course_manager, not in data_models.
        self.username = username
        self.password = password