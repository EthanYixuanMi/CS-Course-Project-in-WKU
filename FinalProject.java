package Project;

import java.util.*;

public class FinalProject {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        int optionNumber;
        // Use do-while loop to create a menu for the user to choose from
        do {
            // Prompt the user to choose an option
            System.out.print("""
                    Main Menu
                    1. Addition Quiz
                    2. Lottery
                    3. Calculate Income Tax
                    4. Display COVID Official Statistics
                    5. MonteCarlo Simulation
                    6. Print Calendar
                    7. Print 50 prime numbers
                    8. Exit
                    Enter your option:\s""");

            optionNumber = input.nextInt();

            // If the input number is invalid, then prompt the user to enter again!
            while (optionNumber > 8 || optionNumber < 1) {
                System.out.println("Invalid input\n\n");
                System.out.print("""
                        Main Menu
                        1. Addition Quiz
                        2. Lottery
                        3. Calculate Income Tax
                        4. Display COVID Official Statistics
                        5. MonteCarlo Simulation
                        6. Print Calendar
                        7. Print 50 prime numbers
                        8. Exit
                        Enter your option:\s""");
                optionNumber = input.nextInt();
            }

            // use switch statement to invoke the methods
            switch (optionNumber) {
                case 1:
                    additionQuiz();
                    break;
                case 2:
                    lottery();
                    break;
                case 3:
                    calculateIncomeTax();
                    break;
                case 4:
                    displayCOVID();
                    break;
                case 5:
                    monteCarloSimulation();
                    break;
                case 6:
                    printCalendar();
                    break;
                case 7:
                    printPrimeNumbers();
                    break;
                case 8:
                    System.out.println("Exiting...");
                    break;
            }
        } while (optionNumber != 8); // Continue the loop until the user choose to exit
    }

    // Create the first question method
    public static void additionQuiz() {
        Scanner input = new Scanner(System.in);
        int a = (int) (Math.random() * 10);
        // Generate a random number between 0 and 9
        int b = (int) (Math.random() * 10);
        System.out.println("What is " + a + " + " + b + " ?");
        while (true) {
            int c = input.nextInt();
            // Check the answer
            if (a + b == c) {
                System.out.println("You got it correct");
                break;
            } else {
                System.out.println("Wrong answer. Try again.");
                System.out.println("What is " + a + " + " + b + " ?");
            }
        }
    }

    // Create the second question method
    public static void lottery() {
        // Generate a lottery number
        int lottery = (int) (Math.random() * 100);

        // Prompt the user to enter a guess
        Scanner input = new Scanner(System.in);
        System.out.print("Enter your lottery pick (two digits): ");
        int guess = input.nextInt();

        // Get digits from lottery
        int lotteryDigit1 = lottery / 10;
        int lotteryDigit2 = lottery % 10;

        // Get digits from guess
        int guessDigit1 = guess / 10;
        int guessDigit2 = guess % 10;

        System.out.println("The lottery number is " + lottery);

        // Check the guess
        if (guess == lottery)
            System.out.println("Exact match: you win $10000");
        // Check if the digits are matched
        else if (guessDigit2 == lotteryDigit1 && guessDigit1 == lotteryDigit2)
            System.out.println("Match all digits: you win $3000");
        else if (guessDigit1 == lotteryDigit1 || guessDigit1 == lotteryDigit2
                || guessDigit2 == lotteryDigit1 || guessDigit2 == lotteryDigit2)
            System.out.println("Match one digit: you win $1000");
        else
            System.out.println("Sorry, no match");
    }

    // Create the third question method
    public static void calculateIncomeTax() {
        Scanner input = new Scanner(System.in);

        // Prompt the user to enter filing status
        System.out.print("(0-single filer, 1-married jointly or " +
                "qualifying widow(er), 2-married separately, 3-head of household) " +
                "\nEnter the filing status: ");

        int status = input.nextInt();

        // Prompt the user to enter taxable income
        System.out.print("Enter the taxable income: ");
        double income = input.nextDouble();

        // Compute tax
        double tax = 0;
        // Compute tax for single filers
        if (status == 0) {
            if (income <= 8350)
                tax = income * 0.10;
            else if (income <= 33950)
                tax = 8350 * 0.10 + (income - 8350) * 0.15;
            else if (income <= 82250)
                tax = 8350 * 0.10 + (33950 - 8350) * 0.15
                        + (income - 33950) * 0.25;
            else if (income <= 171550)
                tax = 8350 * 0.10 + (33950 - 8350) * 0.15
                        + (82250 - 33950) * 0.25 + (income - 82250) * 0.28;
            else if (income <= 372950)
                tax = 8350 * 0.10 + (33950 - 8350) * 0.15 +
                        (82250 - 33950) * 0.25 + (171550 - 82250) * 0.28 +
                        (income - 171550) * 0.33;
            else
                tax = 8350 * 0.10 + (33950 - 8350) * 0.15 +
                        (82250 - 33950) * 0.25 + (171550 - 82250) * 0.28 +
                        (372950 - 171550) * 0.33 + (income - 372950) * 0.35;
        }
        // Compute tax for married file jointly or qualifying widow(er)
        else if (status == 1) {
            if (income <= 16700)
                tax = income * 0.10;
            else if (income <= 67900)
                tax = 16700 * 0.10 + (income - 16700) * 0.15;
            else if (income <= 137050)
                tax = 16700 * 0.10 + (67900 - 16700) * 0.15
                        + (income - 67900) * 0.25;
            else if (income <= 208850)
                tax = 16700 * 0.10 + (67900 - 16700) * 0.15
                        + (137050 - 67900) * 0.25 + (income - 137050) * 0.28;
            else if (income <= 372950)
                tax = 16700 * 0.10 + (67900 - 16700) * 0.15 +
                        (137050 - 67900) * 0.25 + (208850 - 137050) * 0.28 +
                        (income - 208850) * 0.33;
            else
                tax = 16700 * 0.10 + (67900 - 16700) * 0.15 +
                        (137050 - 67900) * 0.25 + (208850 - 137050) * 0.28 +
                        (372950 - 208850) * 0.33 + (income - 372950) * 0.35;
        }
        // Compute tax for married separately
        else if (status == 2) {
            if (income <= 8350)
                tax = income * 0.10;
            else if (income <= 33950)
                tax = 8350 * 0.10 + (income - 8350) * 0.15;
            else if (income <= 68525)
                tax = 8350 * 0.10 + (33950 - 8350) * 0.15
                        + (income - 33950) * 0.25;
            else if (income <= 104425)
                tax = 8350 * 0.10 + (33950 - 8350) * 0.15
                        + (68525 - 33950) * 0.25 + (income - 68525) * 0.28;
            else if (income <= 186475)
                tax = 8350 * 0.10 + (33950 - 8350) * 0.15 +
                        (68525 - 33950) * 0.25 + (104425 - 68525) * 0.28 +
                        (income - 104425) * 0.33;
            else
                tax = 8350 * 0.10 + (33950 - 8350) * 0.15 +
                        (68525 - 33950) * 0.25 + (104425 - 68525) * 0.28 +
                        (186475 - 104425) * 0.33 + (income - 186475) * 0.35;
        }
        // Compute tax for head of household
        else if (status == 3) {
            if (income <= 11950)
                tax = income * 0.10;
            else if (income <= 45500)
                tax = 11950 * 0.10 + (income - 11950) * 0.15;
            else if (income <= 117450)
                tax = 11950 * 0.10 + (45500 - 11950) * 0.15
                        + (income - 45500) * 0.25;
            else if (income <= 190200)
                tax = 11950 * 0.10 + (45500 - 11950) * 0.15
                        + (117450 - 45500) * 0.25 + (income - 117450) * 0.28;
            else if (income <= 372950)
                tax = 11950 * 0.10 + (45500 - 11950) * 0.15 +
                        (117450 - 45500) * 0.25 + (190200 - 117450) * 0.28 +
                        (income - 190200) * 0.33;
            else
                tax = 11950 * 0.10 + (45500 - 11950) * 0.15 +
                        (117450 - 45500) * 0.25 + (190200 - 117450) * 0.28 +
                        (372950 - 190200) * 0.33 + (income - 372950) * 0.35;
        } else {
            System.out.println("Error: invalid status");
            System.exit(1);
        }
        // Display the result
        System.out.println("Tax is " + (int) (tax * 100) / 100.0);
    }

    // Create the fourth question method
    public static void displayCOVID() {
        Scanner input = new Scanner(System.in);

        System.out.print("Enter initial COVID infected population: ");
        int initialInfected = input.nextInt();

        System.out.print("Enter COVID infection rate (as a decimal): ");
        double infectionRate = input.nextDouble();

        System.out.print("Enter COVID simulation duration (in days): ");
        int days = input.nextInt();

        simulateInfection(initialInfected, infectionRate, days);
    }

    public static void simulateInfection(int initialInfected, double infectionRate, int days) {
        System.out.printf("%-10s\n", "Day Infected Population");

        int currentInfected = initialInfected;

        for (int day = 1; day <= days; day++) {
            System.out.printf("%-4d%-3d\n", day, currentInfected);
            currentInfected = (int) (currentInfected * (1 + infectionRate));
        }
    }

    // Create the fifth question method
    public static void monteCarloSimulation() {
        int numberOfSimulations = 1000000;
        int numberOfDice = 2;
        int[] count = new int[13];

        // Run simulations
        for (int i = 0; i < numberOfSimulations; i++) {
            // we have two dices so roll two times
            int sum = rollDice(numberOfDice);
            // the index of sum in the array will be self-increment
            count[sum]++;
        }
        // Print results
        System.out.println("Simulation Results:");
        for (int i = 2; i <= 12; i++) {
            double probability = (double) count[i] / numberOfSimulations;
            System.out.println("Sum " + i + ": Probability = " + probability);
        }
    }

    public static int rollDice(int n) {
        Random random = new Random();
        int sum = 0;
        for (int i = 0; i < n; i++) {
            // Generate random number between 1 and 6
            sum += random.nextInt(6) + 1;
        }
        // return the sum of two dices
        return sum;
    }

    // Create the sixth question method
    public static void printCalendar() {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter full year: ");
        int year = input.nextInt();
        System.out.print("Enter month as a number between 1 and 12: ");
        int month = input.nextInt();
        printMonth(year, month);
    }

    public static void printMonth(int year, int month) {
        printMonthTitle(year, month);
        printMonthBody(year, month);
    }

    public static void printMonthTitle(int year, int month) {
        System.out.println(" " + getMonthName(month) + " " + year);
        System.out.println("-----------------------------");
        System.out.println(" Sun Mon Tue Wed Thu Fri Sat");
    }

    public static String getMonthName(int month) {
        String monthName = "";
        switch (month) {
            case 1:
                monthName = "January";
                break;
            case 2:
                monthName = "February";
                break;
            case 3:
                monthName = "March";
                break;
            case 4:
                monthName = "April";
                break;
            case 5:
                monthName = "May";
                break;
            case 6:
                monthName = "June";
                break;
            case 7:
                monthName = "July";
                break;
            case 8:
                monthName = "August";
                break;
            case 9:
                monthName = "September";
                break;
            case 10:
                monthName = "October";
                break;
            case 11:
                monthName = "November";
                break;
            case 12:
                monthName = "December";
                break;
        }
        return monthName;
    }

    public static void printMonthBody(int year, int month) {
        int startDay = getStartDay(year, month);
        int numberOfDaysInMonth = getNumberOfDaysInMonth(year, month);
        int i = 0;
        for (i = 0; i < startDay; i++) {
            System.out.print("    ");
        }
        for (i = 1; i <= numberOfDaysInMonth; i++) {
            System.out.printf("%4d", i);
            if ((i + startDay) % 7 == 0) {
                System.out.println();
            }
        }
        System.out.println();
    }

    public static int getStartDay(int year, int month) {
        int day = 1, h, q, m, j, k, statement;

        q = day;
        if (month == 1 || month == 2) {
            month += 12;
            year -= 1;
        }
        m = month;
        j = year / 100;
        k = year % 100;

        // use the Zeller's congruence
        h = (q + (26 * (m + 1) / 10) + k + k / 4 + j / 4 + 5 * j) % 7;

        switch (h) {
            case 0:
                statement = 6;
                break;
            case 1:
                statement = 0;
                break;
            case 2:
                statement = 1;
                break;
            case 3:
                statement = 2;
                break;
            case 4:
                statement = 3;
                break;
            case 5:
                statement = 4;
                break;
            case 6:
                statement = 5;
                break;
            default:
                statement = -1;
        }
        return statement;

    }

    public static int getNumberOfDaysInMonth(int year, int month) {
        if (month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10 || month == 12) {
            return 31;
        }

        if (month == 4 || month == 6 || month == 9 || month == 11) {
            return 30;
        }

        if (month == 2) {
            return isLeapYear(year) ? 29 : 28;
        }
        return 0;
    }

    public static boolean isLeapYear(int year) {
        return year % 400 == 0 || (year % 4 == 0 && year % 100 != 0);
    }

    // Create the seventh question method
    public static void printPrimeNumbers() {
        final int NUMBER_OF_PRIMES = 50;
        final int NUMBER_OF_PRIMES_PER_LINE = 10;
        int count = 0;
        int number = 2;
        System.out.println("The first 50 prime numbers are \n");
        while (count < NUMBER_OF_PRIMES) {
            boolean isPrime = true;
            for (int divisor = 2; divisor <= number / 2; divisor++) {
                if (number % divisor == 0) {
                    isPrime = false;
                    break;
                }
            }
            if (isPrime) {
                count++;
                if (count % NUMBER_OF_PRIMES_PER_LINE == 0) {
                    System.out.println(number);
                } else
                    System.out.print(number + " ");
            }
            number++;
        }
    }
}