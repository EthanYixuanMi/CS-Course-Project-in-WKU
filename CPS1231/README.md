# FinalProject - Student Course Management System

## 📌 Introduction

This is a simple **console-based student course management system** developed in Java. It allows users to create accounts, log in as students or teachers, and manage course registration and student information through a text-based menu interface.

## 🚀 Features

* 🧑‍🎓 **Student Functionality**

  * Register new account
  * Login
  * View available courses
  * Enroll in a course
  * Drop a course
  * View enrolled courses

* 👩‍🏫 **Instructor Functionality**

  * Login
  * View list of all students
  * View which courses a student has enrolled in

* 💾 **Persistent Storage**

  * Student and instructor data are stored in `.txt` files
  * Courses and enrollment data are stored and loaded automatically

## 📂 Project Structure

```bash
FinalProject.java       # Main Java file containing all logic and classes
account.txt             # Stores user credentials
course_list.txt         # Stores all course information
enrolled_courses.txt    # Stores student-course enrollment relationships
log.txt                 # Optional log file for tracking operations
```

## 🔧 How to Run

1. Make sure you have JDK installed (Java 8+).
2. Compile the project:

   ```bash
   javac FinalProject.java
   ```
3. Run the program:

   ```bash
   java FinalProject
   ```

## ✅ Example Use Case

* A student logs in and enrolls in `CPS 1231`.
* A teacher logs in and checks which students are enrolled in `CPS 1231`.

## 📌 Notes

* No GUI is included — all operations happen in the terminal.
* This project is ideal for learning Java file I/O, object-oriented programming, and basic console interactions.
