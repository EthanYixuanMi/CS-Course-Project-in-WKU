package Project;

import java.io.*;
import java.util.*;

public class Reproduce_KeanWISE {
    public static void main(String[] args) {
        CourseManager courseManager = new CourseManager();
        Scanner input = new Scanner(System.in);

        boolean authenticated = false;
        String username = null;
        boolean ifStudent = false;

        System.out.println("Welcome to KeanWISE!");

        while (!authenticated) {
            System.out.print("Enter your username (or \"new\" to create a new account): ");
            username = input.nextLine();

            // If user choose to create a new account, ask for username, password, and identity
            if (username.equals("new")) {
                System.out.print("Enter your username: ");
                String newUsername = input.nextLine();
                System.out.print("Enter your password: ");
                String newPassword = input.nextLine();
                System.out.print("What's your identity? (student or instructor): ");
                String identity = input.nextLine();
                ifStudent = identity.equals("student");

                // Create a new account
                courseManager.createAccount(newUsername, newPassword, ifStudent);

                // Record the log to the log file
                log("Created new account for " + newUsername);
                System.out.println("Account created! Please log in.");
            } else {
                System.out.print("Enter your password: ");
                String password = input.nextLine();

                ifStudent = courseManager.isStudent(username);
                if (courseManager.authenticate(username, password, ifStudent)) {
                    authenticated = true;

                    // Record the log to the log file
                    log(username + " successfully logged in.");
                    System.out.println("Welcome, " + username + "!");
                } else {
                    System.out.println("Invalid username or password. Please try again.");
                }
            }
        }

        while (true) {
            if (ifStudent) {
                studentMenu(courseManager, username, input);
            } else {
                instructorMenu(courseManager, input);
            }
        }
    }

    public static void studentMenu(CourseManager courseManager, String username, Scanner input) {
        System.out.println("\nStudent Menu:");
        System.out.println("1. Enroll in a course");
        System.out.println("2. View enrolled courses");
        System.out.println("3. Drop a course");
        System.out.println("4. Exit");

        System.out.print("Enter your choice: ");
        int choice = input.nextInt();
        input.nextLine();

        switch (choice) {
            case 1:
                System.out.print("Enter the course you want to enroll (or press enter to see all courses): ");
                String search = input.nextLine();
                ArrayList<String> availableCourses = courseManager.searchCourses(search);
                if (availableCourses.isEmpty()) {
                    System.out.println("No courses found. Try again.");
                } else {
                    for (String course : availableCourses) {
                        System.out.println(course);
                    }
                    System.out.print("Enter the course to enroll: ");
                    String course = input.nextLine();
                    if (courseManager.getCourses().contains(course)) {
                        courseManager.enrollCourse(username, course);
                        log(username + " enrolled in " + course);
                        System.out.println("You have enrolled in " + course);
                    } else {
                        System.out.println("Course not found. Try again.");
                    }
                }
                break;
            case 2:
                System.out.println("Here are the courses you have enrolled:");
                ArrayList<String> enrolledCourses = courseManager.getEnrolledCourses(username);
                for (String enrolledCourse : enrolledCourses) {
                    System.out.println(enrolledCourse);
                }
                break;
            case 3:
                System.out.println("Here are the courses you have enrolled:");
                ArrayList<String> coursesToDrop = courseManager.getEnrolledCourses(username);
                for (String enrolledCourse : coursesToDrop) {
                    System.out.println(enrolledCourse);
                }
                System.out.print("Enter the course you want to drop: ");
                String dropCourse = input.nextLine();
                if (coursesToDrop.contains(dropCourse)) {
                    courseManager.dropCourse(username, dropCourse);
                    log(username + " dropped " + dropCourse);
                    System.out.println("You have dropped " + dropCourse);
                } else {
                    System.out.println("You are not enrolled in that course.");
                }
                break;
            case 4:
                System.out.println("Goodbye!");
                courseManager.saveData();
                System.exit(0);
            default:
                System.out.println("Invalid choice. Please try again.");
        }
    }

    public static void instructorMenu(CourseManager courseManager, Scanner input) {
        System.out.println("\nInstructor Menu:");
        System.out.println("1. View student's enrolled courses");
        System.out.println("2. Exit");

        System.out.print("Enter your choice: ");
        int choice = input.nextInt();
        input.nextLine();

        switch (choice) {
            case 1:
                System.out.println("Here are the students:");
                for (Student student : courseManager.getStudents()) {
                    System.out.println(student.getUsername());
                }
                System.out.print("Enter the student's username to view their enrolled courses: ");
                String studentUsername = input.nextLine();
                ArrayList<String> studentCourses = courseManager.getEnrolledCourses(studentUsername);
                if (studentCourses != null) {
                    System.out.println(studentUsername + " has enrolled in:");
                    for (String course : studentCourses) {
                        System.out.println(course);
                    }
                } else {
                    System.out.println("Student not found. Try again.");
                }
                break;
            case 2:
                System.out.println("Goodbye!");
                courseManager.saveData();
                System.exit(0);
            default:
                System.out.println("Invalid choice. Please try again.");
        }
    }

    public static void log(String message) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\Users\\25097\\OneDrive\\Desktop\\Log.txt", true))) {
            writer.write(new Date() + ": " + message);
            writer.newLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

class Student {
    String username;
    String password;
    ArrayList<String> enrolledCourses;

    public Student(String username, String password) {
        this.username = username;
        this.password = password;
        this.enrolledCourses = new ArrayList<>();
    }

    public void addEnrolledCourse(String course) {
        enrolledCourses.add(course);
    }

    public void dropEnrolledCourse(String course) {
        enrolledCourses.remove(course);
    }

    public String getUsername() {
        return username;
    }

    public ArrayList<String> getEnrolledCourses() {
        return enrolledCourses;
    }
}

class Instructor {
    String username;
    String password;

    public Instructor(String username, String password) {
        this.username = username;
        this.password = password;
    }

    public String getUsername() {
        return username;
    }
}

class CourseManager {
    ArrayList<String> courses;
    ArrayList<Student> students;
    ArrayList<Instructor> instructors;

    public CourseManager() {
        courses = loadCourses("C:\\Users\\25097\\OneDrive\\Desktop\\Course_list.txt");
        students = new ArrayList<>();
        instructors = new ArrayList<>();

        // Load accounts from files
        loadAccounts("C:\\Users\\25097\\OneDrive\\Desktop\\Account.txt");

        // Load enrolled courses from files
        loadEnrolledCourses("C:\\Users\\25097\\OneDrive\\Desktop\\EnrolledCourses.txt");
    }

    private ArrayList<String> loadCourses(String filename) {
        ArrayList<String> courseList = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;

            // Read each line from the file and add it to the course list
            while ((line = reader.readLine()) != null) {
                courseList.add(line.trim());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return courseList;
    }

    private void loadAccounts(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;

            // Read each line from the file and add the account to the corresponding list
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");

                // Check if the line has the correct format
                if (parts.length == 3) {
                    String username = parts[0].trim();
                    String password = parts[1].trim();
                    boolean isStudent = parts[2].trim().equals("student");
                    if (isStudent) {
                        students.add(new Student(username, password));
                    } else {
                        instructors.add(new Instructor(username, password));
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void loadEnrolledCourses(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;

            // Read each line from the file and add the enrolled course to the corresponding student
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 2) {
                    String username = parts[0].trim();
                    String course = parts[1].trim();
                    for (Student student : students) {
                        if (student.getUsername().equals(username)) {
                            student.addEnrolledCourse(course);
                        }
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void createAccount(String username, String password, boolean isStudent) {
        if (isStudent) {
            students.add(new Student(username, password));
        } else {
            instructors.add(new Instructor(username, password));
        }
        saveAccount(username, password, isStudent);
    }

    private void saveAccount(String username, String password, boolean isStudent) {
        // Save the account to the file
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\Users\\25097\\OneDrive\\Desktop\\Account.txt", true))) {
            writer.write(username + "," + password + "," + (isStudent ? "student" : "instructor"));
            writer.newLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public boolean authenticate(String username, String password, boolean isStudent) {
        if (isStudent) {
            for (Student student : students) {
                if (student.getUsername().equals(username) && student.password.equals(password)) {
                    return true;
                }
            }
        } else {
            for (Instructor instructor : instructors) {
                if (instructor.getUsername().equals(username) && instructor.password.equals(password)) {
                    return true;
                }
            }
        }
        return false;
    }

    public boolean isStudent(String username) {
        for (Student student : students) {
            if (student.getUsername().equals(username)) {
                return true;
            }
        }
        return false;
    }

    public ArrayList<Instructor> getInstructors() {
        return instructors;
    }

    public ArrayList<Student> getStudents() {
        return students;
    }

    public ArrayList<String> getCourses() {
        return courses;
    }

    public ArrayList<String> searchCourses(String keyword) {
        ArrayList<String> result = new ArrayList<>();
        for (String course : courses) {
            if (keyword.isEmpty() || course.contains(keyword)) {
                result.add(course);
            }
        }
        return result;
    }

    public void enrollCourse(String username, String course) {
        for (Student student : students) {
            if (student.getUsername().equals(username)) {
                student.addEnrolledCourse(course);
                saveEnrolledCourse(username, course);
            }
        }
    }

    private void saveEnrolledCourse(String username, String course) {
        // Save the enrolled course to the file
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\Users\\25097\\OneDrive\\Desktop\\EnrolledCourses.txt", true))) {
            writer.write(username + "," + course);
            writer.newLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void dropCourse(String username, String course) {
        for (Student student : students) {
            if (student.getUsername().equals(username)) {
                student.dropEnrolledCourse(course);
                saveAllEnrolledCourses();
            }
        }
    }

    private void saveAllEnrolledCourses() {
        // Save all enrolled courses to the file
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\Users\\25097\\OneDrive\\Desktop\\EnrolledCourses.txt"))) {
            for (Student student : students) {
                for (String course : student.getEnrolledCourses()) {
                    writer.write(student.getUsername() + "," + course);
                    writer.newLine();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public ArrayList<String> getEnrolledCourses(String username) {
        for (Student student : students) {
            if (student.getUsername().equals(username)) {
                return student.getEnrolledCourses();
            }
        }
        return null;
    }

    public void saveData() {
        saveAllEnrolledCourses();
    }
}
