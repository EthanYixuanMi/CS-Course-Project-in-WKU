# Reproduce\_KeanWISE (Java CLI Student System)

A command-line Java application that simulates a simplified version of **KeanWISE**, a university student/faculty portal. This program allows users to register/login, manage courses, and simulate basic student and faculty interactions with a university information system.

## Features

* Account creation and authentication for both **students** and **faculty**
* Student capabilities:

  * Register for courses
  * View enrolled courses
  * Drop courses
* Faculty capabilities:

  * Create and delete courses
  * View enrolled students
* Data persistence using text files (`users.txt`, `courses.txt`)

## Project Structure

All Java classes are implemented within a single file:

```
├── Reproduce_KeanWISE.java      # Contains main method and all supporting classes
├── Account.txt                  # Store all accounts and their corresponding passwords
├── Course_list.txt              # List all courses that may be selected
├── EnrolledCourses.txt          # Store all enrolled courses with their corresponding account
├── Log.txt                      # Record all operations
```

## Getting Started

### 1. Download the Repository

### 2. Compile

```bash
javac Reproduce_KeanWISE.java
```

### 3. Run

```bash
java Reproduce_KeanWISE
```

### 4. Follow the CLI Prompts

* Log in or create a new account
* Select your identity (student or faculty)
* Perform role-specific actions like course registration or creation

## Requirements

* Java JDK 8 or higher
* Terminal or command-line environment

## Notes

* All user and course data is saved in the provided `users.txt` and `courses.txt` files in the root of the repository.
* This is a standalone educational simulation project—no external libraries or frameworks required.
