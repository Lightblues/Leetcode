package oop.method;

public class Main {
    public static void main(String[] args) {
		Person ming = new Person();
		ming.setName("小明");
		System.out.println(ming.getName());

		ming.setAge(12);
		System.out.println(ming.getAge());
	}
}
