import gradio as gr
from course_manager import CourseManager
from data_models import Student, Instructor
from utils import write_log, send_enrollment_email, send_grade_email, ask_ai_question

# Security Password Constants (Consistent with those in CLI)
SECURITY_PASSWORD = "wku12345"

# Initialize the course manager (load the course list, accounts, course selection records, etc.)
manager = CourseManager()

# Predefined List (Used for Dropdown Options)
ALLOWED_MAJORS = ["cps", "acct", "math"]
ALLOWED_GRADES = ["A", "A-", "B+", "B", "B-", "C+", "C", "D", "F"]

# Gradio Interface Construction
with gr.Blocks(css=""" 
/* Custom styles to enhance readability */
.gradio-container {font-size: 16px;}
.gr-button {font-size: 16px; padding: 8px 16px; margin: 4px 0;}
""") as demo:
    # Application Title
    gr.Markdown("# SmartCourse Management System", elem_id="app-title")

    # State Storage: Current Logged-In User and Role
    state_username = gr.State(value="")
    state_role = gr.State(value="")  # "student" or "instructor", will be empty when not logged in

    # Main Menu Interface
    with gr.Column(visible=True) as main_menu:
        gr.Markdown("## Main Menu")
        main_menu_msg = gr.Markdown("", visible=False)  # Main Menu Notification Messages (Login Successful, etc.)
        btn_login = gr.Button("Login")
        btn_register = gr.Button("Register a new account")
        btn_exit = gr.Button("Exit System")

    # Main Menu Notification Messages (Registration Successful, etc.)
    with gr.Column(visible=False) as login_frame:
        gr.Markdown("## Log in to the account")
        login_error = gr.Markdown("", visible=False)  # Login error message
        login_username = gr.Textbox(label="user name (@kean.edu)", placeholder="name@kean.edu")
        login_password = gr.Textbox(label="password", type="password")
        login_submit = gr.Button("Log in")

    # Registration interface
    with gr.Column(visible=False) as register_frame:
        gr.Markdown("## Register a new account")
        register_error = gr.Markdown("", visible=False)  # Registration error message
        reg_username = gr.Textbox(label="mail (@kean.edu)")
        reg_password = gr.Textbox(label="set a password", type="password")
        reg_role = gr.Radio(["student", "instructor"], label="account type", value="student")
        reg_major = gr.Dropdown(ALLOWED_MAJORS, label="Professional (Student Account)", visible=True)
        reg_security = gr.Textbox(label="Security registration code", type="password", visible=False)
        reg_submit = gr.Button("create an account")

    # Student Menu Interface
    with gr.Column(visible=False) as student_frame:
        student_welcome = gr.Markdown("")  # Welcome message, such as "Welcome, user@kean.edu!"
        gr.Markdown("### Student Menu")
        stud_menu_msg = gr.Markdown("", visible=False)  # Generally used to display one-time prompts, such as exit/error messages.
        # Student Function Button
        stud_enroll = gr.Button("Enroll in Course")
        stud_view = gr.Button("View My Courses")
        stud_drop = gr.Button("Drop Course")
        stud_ask = gr.Button("Ask AI for Advice")
        stud_exit = gr.Button("Logout")

        # Course Selection Sub-interface
        with gr.Column(visible=False) as stud_enroll_section:
            gr.Markdown("**Course Selection:** Search for and select courses for enrollment.")
            enroll_search = gr.Textbox(label="Course search keywords", placeholder="Enter the search keyword. If left blank, all courses will be displayed.")
            enroll_search_btn = gr.Button("Search for courses")
            enroll_course_list = gr.Dropdown(label="List of Optional Courses", choices=[], visible=False)
            enroll_confirm_btn = gr.Button("Confirm course selection", visible=False)
            enroll_status = gr.Markdown("", visible=False)

        # View Course Sub-interface
        with gr.Column(visible=False) as stud_view_section:
            gr.Markdown("**My Selected Courses: **")
            view_courses_text = gr.Markdown("")  # Directly used to display the course list

        # Withdrawal Course Interface
        with gr.Column(visible=False) as stud_drop_section:
            gr.Markdown("**Drop a course:** Select to withdraw from a course")
            drop_course_select = gr.Dropdown(label="Selected courses", choices=[], visible=True, interactive=True)
            drop_confirm_btn = gr.Button("Confirm withdrawal from class")
            drop_status = gr.Markdown("", visible=False)

        # AI Questioning Sub-interface
        with gr.Column(visible=False) as stud_ask_section:
            gr.Markdown("**Seeking Academic Advice from AI: **")
            ask_question = gr.Textbox(label="your problem", placeholder="For example: What courses should I choose for the next semester?")
            ask_submit_btn = gr.Button("Question AI")
            ask_response = gr.Markdown("", visible=False)

    # Teacher Menu Interface
    with gr.Column(visible=False) as instructor_frame:
        inst_welcome = gr.Markdown("")  # Welcome Message
        gr.Markdown("### Teacher Menu")
        inst_menu_msg = gr.Markdown("", visible=False)
        inst_view = gr.Button("View Student Courses")
        inst_assign = gr.Button("Assign Grade")
        inst_exit = gr.Button("Logout")

        # View Sub-Interface of Student Courses
        with gr.Column(visible=False) as inst_view_section:
            gr.Markdown("**Check the students' course selection: **")
            view_student_select = gr.Dropdown(label="Select students", choices=manager.list_all_students(), interactive=True)
            view_student_btn = gr.Button("View courses")
            view_student_courses_text = gr.Markdown("", visible=False)


        # --- Added: Button Callback ---
        def on_view_student_courses(student_name):
            if not student_name:
                return gr.update(value="⚠ Please select the students.", visible=True)

            courses = manager.get_student_courses(student_name)
            if not courses:  # Did not choose courses
                return gr.update(value=f"*{student_name} No courses have been selected yet. *", visible=True)

            # Assembly course list
            lines = [f"- **{c}** Grade: {grade if grade else 'Not assigned'}"
                     for c, grade in courses.items()]
            content = f"**{student_name} the course：**\n\n" + "\n".join(lines)
            return gr.update(value=content, visible=True)


        # Bind button
        view_student_btn.click(
            on_view_student_courses,
            inputs=view_student_select,
            outputs=view_student_courses_text
        )

        # Registration Results Sub-interface
        with gr.Column(visible=False) as inst_assign_section:
            gr.Markdown("**Grade students' courses:**")
            assign_student_select = gr.Dropdown(label="chose students", choices=manager.list_all_students(), interactive=True)
            assign_course_select = gr.Dropdown(label="chose courses", choices=[], visible=False, interactive=True)
            assign_grade_select = gr.Dropdown(label="grades", choices=ALLOWED_GRADES, visible=False, interactive=True)
            assign_grade_btn = gr.Button("submit grades", visible=False)
            assign_status = gr.Markdown("", visible=False)


    ### Definition of Event Handling Function ###

    # Main menu button event: Enter login interface
    def on_main_login():
        #  ensure the main menu is hidden, clear any previous messages
        login_username.value = ""
        login_password.value = ""
        return (gr.update(visible=False),
                gr.update(value="", visible=False),  # clear main menu message
                gr.update(visible=True),  # login interface visible
                gr.update(value="", visible=False))  # clear login error message


    btn_login.click(on_main_login,
                    inputs=None,
                    outputs=[main_menu, main_menu_msg, login_frame, login_error])


    # Main menu button event: Enter registration interface
    def on_main_register():
        # Clear the fields of the registration form
        return (gr.update(visible=False),  # Hide main menu
                "", "",  # Clear the values in the username and password input fields
                gr.update(value="student"),  # Reset the character selection to "student"
                gr.update(visible=True),  # Display professional fields
                gr.update(value="", visible=False),  # Hide Security Code Field
                gr.update(visible=True),  # Display the registration interface
                gr.update(value="", visible=False))  # Hide the registration error message


    btn_register.click(lambda: None, inputs=None, outputs=None)  # Clear the main menu message before switching to registration
    btn_register.click(on_main_register,
                       inputs=None,
                       outputs=[main_menu, reg_username, reg_password, reg_role, reg_major, reg_security,
                                register_frame, register_error])


    # Main Menu Button Event: Exit System
    def on_main_exit():
        # Keep all the modification records (just in case)
        manager.save_enrollments()
        # Display "Goodbye" and disable other components (by hiding the buttons)
        return ("**Exit the System, Goodbye!**",  # Display "Goodbye" in the message area of the main menu.
                gr.update(visible=True),  # Main menu message visible
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False))


    btn_exit.click(on_main_exit,
                   inputs=None,
                   outputs=[main_menu_msg, main_menu_msg, btn_login, btn_register, btn_exit])


    # Registration interface: Role switching event (Radio change)
    def on_role_change(role):
        if role == "student":
            return (gr.update(visible=True), gr.update(visible=False))
        else:
            return (gr.update(visible=False), gr.update(visible=True))


    reg_role.change(on_role_change,
                    inputs=reg_role,
                    outputs=[reg_major, reg_security])


    # Submit registration event
    def on_register_submit(username, password, role, major, security):
        error_msg = ""
        if not username.endswith("@kean.edu"):
            error_msg = "⚠ The username must end with @kean.edu！"
        elif role not in ["student", "instructor"]:
            error_msg = "⚠ The character must be 'student' or 'instructor'！"
        elif role == "instructor" and security != SECURITY_PASSWORD:
            error_msg = "⚠ The security registration code is incorrect, so the teacher account cannot be created."
        else:
            user_exists = (manager.get_student_by_username(username) is not None) or any(
                inst.username == username for inst in manager.instructors)
            if user_exists:
                error_msg = "⚠ This username has already been registered. Please change your email address."
        if error_msg:
            # If there is an error, return the error message and keep the registration interface visible
            # return (gr.update(value=error_msg, visible=True),)
            return(gr.update(value=error_msg, visible=True), gr.update(visible=True),
                   gr.update(visible=False), gr.update(value="", visible=False))
        # If no error, proceed with registration
        is_student = (role == "student")
        if is_student:
            # Check if the major is valid
            if (major or "").strip().lower() not in ALLOWED_MAJORS:
                return (gr.update(value='⚠ The information for this major is incorrect. Only "cps", "acct" and "math" are supported.', visible=True))
            # Create a new student account
            manager.students.append(Student(username, password, major.strip().lower()))
        else:
            manager.instructors.append(Instructor(username, password))
        # Write the new account to the data file
        manager.create_account(username, password, is_student)
        write_log(f"Created new account: {username}")
        # Send registration success email
        success_message = f"✅ Account {username} has been created. Please log in."
        return (
            gr.update(visible=False),  # Hide the registration interface
            gr.update(value=success_message, visible=True),  # Show success message
            gr.update(visible=True),  # Show the main menu
            gr.update(value="", visible=False)  # Clear the main menu message (if any, such as "Registration successful"
        )


    reg_submit.click(on_register_submit,
                     inputs=[reg_username, reg_password, reg_role, reg_major, reg_security],
                     outputs=[register_error, register_frame, main_menu, main_menu_msg])


    # Login Interface: Submit Login Event
    def on_login_submit(username, password):
        # Clear previous error messages
        error = ""
        welcome = ""
        user_role = ""
        if not username.endswith("@kean.edu"):
            error = "⚠ The username must end with @kean.edu！"
        else:
            is_student = manager.is_student_account(username)
            if manager.authenticate_user(username, password, is_student):
                write_log(f"{username} logged in")
                welcome = f"Welcome, {username}!"
                user_role = "student" if is_student else "instructor"
            else:
                error = "⚠ Login failed. Please check your username and password."
        if error:
            # If there is an error, return the error message and keep the login interface visible
            return (gr.update(value=error, visible=True),
                    state_username, state_role,
                    gr.update(visible=True), gr.update(value="", visible=False),
                    gr.update(visible=False), gr.update(visible=False), gr.update(value=error, visible=True))
        else:
            # If login is successful, update the state and switch to the corresponding menu
            return (gr.update(value="", visible=False),
                    username, user_role,
                    gr.update(visible=False),  # Hide the login interface
                    gr.update(value=welcome, visible=True),
                    gr.update(visible=user_role == "student"),
                    gr.update(visible=user_role == "instructor"),
                    # gr.update(visible=True) if user_role == "student" else gr.update(visible=False),
                    # gr.update(visible=True) if user_role == "instructor" else gr.update(visible=False),
                    gr.update(value="", visible=False))


    login_submit.click(on_login_submit,
                       inputs=[login_username, login_password],
                       outputs=[login_error, state_username, state_role, login_frame,
                                student_welcome, student_frame, instructor_frame, login_error])


    # Student Menu Button Event: Enroll in Course
    def on_stud_enroll():
        # Clear the course selection area and reset the search box
        return (gr.update(visible=True),  
                gr.update(visible=False),  
                gr.update(visible=False),
                gr.update(visible=False),
                "",  
                gr.update(choices=[], value=None, visible=False),  
                gr.update(visible=False),  
                gr.update(value="", visible=False))  


    stud_enroll.click(on_stud_enroll,
                      inputs=None,
                      outputs=[stud_enroll_section, stud_view_section, stud_drop_section, stud_ask_section,
                               enroll_search, enroll_course_list, enroll_confirm_btn, enroll_status])


    # Student menu button event: View courses
    def on_stud_view(username):
        courses = manager.get_student_courses(username)
        if not courses:
            content = "*(You haven't taken any courses yet.)*"
        else:
            lines = [f"- **{course}** - Grade: {grade if grade else 'Not assigned'}"
                     for course, grade in courses.items()]
            content = "\n".join(lines)
        return (gr.update(value=content, visible=True),
                gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))


    stud_view.click(on_stud_view,
                    inputs=state_username,
                    outputs=[view_courses_text, stud_enroll_section, stud_view_section, stud_drop_section,
                             stud_ask_section])


    # Student Menu Button Event: Drop Course
    def on_stud_drop(username):
        courses = manager.get_student_courses(username)
        if not courses:
            # No courses can be withdrawn
            return (gr.update(choices=[], visible=False), 
                    gr.update(value="*(You currently have no selected courses.)*", visible=True),
                    gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=True),
                    gr.update(visible=False))
        else:
            course_list = list(courses.keys())
            return (gr.update(choices=course_list, value=None, visible=True),
                    gr.update(value="", visible=False),  
                    gr.update(visible=True),  
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=True),
                    gr.update(visible=False))



    stud_drop.click(on_stud_drop,
                    inputs=state_username,
                    outputs=[drop_course_select, drop_status, drop_confirm_btn,
                             stud_enroll_section, stud_view_section, stud_drop_section, stud_ask_section])


    # Student Menu Button Event: Ask AI
    def on_stud_ask():
        # Open the question area and clear the previous answer
        return (gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True),
                "",  
                gr.update(value="", visible=False))  


    stud_ask.click(on_stud_ask,
                   inputs=None,
                   outputs=[stud_enroll_section, stud_view_section, stud_drop_section, stud_ask_section,
                            ask_question, ask_response])


    # Student Course Selection: Search for Courses Event
    def on_search_courses(keyword):
        matches = manager.search_courses(keyword)
        if not matches:
            return (gr.update(choices=[], visible=False),  
                    gr.update(visible=False),  
                    gr.update(value="*(No matching courses found.)*", visible=True))
        else:
            return (gr.update(choices=matches, value=None, visible=True),
                    gr.update(visible=True),  
                    gr.update(value="", visible=False))  


    enroll_search_btn.click(on_search_courses,
                            inputs=enroll_search,
                            outputs=[enroll_course_list, enroll_confirm_btn, enroll_status])


    # Student Course Selection: Confirmation of Course Selection Event
    def on_enroll_course(username, course_name):
        if not course_name:
            return gr.update(value="⚠ Please select the courses before submitting.", visible=True)
        if course_name not in manager.courses:
            return gr.update(value="⚠ The course is ineffective. Please choose another one.", visible=True)
        enrolled = manager.get_student_courses(username)
        if course_name in enrolled:
            return gr.update(value="⚠ You have already selected this course.", visible=True)
        manager.enroll_student(username, course_name)
        write_log(f"{username} enrolled in {course_name}")
        email_body = (f"Dear {username},\n\n"
                      f"Congratulations! You have successfully enrolled in the course: {course_name}. "
                      f"\nPlease take some time to review the course details and ensure that it aligns with your academic goals. "
                      f"You can do this by logging into your Kean account.\n\n"
                      f"Sincerely,\nKean University")
        try:
            send_enrollment_email(username, email_body)
        except Exception as e:
            print(f"[Warning] Failed to send enrollment email: {e}")
        return gr.update(value=f"✅ Successfully enrolled in **{course_name}**.", visible=True)


    enroll_confirm_btn.click(on_enroll_course,
                             inputs=[state_username, enroll_course_list],
                             outputs=enroll_status)


   # Student Withdrawal: Confirming the Withdrawal Event
    def on_drop_course(username, course_name):
        if not course_name:
            return (gr.update(value="⚠ Please select the course.", visible=True),
                    gr.update(choices=[], visible=True), gr.update(visible=True))
        courses = manager.get_student_courses(username)
        # Double-checking to Verify the Effectiveness of the Course
        if course_name not in courses:
            return (gr.update(value="⚠ The course is not on your selected list.", visible=True),
                    gr.update(choices=[], visible=True), gr.update(visible=True))
        if courses[course_name] is not None:
            return (gr.update(value="⚠ This course has already been graded and cannot be dropped.", visible=True),
                    gr.update(choices=list(courses.keys()), visible=True), gr.update(visible=True))
        manager.drop_student_course(username, course_name)
        write_log(f"{username} dropped {course_name}")
        email_body = (f"Dear {username},\n\n"
                      f"You have successfully dropped the course: {course_name}. "
                      f"\nIf this was a mistake, please log into your Kean account to re-enroll in the course.\n\n"
                      f"Sincerely,\nKean University")
        try:
            send_enrollment_email(username, email_body)
        except Exception as e:
            print(f"[Warning] Failed to send drop email: {e}")

        remaining_courses = manager.get_student_courses(username)
        if remaining_courses:
            new_list = list(remaining_courses.keys())
            success_msg = f"✅ Has withdrawn from the selection. **{course_name}**."
            return (gr.update(value=success_msg, visible=True),
                    gr.update(choices=new_list, value=None, visible=True),
                    gr.update(visible=True))
        else:

            return (gr.update(value=f"✅ Has withdrawn from the selection. **{course_name}**. You are not currently taking any other courses.", visible=True),
                    gr.update(choices=[], visible=False),
                    gr.update(visible=False))


    drop_confirm_btn.click(on_drop_course,
                           inputs=[state_username, drop_course_select],
                           outputs=[drop_status, drop_course_select, drop_confirm_btn])


    # Student's Question for AI: Submitting an Event
    def on_ask_submit(username, question):
        if not question or question.strip() == "":
            return gr.update(value="⚠ Please enter a question first.", visible=True)
        # Building AI Prompt
        courses = manager.get_student_courses(username)
        course_info_lines = [f"{c} - {('Not assigned' if grade is None else grade)}" for c, grade in courses.items()]
        course_info = "\n".join(course_info_lines)
        student = manager.get_student_by_username(username)
        plan_text = ""
        if student and student.major:
            plan_file = f"{student.major}_plan.txt"
            try:
                with open(plan_file, "r", encoding="utf-8") as f:
                    plan_text = f.read()
            except FileNotFoundError:
                plan_text = ""
                no_plan_note = f"*No major plan found for {student.major}.*\n\n"
            else:
                no_plan_note = ""
        else:
            no_plan_note = ""
        prompt = (f'I am a student asking the following academic question:\n"{question}"\n'
                  f'My current course history:\n{course_info}\n'
                  f'Here is the four-year plan for my major:\n{plan_text}\n'
                  f'Based on my question, my course history, and the plan above, give me a suggestion.')
        
        reply = ask_ai_question(prompt)
        
        advice_header = "**AI ADVICE:**\n\n"
        response_text = (no_plan_note if 'no_plan_note' in locals() else "") + reply.strip()
        return gr.update(value=advice_header + response_text, visible=True)


    ask_submit_btn.click(on_ask_submit,
                         inputs=[state_username, ask_question],
                         outputs=[ask_response])


    # Teacher Menu: "View Student Courses" Button Event
    def on_inst_view():
        student_list = manager.list_all_students()
        return (
            gr.update(choices=student_list, value=None),  
            gr.update(choices=student_list, value=None),  
            gr.update(visible=True),  
            gr.update(visible=False), 
            gr.update(value="", visible=False)  
        )


    inst_view.click(
        on_inst_view,
        inputs=None,
        outputs=[
            view_student_select, 
            assign_student_select,  
            inst_view_section, 
            inst_assign_section,  
            assign_status  
        ]
    )


    # Teacher Menu: Register Grades Button Event
    def on_inst_assign():
        
        student_list = manager.list_all_students()
        return (gr.update(choices=student_list, value=None),
                gr.update(choices=[], value=None, visible=False),  
                gr.update(value=None, visible=False),  
                gr.update(visible=False),  
                gr.update(value="", visible=False),  
                gr.update(visible=False), gr.update(visible=True))
        # output: assign_student_select.options, assign_course_select, assign_grade_select, assign_grade_btn, assign_status, inst_view_section, inst_assign_section


    inst_assign.click(on_inst_assign,
                      inputs=None,
                      outputs=[assign_student_select, assign_course_select, assign_grade_select, assign_grade_btn,
                               assign_status, inst_view_section, inst_assign_section])


    # Teacher: Event to display course list after selecting students
    def on_select_student_for_grade(student_name):
        if not student_name:
            return (gr.update(choices=[], visible=False),
                    gr.update(choices=[], visible=False),
                    gr.update(visible=False),
                    gr.update(value="", visible=False))
        courses = manager.get_student_courses(student_name)
        if not courses:
            # no class
            return (gr.update(choices=[], visible=False),
                    gr.update(choices=ALLOWED_GRADES, visible=False),
                    gr.update(visible=False),
                    gr.update(value=f"*(No courses found for {student_name}.)*", visible=True))
        course_list = list(courses.keys())
        return (gr.update(choices=course_list, value=None, visible=True),
                gr.update(choices=ALLOWED_GRADES, value="A", visible=True),
                gr.update(visible=True),
                gr.update(value="", visible=False))
        # output: assign_course_select, assign_grade_select, assign_grade_btn, assign_status


    assign_student_select.change(on_select_student_for_grade,
                                 inputs=assign_student_select,
                                 outputs=[assign_course_select, assign_grade_select, assign_grade_btn, assign_status])


    # Teacher: Submission of Grades Event
    def on_assign_grade(student_name, course_name, grade):
        if not student_name or not course_name or not grade:
            return gr.update(value="⚠ Please select all the students, courses and grades.", visible=True)
        student_courses = manager.get_student_courses(student_name)
        if course_name not in student_courses:
            return gr.update(value="⚠ Students who have not taken this course cannot register for the grades.", visible=True)
        if grade not in ALLOWED_GRADES:
            return gr.update(value="⚠ The score value is invalid. Please select again.", visible=True)
        manager.set_student_grade(student_name, course_name, grade)
        write_log(f"Assigned grade {grade} to {student_name} for {course_name}")
       
        email_body = (f"Dear {student_name},\n\n"
                      f"You received grade '{grade}' for course {course_name}. "
                      f"\nPlease take some time to review and confirm your grade to ensure that it aligns with your academic goals. "
                      f"You can do this by logging into your Kean account.\n\n"
                      f"Sincerely,\nKean University")
        try:
            send_grade_email(student_name, email_body)
        except Exception as e:
            print(f"[Warning] Failed to send grade email: {e}")
       
        success_msg = f"✅ The grades for the course **{course_name}** of **{student_name}** have been registered. **{grade}**."
        return gr.update(value=success_msg, visible=True)


    assign_grade_btn.click(on_assign_grade,
                           inputs=[assign_student_select, assign_course_select, assign_grade_select],
                           outputs=[assign_status])


    # Student/Teacher Logout Event (Both buttons can use the same function)
    def on_logout():
        
        manager.save_enrollments()
        
        return ("", "",  
                gr.update(visible=False), gr.update(visible=False),  
                gr.update(visible=True), 
                gr.update(value="Account has been deactivated. Please log in again.", visible=True))


    stud_exit.click(on_logout,
                    inputs=None,
                    outputs=[state_username, state_role, student_frame, instructor_frame, main_menu, main_menu_msg])
    inst_exit.click(on_logout,
                    inputs=None,
                    outputs=[state_username, state_role, student_frame, instructor_frame, main_menu, main_menu_msg])


if __name__ == "__main__":
    demo.launch()
