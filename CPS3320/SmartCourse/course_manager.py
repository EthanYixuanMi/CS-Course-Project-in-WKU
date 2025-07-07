from data_models import Student, Instructor

class CourseManager:
    # Create an instance of CourseManager to manage courses, students, and instructors.
    def __init__(self):
        self.courses = self.load_course_list("course_list.txt")
        self.students = []
        self.instructors = []
        self.load_user_accounts("account.txt")
        self.load_enrollments("enrolled_courses.txt")

    def load_course_list(self, filename):
        try:
            # Open the course list file in read-only mode and read its contents.
            with open(filename, "r", encoding="utf-8") as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            return []

    def load_user_accounts(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split(",")
                    # Check if a major is assigned to the student
                    if len(parts) >= 3:
                        username, password, role = parts[0], parts[1], parts[2]
                        major = parts[3] if len(parts) >= 4 else None
                        if role == "student":
                            self.students.append(Student(username, password, major))
                        else:
                            self.instructors.append(Instructor(username, password))
        except FileNotFoundError:
            pass

    def load_enrollments(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split(",")
                    # Check if the line has enough parts to extract username, course name, and grade
                    if len(parts) >= 2:
                        username, course_name = parts[0], parts[1]
                        grade = parts[2] if len(parts) == 3 else None
                        student = self.get_student_by_username(username)
                        if student:
                            student.add_course(course_name)
                            if grade:
                                student.set_grade(course_name, grade)
        except FileNotFoundError:
            pass

    def save_account(self, username, password, is_student):
        with open("account.txt", "a", encoding="utf-8") as file:
            role = "student" if is_student else "instructor"
            # If the user is a student, include their major in the account file
            if is_student:
                student = self.get_student_by_username(username)
                major = student.major if student else ""
                file.write(f"{username},{password},{role},{major}\n")
            else:
                # For instructors, just save username, password, and role
                file.write(f"{username},{password},{role}\n")

    def save_enrollments(self):
        with open("enrolled_courses.txt", "w", encoding="utf-8") as file:
            for student in self.students:
                for course_name, grade in student.enrolled_courses.items():
                    line = f"{student.username},{course_name}"
                    # If the student has a grade for the course, include it in the line
                    if grade is not None:
                        line += f",{grade}"
                    file.write(line + "\n")

    def append_enrollment(self, username, course_name):
        with open("enrolled_courses.txt", "a", encoding="utf-8") as file:
            file.write(f"{username},{course_name}\n")

    def create_account(self, username, password, is_student):
        if is_student:
            self.students.append(Student(username, password))
        else:
            self.instructors.append(Instructor(username, password))
        self.save_account(username, password, is_student)

    def authenticate_user(self, username, password, is_student):
        user_list = self.students if is_student else self.instructors # Select the appropriate user list based on the role
        return any(user.username == username and user.password == password for user in user_list) # Check if the user exists in the selected list

    def is_student_account(self, username):
        return any(student.username == username for student in self.students)

    def get_student_by_username(self, username):
        for student in self.students:
            if student.username == username:
                return student
        return None

    def search_courses(self, keyword):
        keyword_lower = keyword.lower()
        # User can search for courses for any keyword, including an empty string to return all courses
        return [course for course in self.courses if keyword_lower in course.lower() or not keyword]

    def enroll_student(self, username, course_name):
        student = self.get_student_by_username(username)
        if student and course_name not in student.enrolled_courses:
            student.add_course(course_name)
            self.append_enrollment(username, course_name)

    def drop_student_course(self, username, course_name):
        student = self.get_student_by_username(username)
        if student:
            student.drop_course(course_name)
            self.save_enrollments()

    def set_student_grade(self, username, course_name, grade):
        student = self.get_student_by_username(username)
        if student and course_name in student.enrolled_courses:
            student.set_grade(course_name, grade)
            self.save_enrollments()

    def get_student_courses(self, username):
        student = self.get_student_by_username(username)
        return student.enrolled_courses if student else {}

    def list_all_students(self):
        return [student.username for student in self.students]
