# Car Rental Management System (CRMS)

## Project Overview

The Car Rental Management System (CRMS) is designed to enhance operational efficiency and user experience within the vehicle rental industry. This Java-based system supports car rental companies (administrators) and customers (users) by providing intuitive interfaces for vehicle management, rental transactions, and user authentication.

## Key Features

* **User Roles and Authentication**:

  * Admin: Manage vehicles, view rental logs, and maintain user accounts.
  * Customer: Register, browse available vehicles, rent vehicles, and return vehicles.

* **Vehicle Management**:

  * Administrators can add, view, update, and remove vehicles.
  * Vehicles have detailed attributes like brand, model, color, capacity, rental price, and size.

* **Rental Transactions**:

  * Users can rent and return vehicles.
  * Automatic updates of vehicle availability.

* **Notification System**:

  * Integrated with JavaMail API for sending rental confirmations and account notifications via email.

* **Persistent Storage**:

  * Uses file-based storage for vehicle and user data (Vehicles.txt, Accounts.txt).
  * Transaction logs maintained in Log.txt.

## Technologies Used

* **Java** (primary programming language)
* **JavaMail API** (email notifications)
* **ArrayList** (dynamic data handling)
* **File I/O** (persistent data storage)

## Project Structure

* `CarRentalManagementSystem.java`: Main class, handles user interaction and program initialization.
* `RentalManager.java`: Manages rental transactions, vehicle data, and email notifications.
* `User.java`: Represents user information, including authentication and role management.
* `Vehicle.java`: Defines vehicle attributes and availability management.

## Installation and Usage

### Requirements

* Java SE (version 8 or higher)
* JavaMail API

### Setup

1. Clone the repository or download source files.
2. Ensure `Vehicles.txt`, `Accounts.txt`, and `Log.txt` exist in the project's root directory.
3. Configure your SMTP server details in the `RentalManager` class for email notifications.

### Running the Application

* Compile the Java files:

  ```
  javac *.java
  ```
* Execute the main program:

  ```
  java CarRentalManagementSystem
  ```

## Functionalities

### Admin Features

* Add/Delete vehicles
* View all vehicles
* Access transaction logs

### Customer Features

* Account creation and login
* Browse available vehicles
* Rent and return vehicles
* Receive transaction confirmation emails

## Future Enhancements

* Improve email notification reliability
* Enhanced filtering and search functionality
* Expansion of the system to support more advanced management features

## Contact

* Project Main Contributor: Mi Yixuan
* Email: miy@kean.edu

---

This project demonstrates efficient use of data structures and Java programming concepts to deliver a robust solution tailored to the needs of the car rental industry.
