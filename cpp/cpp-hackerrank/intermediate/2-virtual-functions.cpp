/* 

1] 类基础
在C++中，类是一种用户定义的数据类型，它允许你封装数据和功能在一个逻辑单元中。类提供了一种面向对象的编程方式，通过创建对象来使用类，并使用类的成员函数来访问和操作对象的数据。

下面是关于C++中类的一些常见特性和概念：

1.  成员变量（Member Variables）：
    *   类中的成员变量也被称为数据成员或属性。它们用于存储对象的状态和数据。
    *   成员变量可以具有不同的数据类型，如整数、浮点数、字符、指针、其他类对象等。
    *   成员变量可以是公有的（public）、私有的（private）或受保护的（protected），用于控制对数据的访问权限。
2.  成员函数（Member Functions）：
    *   成员函数也被称为方法或操作，用于操作和处理类的对象。
    *   成员函数可以访问和操作类的成员变量，也可以执行其他操作。
    *   成员函数可以是公有的、私有的或受保护的，用于控制对功能的访问权限。
3.  构造函数（Constructor）：
    *   构造函数是一种特殊的成员函数，用于在创建对象时进行初始化。
    *   构造函数的名称与类名相同，没有返回类型，并可以带有参数。
    *   构造函数在创建对象时自动调用，用于对对象的成员变量进行初始化。
4.  析构函数（Destructor）：
    *   析构函数是一种特殊的成员函数，用于在对象销毁时进行清理工作。
    *   析构函数的名称与类名相同，前面加上波浪号（~）作为前缀，没有返回类型，不带参数。
    *   析构函数在对象销毁时自动调用，用于释放对象所占用的资源。
5.  访问控制（Access Control）：
    *   类中的成员变量和成员函数可以使用访问修饰符来指定其访问级别。
    *   公有成员（public）可以在类的内部和外部访问。
    *   私有成员（private）只能在类的内部访问。
    *   受保护成员（protected）可以在类的内部和派生类中访问。
6.  封装（Encapsulation）：
    *   封装是指将数据和相关的操作封装在一个类中，隐藏实现细节，并提供公共接口来访问和操作数据。
    *   封装提供了数据的安全性和灵活性，可以通过成员函数来控制对数据的访问。
7.  继承（Inheritance）：
    *   继承是面向对象编程的一个重要概念，允许创建一个类从另一个类派生，继承父类的属性和行为。
    *   派生类可以继承父类的成员变量和成员函数，并可以添加自己的新成员变量和成员函数。
    *   继承提供了代码重用和层次化组织的能力。
8.  多态（Polymorphism）：
    *   多态是面向对象编程的另一个重要概念，允许不同的对象对相同的消息作出不同的响应。
    *   多态通过继承和虚函数实现，允许以父类的指针或引用来调用派生类的成员函数。


2] static

自动对于类成员进行计数. 需要用到静态成员变量（Static Member Variables）和静态成员函数（Static Member Functions）。
如下面的 `static int cur_id;` 变量, 但是主要要在类定义外面进行初始化 `int Professor::cur_id = 0;`。


3] 虚函数（Virtual Functions）
    virtual, override
    普通虚函数: 在基类中已经实现了, 可以在派生类中重新实现 (override)
    纯虚函数: 在基类中没有实现, 必须在派生类中实现. 通过 `virtual void getdata() = 0;` 的形式来声明纯虚函数。


Input:
4
1
Walter 56 99
2
Jesse 18 50 48 97 76 34 98
2
Pinkman 22 10 12 0 18 45 50
1
White 58 87

Output:
Walter 56 99 1
Jesse 18 403 1
Pinkman 22 135 2
White 58 87 2

 */


#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;

// code from here
class Person {
    protected:
        string name;
        int age;
    public:
        // 纯虚函数（Pure Virtual Functions）
        virtual void getdata() = 0;
        virtual void putdata() = 0;
};

class Professor : public Person {
    private:
        int publications;
        // 静态成员变量（Static Member Variables）
        static int cur_id;
        int id;
    public:
        // 构造函数（Constructor）
        Professor() {
            cur_id++;
            id = cur_id;
        }
        void getdata() {
            cin >> name >> age >> publications;
        }
        void putdata() {
            cout << name << " " << age << " " << publications << " " << id << endl;
        }
};
class Student : public Person {
    private:
        int marks[6];
        static int cur_id;
        int id;
    public:
        Student() {
            cur_id++;
            id = cur_id;
        }
        void getdata() {
            cin >> name >> age;
            for (int i = 0; i < 6; i++) {
                cin >> marks[i];
            }
        }
        void putdata() {
            int sum = 0;
            for (int i = 0; i < 6; i++) {
                sum += marks[i];
            }
            cout << name << " " << age << " " << sum << " " << id << endl;
        }
};
int Professor::cur_id = 0;
int Student::cur_id = 0;

int main(){

    int n, val;
    cin>>n; //The number of objects that is going to be created.
    Person *per[n];

    for(int i = 0;i < n;i++){

        cin>>val;
        if(val == 1){
            // If val is 1 current object is of type Professor
            per[i] = new Professor;

        }
        else per[i] = new Student; // Else the current object is of type Student

        per[i]->getdata(); // Get the data from the user.

    }

    for(int i=0;i<n;i++)
        per[i]->putdata(); // Print the required output for each object.

    return 0;

}
