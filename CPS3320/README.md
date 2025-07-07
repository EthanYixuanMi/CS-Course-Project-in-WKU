# SmartCourse: Course Selection System with AI Suggestion Module

## Introduction

SmartCourse is a university course management system designed to streamline course selection and academic planning for students and instructors. It allows students to register accounts, search and enroll in courses, view enrolled courses and grades, and drop courses as needed. Instructors can manage course enrollments by viewing student selections and assigning grades. A standout feature is the integrated AI suggestion module, providing personalized course advice based on academic history and major-specific plans.

## Key Features

### Account Creation with Email Validation

* Accounts created using official university email (`@kean.edu`).
* Instructor accounts protected by a security code during registration.

### Secure Login and Authentication

* Password-based authentication verified against stored credentials.
* Email domain enforced at login.

### Student Functions

* **Course Search & Enrollment:**

  * Keyword search of course catalog.
  * Enrollment validation to prevent duplicate registrations.
  * Email notification upon enrollment.

* **View Enrolled Courses and Grades:**

  * List enrolled courses with current grades or "Not assigned."

* **Drop Courses:**

  * Drop ungraded courses only.
  * Schedule updates and email confirmation upon dropping.

* **AI Academic Advice:**

  * AI-generated course recommendations based on academic history and major-specific plans.

### Instructor Functions

* **View Student Enrollments:**

  * Access enrolled courses and grades for individual students.

* **Assign Grades:**

  * Grade submission validated against standard grading scales.
  * Notifications sent to students upon grade assignment.

### Email Notifications for Key Events

* Automated email alerts for enrollments, dropped courses, and new grades.
* Customizable SMTP email settings.

### Multiple Interfaces – CLI and GUI

* **Command-Line Interface (CLI):**

  * Terminal-based access, lightweight and suitable for quick or remote usage.

* **Graphical User Interface (GUI) with Gradio:**

  * Intuitive, point-and-click web interface.
  * Form fields and dropdown menus for easy interaction.

## Installation and Setup

### Prerequisites

* Python 3.8+
* Required packages:

```bash
pip install gradio requests
```

### Project Files

Ensure these files are in your project directory:

* `course_list.txt`: Course catalog.
* `account.txt`: User accounts (auto-created).
* `enrolled_courses.txt`: Student enrollments and grades.
* *(Optional)* Major-specific plan files (e.g., `cps_plan.txt`).

## Running the Application

### CLI Mode

Run the following command:

```bash
python main.py
```

* Use numeric options to navigate menus after logging in or registering.

### Gradio GUI Mode

Run the following command:

```bash
python ui_gradio.py
```

* Open the local URL provided (e.g., `http://127.0.0.1:7860/`).
* Interactive menus for login, registration, and course management.

## AI Suggestion Module Setup

* Requires Ollama installed with `deepseek-r1:1.5b` model.
* Ensure Ollama service runs locally (default port: `11434`).
* SmartCourse sends student data to the model for tailored advice.
* Error messages displayed if the AI service is unavailable.

SmartCourse provides a seamless, AI-driven platform for university course management, enhancing academic planning and course selection for students and instructors alike.
