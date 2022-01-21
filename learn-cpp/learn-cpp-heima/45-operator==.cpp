#include<iostream>
using namespace std;

class Person{
    public:
    Person(string name, int age){
        m_name = name;
        m_age = age;
    }
    bool operator==(Person &p){
        if (this->m_age==p.m_age && this->m_name==p.m_name){
            return true;
        } else {
            return false;
        }
    }


    int m_age;
    string m_name;
};

bool operator!= (Person &p1, Person &p2){
    if (p1.m_name==p2.m_name && p1.m_age==p2.m_age){
        return false;
    } else {
        return true;
    }
}

int main() {
    Person p1("Hi", 10), p2("HI", 10);
    cout << "p1==p2: " << (p1==p2) << endl;
    cout << "p1!=p2: " << (p1!=p2) << endl;

}