
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
