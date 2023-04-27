
ref: C语言中文网: <http://c.biancheng.net/cplus/>

STL: [[cpp-STL-note.md]]

## 从C语言到C++

### 类和对象简介

- **类**（Class）和 **对象**（Object）
    - 也称对象是类的一个 实例（Instance）
    - 类的成员变量称为属性（Property），将类的成员函数称为方法（Method）

### 编译和运行

!!! note
    源代码 - 编译器 - 目标代码 - 链接器(启动代码, 库代码) - 可执行文件

```sh
# gcc
gcc main.c module.c
# `gcc`命令在链接时默认使用C的库，只有添加了`-lstdc++`选项才会使用 C++ 的库。
gcc main.cpp module.cpp -lstdc++

# g++
g++ main.cpp module.cpp
g++ main.cpp -o demo    # 使用`-o`选项可以指定可执行文件的名称
```

### 命名空间 namespace

命名空间内部不仅可以声明或定义变量，对于其它能在命名空间以外声明或定义的名称，同样也都能在命名空间内部进行声明或定义，例如类、函数、`typedef`、`#define` 等都可以出现在命名空间中。

另参考 [C++头文件和std命名空间](http://c.biancheng.net/view/2193.html)

```cpp
namespace name{
    //variables, functions, classes
}
```

e.g.

```cpp
namespace Li{  //小李的变量定义
    FILE* fp = NULL;
}
namespace Han{  //小韩的变量定义
    FILE* fp = NULL;
}

// `::`是一个新符号，称为域解析操作符，在C++中用来指明要使用的命名空间。
Li::fp = fopen("one.txt", "r");  //使用小李定义的变量 fp
Han::fp = fopen("two.txt", "rb+");  //使用小韩定义的变量 fp

// 采用 using 关键字声明
using namespace Li; // 声明整个命名空间
using Li::fp;       // 针对命名空间中的一个变量
fp = fopen("one.txt", "r");  //使用小李定义的变量 fp
Han :: fp = fopen("two.txt", "rb+");  //使用小韩定义的变量 fp
```

### 输入输出（cin和cout）

cout 和 cin 都是 C++ 的内置对象，而不是关键字。C++ 库定义了大量的类（Class），程序员可以使用它们来创建对象，cout 和 cin 就分别是 ostream 和 istream 类的对象，只不过它们是由标准库的开发者提前创建好的，可以直接拿来使用。这种在 C++ 中提前创建好的对象称为内置对象。  
  
使用 cout 进行输出时需要紧跟`<<`运算符，使用 cin 进行输入时需要紧跟`>>`运算符，这两个运算符可以自行分析所处理的数据类型，因此无需像使用 scanf 和 printf 那样给出格式控制字符串。

### 布尔类型（bool）

C语言并没有彻底从语法上支持“真”和“假”，只是用 0 和非 0 来代表。这点在 C++ 中得到了改善，C++ 新增了 `bool` 类型（布尔类型），它一般占用 1 个字节长度。bool 类型只有两个取值，`true` 和 `false`：true 表示“真”，false 表示“假”。

### new和delete运算符简介

- 在C语言中，动态分配内存用 `malloc()` 函数，释放内存用 `free()` 函数。
- C++又新增了两个关键字，new 和 delete：new 用来动态分配内存，delete 用来释放内存。
    - 和 malloc() 一样，new 也是在堆区分配内存，必须手动释放，否则只能等到程序运行结束由操作系统回收。为了避免内存泄露，通常 new 和 delete、new[] 和 delete[] 操作符应该成对出现

```cpp
// malloc, free
int *p = (int*) malloc( sizeof(int) * 10 );  //分配10个int型的内存空间
free(p);  //释放内存

// new delete
int *p = new int;  //分配1个int型的内存空间
delete p;  //释放内存
// new, delete[]
int *p = new int[10];  //分配10个int型的内存空间
delete[] p;
```

### inline 内联函数

函数调用是有时间和空间开销的。程序在执行一个函数之前需要做一些准备工作，要将实参、局部变量、返回地址以及若干寄存器都压入栈中，然后才能执行函数体中的代码；函数体中的代码执行完毕后还要清理现场，将之前压入栈中的数据都出栈，才能接着执行函数调用位置以后的代码。

为了消除函数调用的时空开销，C++ 提供一种提高效率的方法，即在编译时将函数调用处用函数体替换，类似于C语言中的宏展开。这种在函数调用处直接嵌入函数体的函数称为 **内联函数**（Inline Function），又称内嵌函数或者内置函数。

e.g.

```cpp
//内联函数，交换两个数的值
inline void swap(int *a, int *b){
    int temp;
    temp = *a;
    *a = *b;
    *b = temp;
}
int main(){
    int m, n;
    cin>>m>>n;
    cout<<m<<", "<<n<<endl;
    swap(&m, &n);
    cout<<m<<", "<<n<<endl;
}
```

注意，**要在函数定义处添加 `inline` 关键字**，在函数声明处添加 inline 关键字虽然没有错，但这种做法是无效的，编译器会忽略函数声明处的 inline 关键字。

使用内联函数的 **缺点** 也是非常明显的，编译后的程序会存在多份相同的函数拷贝，如果被声明为内联函数的函数体非常大，那么编译后的程序体积也将会变得很大，所以再次强调，一般只将那些短小的、频繁调用的函数声明为内联函数。


### 函数的默认参数

- 在C++中，定义函数时可以给形参指定一个默认的值，这样调用函数时如果没有给这个形参赋值（没有对应的实参），那么就使用这个默认的值。也就是说，调用函数时可以省略有默认值的参数。如果用户指定了参数的值，那么就使用用户指定的值，否则使用参数的默认值。
- 指定了默认参数后，调用函数时就 **可以省略对应的实参** 了。
- C++规定，默认参数只能放在形参列表的最后
- 在以后设计类时你将发现，通过使用默认参数，可以减少要定义的 **析构函数、方法以及方法重载** 的数量。

### C++函数重载 Function Overloading

- **参数列表** 又叫 **参数签名**，包括参数的类型、参数的个数和参数的顺序，只要有一个不同就叫做参数列表不同。
- 注意，参数列表不同包括参数的 **个数不同、类型不同或顺序不同**，仅仅参数名称不同是不可以的。函数返回值也不能作为重载的依据。







## 类和对象

- 与结构体一样，类只是一种复杂数据类型的声明，不占用内存空间。而对象是类这种数据类型的一个变量，或者说是通过类这种数据类型创建出来的一份实实在在的数据，所以占用内存空间。
- 创建对象以后，可以使用点号 `.` 来访问成员变量和成员函数，这和通过结构体变量来访问它的成员类似

```cpp
class Student{
public:
    //成员变量
    char *name;
    int age;
    float score;
    //成员函数
    void say(){
        cout<<name<<"的年龄是"<<age<<"，成绩是"<<score<<endl;
    }
};

// 创建单个对象
class Student stu;      //正确
Student LiLei;          //同样正确
// 创建对象数组
Student allStu[100];

stu.name = "小明";
stu.say();

```

### 对象指针

通过对象名字访问成员使用点号`.`，通过对象指针访问成员使用箭头`->`，这和结构体非常类似。

```cpp
// 上面代码中创建的对象 stu 在栈上分配内存，需要使用`&`获取它的地址
Student stu;
Student *pStu = &stu;
// 在堆上创建对象: new, delete
Student *pStu = new Student;
delete pStu;        //删除对象

// 有了对象指针后，可以通过箭头`->`来访问对象的成员变量和成员函数
pStu -> score = 92.5f;
pStu -> say();
```


在栈上创建出来的对象都有一个名字，比如 stu，使用指针指向它不是必须的。但是通过 `new` 创建出来的对象就不一样了，它在堆上分配内存，没有名字，只能得到一个指向它的指针，所以必须使用一个指针变量来接收这个指针，否则以后再也无法找到这个对象了，更没有办法使用它。也就是说，**使用 `new` 在堆上创建出来的对象是匿名的，没法直接使用，必须要用一个指针指向它，再借助指针来访问它的成员变量或成员函数**。

栈内存是程序自动管理的，不能使用 delete 删除在栈上创建的对象；堆内存由程序员管理，对象使用完毕后可以通过 delete 删除。在实际开发中，new 和 delete 往往成对出现，以保证及时删除不再使用的对象，防止无用内存堆积。

### 成员函数 (inline)

```cpp
class Student{
public:
    char *name;
    int age;
    float score;
    // 函数声明
    void say();  //内联函数声明，可以增加 inline 关键字，但编译器会忽略
};
//函数定义
inline void Student::say(){
    cout<<name<<"的年龄是"<<age<<"，成绩是"<<score<<endl;
}
```

当成员函数定义在类外时，就必须在函数名前面加上类名予以限定。`::` 被称为 **域解析符**（也称作用域运算符或作用域限定符），用来连接类名和函数名，指明当前函数属于哪个类。

成员函数必须先在类体中作原型声明，然后在类外定义，也就是说类体的位置应在函数定义之前。


### 类成员的访问权限

C++通过 `public、protected、private` 三个关键字来控制成员变量和成员函数的访问权限，它们分别表示公有的、受保护的、私有的，被称为成员访问限定符。所谓访问权限，就是你能不能使用该类中的成员。


### 构造函数

- 在栈上创建对象时，实参位于对象名后面，例如`Student stu("小明", 15, 92.5f)`；在堆上创建对象时，实参位于类名后面，例如`new Student("李华", 16, 96)`。
- 构造函数的调用是强制性的，**一旦在类中定义了构造函数，那么创建对象时就一定要调用，不调用是错误的**。如果有多个重载的构造函数，那么创建对象时提供的实参必须和其中的一个构造函数匹配；反过来说，创建对象时只有一个构造函数会被调用。
- 一个类必须有构造函数，要么用户自己定义，要么编译器自动生成。一旦用户自己定义了构造函数，不管有几个，也不管形参如何，编译器都不再自动生成。
- **调用没有参数的构造函数也可以省略括号**。对于示例的代码，在栈上创建对象可以写作`Student stu()`或`Student stu`，在堆上创建对象可以写作`Student *pstu = new Student()`或`Student *pstu = new Student`，它们都会调用构造函数 Student()。

```cpp
class Student{
private:
    char *m_name;
    int m_age;
    float m_score;
public:
    // 构造函数的重载
    Student();
    Student(char *name, int age, float score);
    void setname(char *name);
    void setage(int age);
    void setscore(float score);
    void show();
};
Student::Student(){
    m_name = NULL;
    m_age = 0;
    m_score = 0.0;
}
Student::Student(char *name, int age, float score){
    m_name = name;
    m_age = age;
    m_score = score;
}
void Student::setname(char *name){
    m_name = name;
}
void Student::setage(int age){
    m_age = age;
}
void Student::setscore(float score){
    m_score = score;
}
void Student::show(){
    if(m_name == NULL || m_age <= 0){
        cout<<"成员变量还未初始化"<<endl;
    }else{
        cout<<m_name<<"的年龄是"<<m_age<<"，成绩是"<<m_score<<endl;
    }
}

    //调用构造函数 Student(char *, int, float)
    Student stu("小明", 15, 92.5f);
    stu.show();
    //调用构造函数 Student()
    Student *pstu = new Student();
    pstu -> show();
    pstu -> setname("李华");
    pstu -> setage(16);
    pstu -> setscore(96);
    pstu -> show();
```

#### 构造函数初始化列表

构造函数的一项重要功能是对成员变量进行初始化，为了达到这个目的，可以在构造函数的函数体中对成员变量一一赋值，还可以采用初始化列表。

```cpp
// m_name(name) 采用初始化列表的形式进行初始化
Student::Student(char *name, int age, float score): m_name(name), m_age(age) {
    m_score = score;
}
```

- 构造函数初始化列表还有一个很重要的作用，那就是 **初始化 const 成员变量**。初始化 const 成员变量的唯一方法就是使用初始化列表。


```cpp
// VLA 类，用于模拟变长数组
class VLA{
private:
    const int m_len;
    int *m_arr;
public:
    VLA(int len);
};
//必须使用初始化列表来初始化 m_len
VLA::VLA(int len): m_len(len){
    // m_len = len; // ERROR
    m_arr = new int[len];
}
```

#### (构造) 函数默认值

- 注意加了默认值之后, 多个构造函数 (重构) 可能发生冲突!

```cpp
class complex
{
public:

    // 构造函数, 给定了默认值的情况下, 支持不同的参数传递方式
    complex(double r = 0, double i = 0) : re(r), im(i){};
    // 再写下面的构造函数和默认值形式的冲突了!
    // complex(): re(5), im(5){};

    void show()
    {
        cout << re << " + " << im << "i" << endl;
    }

    // const member function 常数成员函数
    // 在函数 () 后面加 const, 说明不会概念成员变量
    // 作用: `const complex c(2,1)` 来创建一个常量复数, 再调用 `c.real()` 会报错 reference to overloaded function could not be resolved;!!
    double real () const { return re; }
    double imag () const { return im; }
    // 函数重载: 设置值
    void real (double r) { re = r; }

private:
    double re, im;
};

int main(int argc, char const *argv[])
{
    complex c1(1, 2), c2(2), c3;
    c1.show();
    c2.show();
    c3.show();
}
```

### 析构函数 Destructor

析构函数（Destructor）也是一种特殊的成员函数，没有返回值，不需要程序员显式调用（程序员也没法显式调用），而是在销毁对象时自动执行。构造函数的名字和类名相同，而析构函数的名字是在类名前面加一个`~`符号。


#### 析构函数的执行时机

析构函数在对象被销毁时调用，而对象的销毁时机与它所在的内存区域有关。

- 在所有函数之外创建的对象是全局对象，它和全局变量类似，位于内存分区中的全局数据区，程序在结束执行时会调用这些对象的析构函数。
- 在函数内部创建的对象是局部对象，它和局部变量类似，位于栈区，函数执行结束时会调用这些对象的析构函数。
- new 创建的对象位于堆区，通过 delete 删除时才会调用析构函数；如果没有 delete，析构函数就不会被执行。


#### e.g. VLA 类来模拟变长数组

定义了一个 VLA 类来模拟变长数组，它使用一个构造函数为数组分配内存，这些内存在数组被销毁后不会自动释放，所以非常有必要再添加一个析构函数，专门用来释放已经分配的内存

```cpp
class VLA{
public:
    // C++ 中的 new 和 delete 分别用来分配和释放内存，它们与C语言中 malloc()、free() 最大的一个不同之处在于：
    // 用 new 分配内存时会调用构造函数，用 delete 释放内存时会调用析构函数。
    VLA(int len);   //构造函数
    ~VLA();         //析构函数
public:
    void input();   //从控制台输入数组元素
    void show();    //显示数组元素

private:
    // at() 函数只在类的内部使用，所以将它声明为 private 属性
    int *at(int i);  //获取第i个元素的指针
private:
    // m_len 变量不允许修改，所以用 const 进行了限制，这样就只能使用初始化列表来进行赋值
    const int m_len;  //数组长度
    int *m_arr;     //数组指针
    int *m_p;       //指向数组第i个元素的指针
};
VLA::VLA(int len): m_len(len){  //使用初始化列表来给 m_len 赋值
    if(len > 0){ m_arr = new int[len];  /*分配内存*/ }
    else{ m_arr = NULL; }
}
VLA::~VLA(){
    delete[] m_arr;  //释放内存
}
void VLA::input(){
    for(int i=0; m_p=at(i); i++){ cin>>*at(i); }
}
void VLA::show(){
    for(int i=0; m_p=at(i); i++){
        if(i == m_len - 1){ cout<<*at(i)<<endl; }
        else{ cout<<*at(i)<<", "; }
    }
}
int * VLA::at(int i){
    if(!m_arr || i<0 || i>=m_len){ return NULL; }
    else{ return m_arr + i; }
}

int main(){
    //创建一个有n个元素的数组（对象）
    int n;
    cout<<"Input array length: ";
    cin>>n;
    VLA *parr = new VLA(n);
    //输入数组元素
    cout<<"Input "<<n<<" numbers: ";
    parr -> input();
    //输出数组元素
    cout<<"Elements: ";
    parr -> show();
    //删除数组（对象）
    delete parr;
    return 0;
}
```

### this指针

this 是 C++ 中的一个关键字，也是一个 **const 指针**，它指向当前对象，通过它可以访问当前对象的所有成员。

this 实际上是成员函数的一个形参，在调用成员函数时将对象的地址作为实参传递给 this。**不过 this 这个形参是隐式的，它并不出现在代码中，而是在编译阶段由编译器默默地将它添加到参数列表中**。


### C++ static 静态成员变量

- 在C++中，我们可以使用静态成员变量来实现多个对象共享数据的目标。静态成员变量是一种特殊的成员变量，它被关键字 `static` 修饰
- static 成员变量属于类，不属于某个具体的对象，即使创建多个对象，也只为 m_total 分配一份内存，所有对象使用的都是这份内存中的数据。当某个对象修改了 m_total，也会影响到其他对象。
- static 成员变量必须在类声明的外部初始化 `type class::name = value;`
    - 初始化时可以赋初值，也可以不赋值。如果不赋值，那么会被默认初始化为 0。**全局数据区** 的变量都有默认的初始值 0，而 动态数据区（堆区、栈区）变量的默认值是不确定的，一般认为是垃圾值。
- 注意：static 成员变量的内存既不是在声明类时分配，也不是在创建对象时分配，而是在（类外）初始化时分配。反过来说，没有在类外初始化的 static 成员变量不能使用。
    - static 成员变量和普通的 static 变量类似，都在内存分区中的全局数据区分配内存

```cpp
class Student{
public:
    Student(char *name, int age, float score);
    void show();
public:
    static int m_total;  //静态成员变量
private:
    char *m_name;
    int m_age;
    float m_score;
};
// 创建对象的时候更新全局计数器
Student::Student(char *name, int age, float score): m_name(name), m_age(age), m_score(score){
    m_total++;  //操作静态成员变量
}

// 初始化
int Student::m_total = 0;

// 操纵共享的成员变量
//通过类类访问 static 成员变量
Student::m_total = 10;
//通过对象来访问 static 成员变量
Student stu("小明", 15, 92.5f);
stu.m_total = 20;
//通过对象指针来访问 static 成员变量
Student *pstu = new Student("李华", 16, 96);
pstu -> m_total = 20;

// 匿名对象
// 之所以使用匿名对象，是因为每次创建对象后只会使用它的 show() 函数，不再进行其他操作。不过使用匿名对象无法回收内存，会导致内存泄露，在中大型程序中不建议使用。
(new Student("小明", 15, 90)) -> show();
```

### C++ static 静态成员函数

在类中，static 除了可以声明静态成员变量，还可以声明静态成员函数。普通成员函数可以访问所有成员（包括成员变量和成员函数），静态成员函数只能访问静态成员。


静态成员函数与普通成员函数的根本 **区别** 在于：普通成员函数有 this 指针，可以访问类中的任意成员；而静态成员函数没有 this 指针，只能访问静态成员（包括静态成员变量和静态成员函数）。

和静态成员变量类似，静态成员函数在声明时要加 static，在定义时不能加 static。静态成员函数可以通过类来调用（一般都是这样做），也可以通过对象来调用


```cpp
class Student {
public:  //声明静态成员函数
    static int getTotal();
    static float getPoints();
private:
    static int m_total;  //总人数
    static float m_points;  //总成绩
}
// 初始化静态成员变量
int Student::m_total = 0;
float Student::m_points = 0.0;

//定义静态成员函数. 其只能访问静态成员变量
int Student::getTotal(){
    return m_total;
}
float Student::getPoints(){
    return m_points;
}
```

### C++ string 字符串

- <https://cplusplus.com/reference/string/string/>

```cpp
#include <string>

string s1;                      // 默认值是`""`，也即空字符串
string s2 = "c plus plus";      // 与C风格的字符串不同，string 的结尾没有结束标志`'\0'`
string s3 = s2;
string s4 (5, 's');             // 初始化为由 5 个`'s'`字符组成的字符串


// 由于 string 的末尾没有`'\0'`字符，所以 length() 返回的是字符串的真实长度，而不是长度 +1
int len = s.length();
```

#### 转换为C风格的字符串

虽然 C++ 提供了 string 类来替代C语言中的字符串，但是在实际编程中，有时候必须要使用C风格的字符串（例如打开文件时的路径），为此，string 类为我们提供了一个转换函数 `c_str()`，该函数能够将 string 字符串转换为C风格的字符串，并返回该字符串的 const 指针（`const char*`）

```cpp
string path = "D:\\demo.txt";
FILE *fp = fopen(path.c_str(), "rt");
```

#### 字符串的拼接

有了 string 类，我们可以使用`+`或`+=`运算符来直接拼接字符串，非常方便，再也不需要使用C语言中的 strcat()、strcpy()、malloc() 等函数来拼接字符串了，再也不用担心空间不够会溢出了。

用`+`来拼接字符串时，运算符的两边可以都是 string 字符串，也可以是一个 string 字符串和一个 **C风格的字符串**，还可以是一个 string 字符串和一 **个字符数组**，或者是一个 string 字符串和 **一个单独的字符**。

```cpp
    string s1 = "first ";
    string s2 = "second ";
    char *s3 = "third ";
    char s4[] = "fourth ";
    char ch = '@';
    
    string s5 = s1 + s2;
    // ... s1 可以和其他都相加
```

#### string 字符串的增删改查

```cpp
// 插入
string& insert (size_t pos, const string& str);
s1 = s2 = "1234567890";
s2.insert(5, "bbb");

// 删除
string& erase (size_t pos = 0, size_t len = npos);
// 如果不指明 len 的话，那么直接删除从 pos 到字符串结束处的所有字符（此时 len = str.length - pos）。
s2.erase(5);
s3.erase(5, 3);

// 子串
string substr (size_t pos = 0, size_t len = npos) const;
s2 = s1.substr(6, 6);

// 查找
size_t find (const string& str, size_t pos = 0) const;
size_t find (const char* s, size_t pos = 0) const;
// 第二个参数为开始查找的位置（下标）；如果不指明，则从第0个字符开始查找。
// 如果没有查找到子字符串，那么会返回一个无穷大值 4294967295。
string s1 = "first second third";
string s2 = "second";
int index = s1.find(s2,5);
// 不同的是 find() 函数从第二个参数开始往后查找，而 rfind() 函数则最多查找到第二个参数处，如果到了第二个参数所指定的下标还没有找到子字符串，则返回一个无穷大值4294967295。

// find_first_of() 函数用于查找子字符串和字符串共同具有的字符在字符串中首次出现的位置
// https://cplusplus.com/reference/string/string/find_first_of/ 将元音都替换为 *
std::string str ("Please, replace the vowels in this sentence by asterisks.");
std::size_t found = str.find_first_of("aeiou");
while (found!=std::string::npos)
{
str[found]='*';
found=str.find_first_of("aeiou",found+1);
}

std::cout << str << '\n';
```




### 总结

类的成员有成员变量和成员函数两种。

成员函数之间可以互相调用，成员函数内部可以访问成员变量。

私有成员只能在类的成员函数内部访问。默认情况下，class 类的成员是私有的，struct 类的成员是公有的。

可以用“对象名.成员名”、“引用名.成员名”、“对象指针->成员名”的方法访问对象的成员变量或调用成员函数。成员函数被调用时，可以用上述三种方法指定函数是作用在哪个对象上的。

对象所占用的存储空间的大小等于各成员变量所占用的存储空间的大小之和（如果不考虑成员变量对齐问题的话）。

定义类时，如果一个构造函数都不写，则编译器自动生成默认（无参）构造函数和复制构造函数。如果编写了构造函数，则编译器不自动生成默认构造函数。一个类不一定会有默认构造函数，但一定会有复制构造函数。

任何生成对象的语句都要说明对象是用哪个构造函数初始化的。即便定义对象数组，也要对数组中的每个元素如何初始化进行说明。如果不说明，则编译器认为对象是用默认构造函数或参数全部可以省略的构造函数初始化。在这种情况下，如果类没有默认构造函数或参数全部可以省略的构造函数，则编译出错。

对象在消亡时会调用析构函数。

每个对象有各自的一份普通成员变量，但是静态成员变量只有一份，被所有对象所共享。静态成员函数不具体作用于某个对象。即便对象不存在，也可以访问类的静态成员。静态成员函数内部不能访问非静态成员变量，也不能调用非静态成员函数。

常量对象上面不能执行非常量成员函数，只能执行常量成员函数。

包含成员对象的类叫封闭类。任何能够生成封闭类对象的语句，都要说明对象中包含的成员对象是如何初始化的。如果不说明，则编译器认为成员对象是用默认构造函数或参数全部可以省略的构造函数初始化。

在封闭类的构造函数的初始化列表中可以说明成员对象如何初始化。封闭类对象生成时，先执行成员对象的构造函数，再执行自身的构造函数；封闭类对象消亡时，先执行自身的析构函数，再执行成员对象的析构函数。

const 成员和引用成员必须在构造函数的初始化列表中初始化，此后值不可修改。

友元分为友元函数和友元类。友元关系不能传递。

成员函数中出现的 this 指针，就是指向成员函数所作用的对象的指针。因此，静态成员函数内部不能出现 this 指针。成员函数实际上的参数个数比表面上看到的多一个，多出来的参数就是 this 指针。


## C++ 引用 Reference

同指针一样，引用能够减少数据的拷贝，提高数据的传递效率。

### C++引用入门

- C/C++ 禁止在函数调用时直接传递数组的内容，而是 **强制传递数组指针**
- 而对于结构体和对象没有这种限制，调用函数时既可以传递指针，也可以直接传递内容
    - 但是在 C++ 中，我们有了一种比指针更加便捷的传递聚合类型数据的方式，那就是引用（Reference）。

引用（Reference）是 C++ 相对于C语言的又一个扩充。引用可以看做是数据的一个别名，通过这个别名和原来的名字都能够找到这份数据。

```cpp
// 引用的定义方式类似于指针，只是用`&`取代了`*`
type &name = data;
// 引用必须在定义的同时初始化，并且以后也要从一而终，不能再引用其它数据，这有点类似于常量（const 变量）。
```

e.g. 引用就是该变量, 共享同一个地址.

```cpp
    int a = 99;
    int &r = a;     // 变量 r 就是变量 a 的引用，它们用来指代同一份数据
    // 注意，引用在定义时需要添加`&`，在使用时不能添加`&`，使用时添加`&`表示取地址。
    cout << a << ", " << r << endl;
    cout << &a << ", " << &r << endl;
// 99, 99
// 0x28ff44, 0x28ff44
```

#### 常引用

为了防止被修改

```cpp
// 常引用,两种语法都可
const type &name = value;
type const &name = value;
```

### C++引用作为函数参数

比较下面通过指针和引用两重方式对于传入参数进行修改的函数

```cpp
void swap2(int *p1, int *p2);
void swap3(int &r1, int &r2);

//传递指针
void swap2(int *p1, int *p2) {
    int temp = *p1;
    *p1 = *p2;
    *p2 = temp;
}
//按引用传参
void swap3(int &r1, int &r2) {
    int temp = r1;
    r1 = r2;
    r2 = temp;
}
```

### C++引用作为函数返回值

```cpp
int &plus10(int &r) {
    r += 10;
    return r;
}

int num1 = 10;
int num2 = plus10(num1);
cout << num1 << " " << num2 << endl;
// 20 20
```

在将引用作为函数返回值时应该注意一个小问题，就是不能返回局部数据（例如局部变量、局部对象、局部数组等）的引用，因为当函数调用完成后局部数据就会被销毁，有可能在下次使用时数据就不存在了，C++ 编译器检测到该行为时也会给出警告。







## topics

### .h .cpp 文件

- [理解头文件(.h)和源文件(.cpp)](https://blog.csdn.net/John_xyz/article/details/82924597)

下面两种 include 方法分别: 1) 编译器会在系统文件目录下查找; 2) 编译器首先在用户目录下查找，然后在C++安装目录中查找，最后在系统文件中查找

```cpp
#include <>
#include ""
```

#### 头文件 (.h)

- 写类的声明（包括类里面的成员和方法的声明）、函数原型、#define 常数等，但一般来说不写出类的具体实现。
- 在写头文件时需要注意，开头和结尾必须按照如下样式加上预编译语句

```cpp
#ifndef CIRCLE_H
#define CIRCLE_H
// your code
#endif
```

### struct, class

[C和C++中struct](https://github.com/Light-City/CPlusPlusThings/tree/master/basic_content/struct)

struct 作为数据结构的实现体，它默认的数据访问控制是 public 的，而 class 作为对象的实现体，它默认的成员变量访问控制是 private 的。

#### struct

在cpp中, struct

- 能将函数放在结构体声明
- public、protected、private 在C++中可以使用。
- 使用结构体, 可以不加struct (而在C中一定要)
- 可以继承 (C中没有这一概念)
- 若结构体的名字与函数名相同，使用结构体，只能使用带struct定义 (而在C中可以直接调用)

```cpp
#include<iostream>
#include<stdio.h>
struct Base {         
    int v1;
//    private:   //error!
        int v3;
    public:   //显示声明public
        int v2;
    virtual void print(){       
        printf("%s\n","Base");
    };    
};
struct Derived:Base {         

    public:
        int v2;
    void print(){       
        printf("%s\n","Derived");
    };    
};
int main() {
    Base *b=new Derived();
    b->print();
    return 0;
}
```

### extern "C"

C++ 调用 C 函数

```cpp
//xx.h
extern int add(...)

//xx.c
int add(){
    
}

//xx.cpp
extern "C" {
    #include "xx.h"
}
```

C 调用 C++ 函数

```c
//xx.h
extern "C"{
    int add();
}
//xx.cpp
int add(){
    
}
// 或者直接写成下面的形式
extern "C" string f(){}

//xx.c
extern int add();
```

### freopen 重定向 标准输入输出

```cpp
// <stdio.h>
FILE *freopen( const char *path, const char *mode, FILE *stream ); 
// 实现重定向，把预定义的标准流文件定向到由path指定的文件中。标准流文件具体是指stdin、stdout和stderr。其
```

e.g.

```cpp
#include <stdio.h>
#include <iostream>
int main()
{ 
    int a,b; 
    freopen("D:\\in.txt","r",stdin);    //输入重定向，输入数据将从D盘根目录下的in.txt文件中读取 
    freopen("D:\\out.txt","w",stdout); //输出重定向，输出数据将保存在D盘根目录下的out.txt文件中 
    while(cin>>a>>b) 
    cout<<a+b<<endl;    // 注意使用endl 
    // C 语法
    // while(scanf("%d %d",&a,&b)!=EOF) 
    // printf("%d\n",a+b);
    fclose(stdin);      //关闭重定向输入
    fclose(stdout);     //关闭重定向输出 
    return 0; 
}
```

### C++11右值引用

see [here](http://c.biancheng.net/view/439.html)

```cpp
class A{};
A & rl = A();  //错误，无名临时变量 A() 是右值，因此不能初始化左值引用 r1
A && r2 = A();  //正确，因 r2 是右值引用
```
