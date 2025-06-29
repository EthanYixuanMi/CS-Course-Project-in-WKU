package Project;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Date;
import javax.mail.*;
import javax.mail.internet.*;
import javax.mail.Session;
import javax.mail.Transport;
import java.util.Properties;

public class RentalManager {
    private ArrayList<Vehicle> vehicles;
    private ArrayList<String> logs;
    private ArrayList<User> users;

    public RentalManager() {
        vehicles = new ArrayList<>();
        logs = new ArrayList<>();
        users = new ArrayList<>();
        loadVehicles();
        loadAccounts();
    }

    // Load vehicles information from file
    private void loadVehicles() {
        try (BufferedReader reader = new BufferedReader(new FileReader("C:\\Users\\Ethan\\Desktop\\Vehicles.txt"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 9) {
                    int id = Integer.parseInt(parts[0].trim());
                    String brand = parts[1].trim();
                    String model = parts[2].trim();
                    String color = parts[3].trim();
                    int capacity = Integer.parseInt(parts[4].trim());
                    double price = Double.parseDouble(parts[5].trim());
                    double length = Double.parseDouble(parts[6].trim());
                    double width = Double.parseDouble(parts[7].trim());
                    String isAvailable = parts[8].trim();
                    vehicles.add(new Vehicle(id, brand, model, color, capacity, price, length, width, isAvailable));
                }
            }
        } catch (IOException e) {
            System.out.println("Error loading vehicles: " + e.getMessage());
        }
    }

    // Load accounts information from file
    private void loadAccounts() {
        try (BufferedReader reader = new BufferedReader(new FileReader("C:\\Users\\Ethan\\Desktop\\Accounts.txt"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 4) {
                    String email = parts[0].trim();
                    String password = parts[1].trim();
                    boolean isAdmin = parts[2].trim().equalsIgnoreCase("admin");
                    int numOfRentals = Integer.parseInt(parts[3].trim());
                    users.add(new User(email, password, isAdmin, numOfRentals));
                }
            }
        } catch (IOException e) {
            System.out.println("Error loading accounts: " + e.getMessage());
        }
    }

    // Create account
    public void createAccount(String email, String password, boolean isAdmin, int numOfRentCars) {
        users.add(new User(email, password, isAdmin, 0));
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\Users\\Ethan\\Desktop\\Accounts.txt", true))) {
            writer.write(email + "," + password + "," + (isAdmin ? "admin" : "user") + "," + numOfRentCars);
            writer.newLine();
        } catch (IOException e) {
            System.out.println("Error saving account: " + e.getMessage());
        }
    }

    // Authenticate user
    public boolean authenticate(String email, String password) {
        for (User user : users) {
            if (user.getEmail().equals(email) && user.getPassword().equals(password)) {
                return true;
            }
        }
        return false;
    }

    public boolean isAdmin(String email) {
        for (User user : users) {
            if (user.getEmail().equals(email)) {
                return user.isAdmin();
            }
        }
        return false;
    }

    // List all vehicles
    public void listVehicles() {
        System.out.println("-------------------------------------------------------------------------------------------------");
        System.out.printf("| %-4s | %-14s | %-12s | %-8s | %-9s | %-9s | %-7s | %-7s |\n",
                "ID", "Brand", "Model", "Color", "Capacity", "RentPrice", "Length", "Width");
        System.out.println("-------------------------------------------------------------------------------------------------");

        for (Vehicle vehicle : vehicles) {
            System.out.printf("| %-4d | %-14s | %-12s | %-8s | %-9d | %-9.2f | %-7.2f | %-7.2f |\n",
                    vehicle.getId(), vehicle.getBrand(), vehicle.getModel(), vehicle.getColor(),
                    vehicle.getPeopleCapacity(), vehicle.getRentPrice(), vehicle.getLength(), vehicle.getWidth());
        }
        System.out.println("-------------------------------------------------------------------------------------------------");
    }

    // View vehicle details
    public void viewVehicleDetails(int id) {
        // Iterate through the vehicles list to find the vehicle with the given ID
        for (Vehicle vehicle : vehicles) {
            if (vehicle.getId() == id) {
                System.out.println(vehicle);
                return;
            }
        }
        System.out.println("Vehicle not found!");
    }

    // Add vehicle
    public void addVehicle(String vehicleDetails) {
        String[] parts = vehicleDetails.split(",");
        if (parts.length == 7) {
            int id = vehicles.size() + 1;
            String brand = parts[0].trim();
            String model = parts[1].trim();
            String color = parts[2].trim();
            int capacity = Integer.parseInt(parts[3].trim());
            double price = Double.parseDouble(parts[4].trim());
            double length = Double.parseDouble(parts[5].trim());
            double width = Double.parseDouble(parts[6].trim());
            vehicles.add(new Vehicle(id, brand, model, color, capacity, price, length, width, "true"));
            saveVehicles();
            System.out.println("Vehicle added successfully!");
        } else {
            System.out.println("Invalid vehicle details!");
        }
    }

    // Delete vehicle
    public void removeVehicle(int id) {
        vehicles.removeIf(vehicle -> vehicle.getId() == id);
        saveVehicles();
        System.out.println("Vehicle removed successfully!");
    }

    // Save vehicles information to file
    private void saveVehicles() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\Users\\Ethan\\Desktop\\Vehicles.txt"))) {
            for (Vehicle vehicle : vehicles) {
                writer.write(vehicle.getId() + "," + vehicle.getBrand() + "," + vehicle.getModel() + "," +
                        vehicle.getColor() + "," + vehicle.getPeopleCapacity() + "," +
                        vehicle.getRentPrice() + "," + vehicle.getLength() + "," + vehicle.getWidth() + "," + vehicle.getIsAvailable());
                writer.newLine();
            }
        } catch (IOException e) {
            System.out.println("Error saving vehicles: " + e.getMessage());
        }
    }

    private void updateAccountFile() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\Users\\Ethan\\Desktop\\Accounts.txt"))) {
            for (User user : users) {
                writer.write(user.getEmail() + "," +
                        user.getPassword() + "," +
                        (user.isAdmin() ? "admin" : "user") + "," +
                        user.getNumOfRentCars());
                writer.newLine();
            }
        } catch (IOException e) {
            System.out.println("Error updating accounts file: " + e.getMessage());
        }
    }

    // Rent vehicle
    public void rentVehicle(String username, int vehicleId, int days) {
        for (Vehicle vehicle : vehicles) {
            if (vehicle.getId() == vehicleId && vehicle.getIsAvailable().equals("true")) {
                vehicle.setAvailable("false");

                for (User user : users) {
                    if (user.getEmail().equals(username)) {
                        user.setNumOfRentCars(user.getNumOfRentCars() + 1);
                        updateAccountFile();
                        break;
                    }
                }

                sendEmail(username, "Vehicle Rental Confirmation",
                        "You have rented the vehicle: " + vehicle.getBrand() + " " +
                                vehicle.getModel() + " for " + days + " days." + "\n" +
                                "Please return the vehicle on time." + "\n" + "Thank you!");
                saveVehicles();
                System.out.println("Vehicle rented successfully!");
                return;
            }
        }
        System.out.println("Vehicle not available!");
    }

    // Return vehicle
    public void returnVehicle(String username, int vehicleId) {
        for (Vehicle vehicle : vehicles) {
            for (User user : users) {
                if (user.getEmail().equals(username)) {
                    if (user.getNumOfRentCars() == 0) {
                        System.out.println("You have not rented any vehicles!");
                        return;
                    }

                    if (vehicle.getId() == vehicleId && vehicle.getIsAvailable().equals("false")) {
                        vehicle.setAvailable("true");

                        user.setNumOfRentCars(user.getNumOfRentCars() - 1);
                        updateAccountFile();

                        saveVehicles();
                        System.out.println("Vehicle returned successfully!");
                        return;
                    }
                }
            }
        }
        System.out.println("Invalid vehicle ID or the vehicle was not rented!");
    }

    // Send email
    private void sendEmail(String to, String subject, String content) {
        // QQ mail configuration
        String from = "xxx@qq.com"; // Enter your own QQ mail address
        String password = "xxxxxxx"; // Enter your own application-specific password

        Properties properties = new Properties();
        properties.put("mail.smtp.host", "smtp.qq.com");
        properties.put("mail.smtp.port", "587");
        properties.put("mail.smtp.auth", "true");
        properties.put("mail.smtp.starttls.enable", "true");

        // Create a session
        Session session = Session.getInstance(properties, new Authenticator() {
            @Override
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(from, password);
            }
        });

        try {
            MimeMessage message = new MimeMessage(session);
            message.setFrom(new InternetAddress(from));
            message.addRecipient(Message.RecipientType.TO, new InternetAddress(to));
            message.setSubject(subject);
            message.setText(content);

            Transport.send(message);
            System.out.println("Email sent successfully to " + to);
        } catch (MessagingException e) {
            e.printStackTrace();
            System.out.println("Failed to send email to " + to);
        }
    }

    public void log(String message) {
        String logMessage = new Date() + ": " + message;
        logs.add(logMessage);

        try (BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\Users\\Ethan\\Desktop\\Log.txt", true))) {
            writer.write(logMessage);
            writer.newLine();
        } catch (IOException e) {
            System.out.println("Error writing to log file: " + e.getMessage());
        }
    }

    public void viewLogs() {
        String logFilePath = "C:\\Users\\Ethan\\Desktop\\Log.txt";

        try (BufferedReader reader = new BufferedReader(new FileReader(logFilePath))) {
            String line;
            System.out.println("---- Rental Logs ----");
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            System.out.println("----------------------");
        } catch (FileNotFoundException e) {
            System.out.println("Log file not found.");
        } catch (IOException e) {
            System.out.println("Error reading log file: " + e.getMessage());
        }
    }
}
