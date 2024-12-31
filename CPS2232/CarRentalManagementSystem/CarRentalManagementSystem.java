package Project;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;
import java.util.Date;

public class CarRentalManagementSystem {
    public static void main(String[] args) {
        RentalManager rentalManager = new RentalManager();
        Scanner input = new Scanner(System.in);

        boolean authenticated = false;
        String username = null;
        boolean isAdmin = false;

        System.out.println("Welcome to the Car Rental Management System!");

        while (!authenticated) {
            System.out.print("Enter your email (or \"new\" to create a new account): ");
            username = input.nextLine();

            if (username.equals("new")) {
                System.out.print("Enter your email: ");
                String newEmail = input.nextLine();
                System.out.print("Enter your password: ");
                String newPassword = input.nextLine();
                System.out.print("What's your role? (user or admin, if you are admin, type \"admin\" exactly; " +
                        "otherwise you will be user): ");
                String role = input.nextLine();
                isAdmin = role.equalsIgnoreCase("admin");

                if (isAdmin) {
                    System.out.print("Enter the admin verification password: ");
                    String adminVerificationPassword = input.nextLine();
                    if (!adminVerificationPassword.equals("Ethan12345")) {
                        System.out.println("Invalid admin verification password. Account creation failed.");
                        continue;
                    }
                }

                rentalManager.createAccount(newEmail, newPassword, isAdmin, 0);
                log("Created new account for " + newEmail);
                System.out.println("Account created! Please log in.");
            } else {
                System.out.print("Enter your password: ");
                String password = input.nextLine();
                isAdmin = rentalManager.isAdmin(username);

                if (rentalManager.authenticate(username, password)) {
                    authenticated = true;
                    log(username + " successfully logged in.");
                    System.out.println("Welcome, " + username + "!");
                } else {
                    System.out.println("Invalid email or password. Please try again.");
                }
            }
        }

        while (true) {
            if (isAdmin) {
                adminMenu(rentalManager, input);
            } else {
                userMenu(rentalManager, username, input);
            }
        }
    }

    public static void adminMenu(RentalManager rentalManager, Scanner input) {
        System.out.println("\nAdmin Menu:");
        System.out.println("1. Add a vehicle");
        System.out.println("2. Remove a vehicle");
        System.out.println("3. View all vehicles");
        System.out.println("4. View rental logs");
        System.out.println("5. Exit");

        System.out.print("Enter your choice: ");
        int choice = input.nextInt();
        input.nextLine();

        switch (choice) {
            case 1:
                System.out.print("Enter vehicle details (format: Brand,Model,Color,Capacity,RentPrice,Length,Width): ");
                String vehicleDetails = input.nextLine();
                rentalManager.addVehicle(vehicleDetails);
                log("Admin added a new vehicle: " + vehicleDetails);
                break;
            case 2:
                System.out.print("Enter vehicle ID to remove: ");
                int vehicleId = input.nextInt();
                rentalManager.removeVehicle(vehicleId);
                log("Admin removed vehicle ID: " + vehicleId);
                break;
            case 3:
                rentalManager.listVehicles();
                break;
            case 4:
                rentalManager.viewLogs();
                break;
            case 5:
                System.out.println("Goodbye!");
                System.exit(0);
            default:
                System.out.println("Invalid choice. Please try again.");
        }
    }

    public static void userMenu(RentalManager rentalManager, String username, Scanner input) {
        System.out.println("\nUser Menu:");
        System.out.println("1. View all vehicles");
        System.out.println("2. View vehicle details");
        System.out.println("3. Rent a vehicle");
        System.out.println("4. Return a vehicle");
        System.out.println("5. Exit");

        System.out.print("Enter your choice: ");
        int choice = input.nextInt();
        input.nextLine();

        switch (choice) {
            case 1:
                rentalManager.listVehicles();
                break;
            case 2:
                System.out.print("Enter vehicle ID to view details: ");
                int vehicleId = input.nextInt();
                rentalManager.viewVehicleDetails(vehicleId);
                break;
            case 3:
                System.out.print("Enter vehicle ID to rent: ");
                int rentVehicleId = input.nextInt();
                System.out.print("Enter rental period (in days): ");
                int rentalPeriod = input.nextInt();
                rentalManager.rentVehicle(username, rentVehicleId, rentalPeriod);
                break;
            case 4:
                System.out.print("Enter vehicle ID to return: ");
                int returnVehicleId = input.nextInt();
                rentalManager.returnVehicle(username, returnVehicleId);
                break;
            case 5:
                System.out.println("Goodbye!");
                System.exit(0);
            default:
                System.out.println("Invalid choice. Please try again.");
        }
    }

    public static void log(String message) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\Users\\Ethan\\Desktop\\Log.txt", true))) {
            writer.write(new Date() + ": " + message);
            writer.newLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
