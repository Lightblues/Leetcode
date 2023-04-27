#include<iostream>
using namespace std;

class Person{
    public:
    Person(int age){
        m_age = new int(age);
    }
    Person & operator=(Person &p){
        if (m_age != NULL){
            delete m_age;
            m_age = NULL;
        }
        m_age = new int(*p.m_age);
        return *this;
    }

    ~Person() {
        if (m_age != NULL){
            delete m_age;
            m_age = NULL;
        }
    }

    int * m_age;
};

int main() {
    Person p1(18);
    Person p2(20);
    Person p3(30);
    p3 = p2 = p1;
    cout << "Person1: " << *p1.m_age << endl;
    cout << "Person2: " << *p2.m_age << endl;
    cout << "Person3: " << *p3.m_age << endl;
}