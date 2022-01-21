#include <iostream>
using namespace std;

class Person{
    public:
        Person(int a, int b){
            this->m_a = a;
            this->m_b = b;
        }
        Person () {};
        //成员函数实现 + 号运算符重载
        // Person operator+(Person &b){
        //     Person temp;
        //     temp.m_b = this->m_b + b.m_b;
        //     temp.m_a = this->m_a + b.m_a;
        //     return temp;
        // }
        
    public: 
        int m_a, m_b;
};
//全局函数实现 + 号运算符重载
Person operator+(Person *p1, Person &p2){
    Person temp;
    temp.m_a = (*p1).m_a + p2.m_a;
    temp.m_b = (*p1).m_b + p2.m_b;
    return temp;
}
//运算符重载 可以发生函数重载 
Person operator+(Person p1, Person &p2){
    Person temp;
    temp.m_a = p1.m_a + p2.m_a;
    temp.m_b = (p1).m_b + p2.m_b;
    return temp;
}

//全局函数实现左移重载
//ostream对象只能有一个
ostream & operator<< (ostream &out, Person &p){
    out << "a: " << p.m_a << "\tb: " << p.m_b << endl;
    return out;
}


int main() {
    Person p1(10, 10);
    Person p2(1, 2);

    Person *pp = new Person(10, 10);

    Person p3 = p1 + p2;
    cout << p3.m_a << p3.m_b << endl;
    p3 = pp + p2;
    cout << p3.m_a << p3.m_b << endl;

    cout << p3 << endl;
}

