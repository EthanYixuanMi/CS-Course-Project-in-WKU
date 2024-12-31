package Project;

public class User {
    private String email;
    private String password;
    private boolean isAdmin;
    private int numOfRentCars;

    // Constructor
    public User(String email, String password, boolean isAdmin, int numOfRentCars) {
        this.email = email;
        this.password = password;
        this.isAdmin = isAdmin;
        this.numOfRentCars = numOfRentCars;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public boolean isAdmin() {
        return isAdmin;
    }

    public void setAdmin(boolean isAdmin) {
        this.isAdmin = isAdmin;
    }

    public int getNumOfRentCars() {
        return numOfRentCars;
    }

    public void setNumOfRentCars(int numOfRentCars) {
        this.numOfRentCars = numOfRentCars;
    }

    @Override
    public String toString() {
        return "User{" +
                "email='" + email + '\'' +
                ", isAdmin=" + isAdmin +
                '}';
    }
}
