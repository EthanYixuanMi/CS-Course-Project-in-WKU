package Project;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class Vehicle {
    private int id;
    private String brand;
    private String model;
    private String color;
    private int peopleCapacity;
    private double rentPrice;
    private double length;
    private double width;
    private String isAvailable;

    public Vehicle(int id, String brand, String model, String color, int peopleCapacity,
                   double rentPrice, double length, double width, String isAvailable) {
        this.id = id;
        this.brand = brand;
        this.model = model;
        this.color = color;
        this.peopleCapacity = peopleCapacity;
        this.rentPrice = rentPrice;
        this.length = length;
        this.width = width;
        this.isAvailable = isAvailable;
    }

    // Getters
    public int getId() {
        return id;
    }

    public String getBrand() {
        return brand;
    }

    public String getModel() {
        return model;
    }

    public String getColor() {
        return color;
    }

    public int getPeopleCapacity() {
        return peopleCapacity;
    }

    public double getRentPrice() {
        return rentPrice;
    }

    public double getLength() {
        return length;
    }

    public double getWidth() {
        return width;
    }

    public String getIsAvailable() {
        return isAvailable;
    }

    // Setters
    public void setAvailable(String isAvailable) {
        this.isAvailable = isAvailable;
        if (isAvailable.equals("false")) {
            try {
                FileWriter fileWriter = new FileWriter("C:\\Users\\Ethan\\Desktop\\Vehicles.txt", true);
                BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);
                bufferedWriter.write("\n" + id + ", " + brand + ", " + model + ", " + color + ", " + peopleCapacity
                        + ", " + rentPrice + ", " + length + ", " + width + ", " + isAvailable);
                bufferedWriter.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    public String toString() {
        return "ID: " + id + ", Brand: " + brand + ", Model: " + model +
                ", Color: " + color + ", Capacity: " + peopleCapacity +
                ", Rent Price: $" + rentPrice + "/day, Dimensions: " +
                length + "m x " + width + "m, Available: " + isAvailable;
    }
}

