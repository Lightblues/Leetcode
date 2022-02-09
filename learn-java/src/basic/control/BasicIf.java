package basic.control;

import java.util.Scanner;

public class BasicIf {
    public static void main(String[] args) {
		Scanner scanner = new Scanner(System.in);
		System.out.print("Height (m): ");
		double height = scanner.nextDouble();
		System.out.print("Weight (kg): ");
		double weight = scanner.nextDouble();
        scanner.close();
		double bmi = 0;
		bmi = weight / (height * height);
        String result = "";
        if (bmi<18.5) {
            result = "Underweight";
        } else if (bmi <25) {
            result = "Normal";
        } else if ( bmi < 28 ){
            result = "Overweight";
        } else if ( bmi < 32 ){
            result = "Obese";
        } else {
            result = "Morbidly obese";
        }
        System.out.println("BMI: " + bmi + "\n" + result);
	}
}
