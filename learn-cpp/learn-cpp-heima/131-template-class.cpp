#include<iostream>

using namespace std;

//类模板中的模板参数列表 可以指定默认参数【函数模板中没有该语法】
template<class NameType, class AgeType=int>
class Person {
    public:
    Person(NameType name, AgeType age){
        this->name = name;
        this->age = age;
    }
    void showPerson(){
        cout << this->name << this->age << endl;
    }

    NameType name;
    AgeType age;
};

int main () {
    //必须使用显示指定类型的方式，使用类模板
    Person<string, int> p("li", 32);
    p.showPerson();

    //类模板中的模板参数列表 可以指定默认参数
    Person<string> p2("ruli", 32);
    p2.showPerson();
}