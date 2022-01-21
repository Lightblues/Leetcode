#include<iostream>

using namespace std;

class Person{
    public:
    Person(string n, int a){
        this->name = n;
        this->age = a;
    }
    string name;
    int age;
};

template<class T>
bool myCompare(T &a, T&b){
    return a==b?true:false;
}

template<> bool myCompare(Person &a, Person &b){
    return (a.age==b.age && a.name==b.name)?true:false;
}

int main () {
    // int a=10, b=20;
    // bool res = myCompare(a, b);
    Person a("tom", 32), b("tom", 32);
    bool res = myCompare(a, b);

    cout << res << endl;
}