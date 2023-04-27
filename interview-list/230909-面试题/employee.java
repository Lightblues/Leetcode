/* Employee Profile
实现一个类
abstract Employee
    abstract void setSalary(int salary)
    abstract int getSalary()
    abstract void setGrade(String grade)
    abstract String getGrade()
    void label()
        # print "Employee's data:\n"
class Engineer extend Employee
    private int salary
    private String grade
    implement setter, getter 
class Manager extend Emphoyee
    private int salary
    private String grade
    implement setter, getter

注意下面的实现都设置了public, 需要写在独立的 Employee.java 这样的文件中. 这里只需要将public去掉就不会报错
 */

// Employee.java
public abstract class Employee {
    public abstract void setSalary(int salary);
    public abstract int getSalary();
    public abstract void setGrade(String grade);
    public abstract String getGrade();
    public void label() {
        System.out.println("Employee's data:");
    }
}

// Engineer.java
public class Engineer extends Employee {
    private int salary;
    private String grade;

    public void setSalary(int salary) {
        this.salary = salary;
    }

    public int getSalary() {
        return salary;
    }

    public void setGrade(String grade) {
        this.grade = grade;
    }

    public String getGrade() {
        return grade;
    }
}

// Manager.java
public class Manager extends Employee {
    private int salary;
    private String grade;

    public void setSalary(int salary) {
        this.salary = salary;
    }

    public int getSalary() {
        return salary;
    }

    public void setGrade(String grade) {
        this.grade = grade;
    }

    public String getGrade() {
        return grade;
    }
}