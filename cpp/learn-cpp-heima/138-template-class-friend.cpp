#include<iostream>

using namespace std;

//2、全局函数配合友元  类外实现 - 先做函数模板声明，下方在做函数模板定义，在做友元
template<typename T1, typename T>class Person;
//如果声明了函数模板，可以将实现写到后面，否则需要将实现体写到类的前面让编译器提前看到
template <class T1, class T2> void printPerson2(Person<T1, T2> &p);

template<class T1, class T2>
class Person{
    public :
    Person(T1 name, T2 age){
        this->name = name;
        this->age = age;
    }

    //1、全局函数配合友元   类内实现
    friend void printPerson(Person<T1, T2> &p){
        cout << p.name << p.age << endl;
    }

    //全局函数配合友元  类外实现
    friend void printPerson2<>(Person<T1, T2> &p);      
    //注意到由于类模板的函数对象是调用时生成的，因此这里直接声明 friend void printPerson2(Person<T1, T2> &p); 
    //的话无法生成真正的函数对象；因此采用类模板的形式，但这个全局函数需要提前声明，因此需要将 printPerson() 的具体实现
    //放在最前面，或者相这里一样将定义写在下面而在开头声明（第 8 行）；而为了让编译器判断 Person 类型，需要在最前面加上 Person 的
    //声明（第 6 行。）

    private:
    T1 name;
    T2 age;
};

template <class T1, class T2>
void printPerson2(Person<T1, T2> &p){
    cout << "Implication out of class. "<<p.name << p.age<< endl;
}

int main () {
    Person<string, int> p("tom", 12);
    printPerson(p);
    printPerson2(p);
}