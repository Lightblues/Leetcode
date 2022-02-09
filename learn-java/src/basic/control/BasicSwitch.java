package basic.control;

import java.util.Scanner;

public class BasicSwitch {
    public static void main(String []args){
        Scanner scanner = new Scanner(System.in);
        System.out.print("Please choice: (1. Rock, 2. Scissors, 3. Paper)");
        int choice = scanner.nextInt();
        scanner.close();
        int random = 1 + (int) (Math.random() * 3);
        System.out.printf("Player: %d; Computer: %d\n", choice, random);
        // switch 经典写法, 注意 break
        switch (choice){
            case 1:
                System.out.println(random==1 ? "Draw" : random==3 ? "Lose" : "Win");
                break;
            case 2:
                System.out.println(random==2 ? "Draw" : random==1 ? "Lose" : "Win");
                break;
            case 3:
                System.out.println(random==3 ? "Draw" : random==2 ? "Lose" : "Win");
                break;
            default:
                System.out.println("Default!!!");
        }
        // switch 简洁写法
        switch (choice) {
            case 1 -> System.out.println(random==1 ? "Draw" : random==3 ? "Lose" : "Win");
            case 2 -> System.out.println(random==2 ? "Draw" : random==1 ? "Lose" : "Win");
            case 3 -> System.out.println(random==3 ? "Draw" : random==2 ? "Lose" : "Win");
        }

    }
}
