
## Java 快速入门

### 流程控制

输入输出

- Java提供的输出包括：System.out.println() / print() / printf()，其中printf()可以格式化输出；
  - `System.out.printf("%.2f\n", d);` // 显示两位小数3.14
  - 十六进制 `System.out.printf("n=%d, hex=%08x", n, n);` // 注意，两个%占位符必须传入两个数
- Java提供 `Scanner` 对象来方便输入，读取对应的类型可以使用：scanner.nextLine() / nextInt() / nextDouble() / ...
  - `Scanner scanner = new Scanner(System.in);` // 创建Scanner对象
  - System.out.print("Input your age: "); // 打印提示
  - `int age = scanner.nextInt();` // 读取一行输入并获取整数

if

- if ... else可以做条件判断，else是可选的；
- 不推荐省略花括号{}；
- 要注意浮点数判断相等不能直接用==运算符；
- 引用类型 (例如 String) 判断内容相等要使用 `equals()`，注意避免 `NullPointerException` (为了防止 s1=null 可以 `(s1 != null && s1.equals("hello"))`)。

switch

- switch语句可以做多重选择，然后执行匹配的case语句后续代码；
- switch的计算结果必须是整型、字符串或枚举类型；
- 从Java 14开始，switch语句正式升级为表达式，不再需要break，并且允许使用yield返回值。

```java
int opt;
switch (fruit) {
    case "apple":
        opt = 1;
        break;
    case "pear":
    case "mango":
        opt = 2;
        break;
    default:
        opt = 0;
        break;
}
// 新语法
String fruit = "orange";
int opt = switch (fruit) {
    case "apple" -> 1;
    case "pear", "mango" -> 2;
    default -> {
        int code = fruit.hashCode();
        yield code; // switch语句返回值
    }
};
```

while, do...while, for

- while循环先判断循环条件是否满足，再执行循环语句；
- while循环可能一次都不执行；
- break语句通常配合if，在满足条件时提前结束整个循环；
- continue语句通常配合if，在满足条件时提前结束本次循环。

### 数组操作

遍历数组

- 遍历数组可以使用for循环，for循环可以访问数组索引，for each循环直接迭代每个数组元素，但无法获取索引 (语法 `for (int n : ns) {}`)；
- 使用 `Arrays.toString()` 可以快速获取数组内容 (直接 print 数组引用得到的是地址)。

数组排序

- 可以直接使用Java标准库提供的Arrays.sort()进行排序；

多维数组

- 二维数组就是数组的数组，三维数组就是二维数组的数组；
- 多维数组的每个数组元素长度都不要求相同；
- 打印多维数组可以使用Arrays.deepToString()；

```java
int[][] ns = {
    { 1, 2, 3, 4 },
    { 5, 6 },
    { 7, 8, 9 }
};

for (int[] arr : ns) {
    for (int n : arr) {
        System.out.print(n);
        System.out.print(', ');
    }
    System.out.println();
}
```

命令行参数

- 命令行参数类型是String[]数组；
- 命令行参数由JVM接收用户输入并传给main方法；

## 面向对象编程

### 基础

- class定义的field，在每个instance都会拥有各自的field，且互不干扰；
- 通过new操作符创建新的instance，然后用变量指向它，即可通过变量来引用这个instance；
- 指向instance的变量都是引用变量。

方法

- 方法可以让外部代码安全地访问实例字段；
- 可变参数用类型...定义，可变参数相当于数组类型

```java
// 可变参数
class Group {
    private String[] names;

    public void setNames(String... names) {
        this.names = names;
    }
}
Group g = new Group();
g.setNames("Xiao Ming", "Xiao Hong", "Xiao Jun"); // 传入3个String
g.setNames("Xiao Ming", "Xiao Hong"); // 传入2个String
g.setNames("Xiao Ming"); // 传入1个String
g.setNames(); // 传入0个String. 注意, 此时如果写成数组类型的参数是不合法的
```

构造方法

- 没有在构造方法中初始化字段时，引用类型的字段默认是null，数值类型的字段用默认值，int类型默认值是0，布尔类型默认值是false
- 可以定义多个构造方法，编译器根据参数自动判断；
- 可以在一个构造方法内部调用另一个构造方法，便于代码复用。

```java
    public static void main(String[] args) {
        Person p1 = new Person("Xiao Ming", 15); // 既可以调用带参数的构造方法
        Person p2 = new Person(); // 也可以调用无参数构造方法
    }

// 构造方法
class Person {
    private String name;
    private int age;

    // 事实上如果不写, 编译器会自动生成类似这样的空方法; 但下面自定义了构造方法, 想要无参调用就要自己写出来
    public Person() {
    }
    // 注意没有返回参数类型
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}
```

方法重载

- 重载方法应该完成类似的功能，参考String的indexOf()；
- 重载方法返回值类型应该相同。

```java
// String.indexOf 方法重载
        String s = "Test string";
        int n1 = s.indexOf('t');
        int n2 = s.indexOf("st");
        int n3 = s.indexOf("st", 4);    // fromIndex
```
