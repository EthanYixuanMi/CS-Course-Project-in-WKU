from course_manager import CourseManager
from utils import write_log, send_enrollment_email, send_grade_email
from data_models import Student, Instructor
from utils import ask_ai_question
import textwrap # This module is used to format the AI response text for better readability

# Security password for instructor registration
SECURITY_PASSWORD = "wku12345"


def display_student_menu(manager, username):
    # Display the student menu and handle student actions
    while True:
        print("\nStudent Menu:\n1. Enroll in Course\n2. View My Courses\n3. Drop Course\n4. Ask AI for Advice\n5. Exit")
        choice = input("Your choice: ")
        # Check the choice and perform the corresponding action

        if choice == "1":
            keyword = input("Search keyword (or leave empty for all): ")
            matched_courses = manager.search_courses(keyword)
            if not matched_courses:
                print("No matching courses found.")
                continue
            for course_name in matched_courses:
                print(course_name)
            course_to_enroll = input("Enter course to enroll: ")
            # Check if the course exists and if the student is already enrolled, to avoid repeated enrollments
            if course_to_enroll in manager.courses:
                existing_course = manager.get_student_courses(username)
                if course_to_enroll in existing_course:
                    print("You are already enrolled in this course.")
                    continue
                # Enroll the student in the course and send an email notification
                manager.enroll_student(username, course_to_enroll)
                write_log(f"{username} enrolled in {course_to_enroll}")
                send_enrollment_email(username, f"Dear {username}, \n"
                                                f"\nCongratulations! You have successfully enrolled in the course: {course_to_enroll}. "
                                                f"\nPlease take some time to review the course details and ensure that it aligns with your academic goals. You can do this by logging into your Kean account.\n"
                                                f"\nSincerely,\nKean University")
                print(f"Successfully enrolled in {course_to_enroll}")
            else:
                print("Invalid course.")
        elif choice == "2":
            # Display the courses the student is enrolled in along with their grades
            courses = manager.get_student_courses(username)
            for course_name, grade in courses.items():
                # If the course's grade is assigned, display it; otherwise, display 'Not assigned'
                print(f"{course_name} - Grade: {grade if grade else 'Not assigned'}")
        elif choice == "3":
            courses = manager.get_student_courses(username)
            for course_name in courses:
                print(course_name)
            course_to_drop = input("Enter course to drop: ")
            # Check if the course exists in the student's enrolled courses
            if course_to_drop in courses:
                # Student can not drop a course that has been graded
                if courses[course_to_drop] is not None:
                    print("You cannot drop a course that has been graded.")
                    continue
                # Drop the course and send an email notification
                manager.drop_student_course(username, course_to_drop)
                write_log(f"{username} dropped {course_to_drop}")
                send_enrollment_email(username, f"Dear {username}, \n"
                                                f"\nYou have successfully dropped the course: {course_to_drop}. "
                                                f"\nIf this was a mistake, please log into your Kean account to re-enroll in the course.\n"
                                                f"\nSincerely,\nKean University")
                print("Course dropped.")
            else:
                # Student can not drop a course that they are not enrolled in
                print("You are not enrolled in this course.")

        elif choice == "4":
            question = input("Enter your academic question (e.g., What course should I take next?): ")
            # Get the student's courses and their grades
            student_courses = manager.get_student_courses(username)
            course_info = "\n".join([f"{course} - {grade if grade else 'Not assigned'}" for course, grade in student_courses.items()])

            # Get the student's major plan file
            student = manager.get_student_by_username(username) # Student's major stores in account.txt file
            major_plan_file = f"{student.major}_plan.txt" if student and student.major else None

            plan_text = ""
            if major_plan_file:
                try:
                    # Read the major plan file in read-only mode and encoding set to utf-8
                    with open(major_plan_file, "r", encoding="utf-8") as file:
                        plan_text = file.read()
                except FileNotFoundError:
                    print(f"No major plan found for {student.major}.")

            # Prepare the full prompt for the AI
            full_prompt = f"""I am a student asking the following academic question:\n"{question}"\n
                My current course history:\n{course_info}\n
                Here is the four-year plan for my major:\n{plan_text}\n
                Based on my question, my course history, and the plan above, give me a suggestion."""

            reply = ask_ai_question(full_prompt)
            print("\n[AI ADVICE]")

            paragraphs = reply.strip().split("\n") # Split the response into paragraphs based on new lines
            for paragraph in paragraphs:
                if paragraph.strip():  # Check if the paragraph is not empty
                    print(textwrap.fill(paragraph.strip(), width=80)) # Format the paragraph for better readability
                else:
                    print()

        elif choice == "5":
            manager.save_enrollments()
            print("Goodbye!")
            break
        # If the choice is not recognized, print an error message
        else:
            print("Invalid choice.")


def display_instructor_menu(manager):
    while True:
        print("\nInstructor Menu:\n1. View Student Courses\n2. Assign Grade\n3. Exit")
        choice = input("Your choice: ")
        if choice == "1":
            print("Registered Students:")
            # Display all registered students and their enrolled courses
            for student_name in manager.list_all_students():
                print(student_name)
            selected_student = input("Enter student username: ")
            student_courses = manager.get_student_courses(selected_student)
            # If the student has enrolled courses, display them; otherwise, print a notfound message
            if student_courses:
                print(f"Courses enrolled by {selected_student}:")
                for course_name, grade in student_courses.items():
                    print(f"{course_name} - Grade: {grade if grade else 'Not assigned'}")
            else:
                print("No courses found for this student.")

        elif choice == "2":
            print("Registered Students:")
            for student_name in manager.list_all_students():
                print(student_name)
            selected_student = input("Enter student username: ")
            student_courses = manager.get_student_courses(selected_student)
            if not student_courses:
                print("No courses found for this student.")
                continue
            print(f"Courses enrolled by {selected_student}:")
            for course_name, grade in student_courses.items():
                print(f"{course_name} - Grade: {grade if grade else 'Not assigned'}")

            course_name = input("Enter course name to assign grade: ")
            # Instructors can not assign grades to courses that the student is not enrolled in
            if course_name not in student_courses:
                print("Student is not enrolled in this course.")
                continue
            grade = input("Enter grade (A, A-, B+, B, B-, C+, C, D, F): ").strip().upper()
            if grade not in ["A", "A-", "B+", "B", "B-", "C+", "C" "D", "F"]:
                print("Invalid grade. Please enter A, A-, B+, B, B-, C+, C, D, or F.")
                continue
            # Assign the grade to the student for the specified course and send an email notification
            manager.set_student_grade(selected_student, course_name, grade)
            write_log(f"Assigned grade {grade} to {selected_student} for {course_name}")
            send_grade_email(selected_student, f"Dear {selected_student}, \n"
                                           f"\nYou received grade '{grade}' for course {course_name}. "
                                           f"\nPlease take some time to review and confirm your grade to ensure that it aligns with your academic goals. You can do this by logging into your Kean account.\n"
                                           f"\nSincerely,\nKean University")
            print(f"Grade {grade} assigned to {selected_student} for {course_name}.")

        elif choice == "3":
            manager.save_enrollments() # Make sure to save the grading changes before exiting
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


def main():
    print("Welcome to SmartCourse!")
    manager = CourseManager()
    while True:
        print("Main Menu:\n1. Login\n2. Register for new account\n3. Exit")
        main_choice = input("Select an option (1/2/3): ").strip()
        if main_choice == "1":
            username = input("Username: ")
            # Ensure the username ends with '@kean.edu' to maintain consistency
            if not username.endswith("@kean.edu"):
                print("Invalid username. Username must end with '@kean.edu'.")
                continue
            password = input("Password: ")
            is_student = manager.is_student_account(username)
            if manager.authenticate_user(username, password, is_student):
                write_log(f"{username} logged in")
                print(f"Welcome, {username}!")
                # Display the appropriate menu based on the user's role
                if is_student:
                    display_student_menu(manager, username)
                else:
                    display_instructor_menu(manager)
                break
            else:
                print("Login failed. Try again.")
        elif main_choice == "2":
            username = input("New username: ")
            # Ensure the username ends with '@kean.edu' to maintain consistency
            if not username.endswith("@kean.edu"):
                print("Invalid username. Username must end with '@kean.edu'.")
                continue
            password = input("Password: ")
            role = input("Role (student/instructor): ").strip().lower()
            if role not in ["student", "instructor"]:
                print("Invalid role. Please enter 'student' or 'instructor'.")
                continue
            # If the role is instructor, ask for the security password
            if role == "instructor":
                security = input("Enter security password to register as instructor: ")
                if security != SECURITY_PASSWORD:
                    print("Security password incorrect. Instructor account not created.")
                    continue
            is_student = role == "student" # Set this boolean variable to determine if the account is for a student or instructor
            # Check if the username already exists in either students or instructors
            if manager.get_student_by_username(username) or any(
                    instructor.username == username for instructor in manager.instructors):
                print("Username already exists. Please choose a different username.")
                continue
            if is_student:
                major = input("Enter your major (cps, acct, math): ").strip().lower()
                if major not in ["cps", "acct", "math"]:
                    print("Sorry, currently this system only support cps, acct and math. Please enter 'cps', 'acct', or 'math'.")
                    continue
                # Append student's username, password and major to the account.txt file if the account is for a student
                manager.students.append(Student(username, password, major))
            else:
                # Append instructor's username and password to the instructors list if the account is for an instructor
                manager.instructors.append(Instructor(username, password))

            manager.create_account(username, password, is_student)
            write_log(f"Created new account: {username}")
            print("Account created. Please log in.")
        elif main_choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Ensure the main function is called when the script is run directly
if __name__ == "__main__":
    main()
