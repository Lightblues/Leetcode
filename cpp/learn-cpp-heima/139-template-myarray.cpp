#include<iostream>

using namespace std;

#include "139-myarray.hpp"
#include <string>

void printMyarray(MyArray<int> & arr){
    for (int i=0; i<arr.get_size(); i++){
        cout << arr[i] << "\t";
    }
    cout << endl;
}





class Person{
    public:
    Person() {};        // 还要提供一个空的实现
    Person(int age, string name){
        this->age = age;
        this->name = name;
    }

    int age;
    string name;
};

void printPersonArray(MyArray<Person> & arr){
    for(int i=0; i<arr.get_size(); i++){
        cout << arr[i].name << arr[i].age << endl;
    }
}



int main () {
    // MyArray<int> arr(7);
    // MyArray<int> arr2(arr);
    // MyArray<int> arr3(100);
    // arr3 = arr2;

    // MyArray<int> arr1(10);
    // for(int i=0; i<5; i++){
    //     arr1.push_back(i);
    // }
    // cout << "size: " << arr1.get_size()<< endl;
    // printMyarray(arr1);
    // arr1.pop_back();
    // printMyarray(arr1);
    // cout << "size: " << arr1.get_size()<< endl;
    // cout << "capacity: " << arr1.get_capacity()<< endl;



    MyArray<Person> arr2(10);

    cout << arr2.get_size()<<endl;
    arr2.push_back(Person(4, "li"));
    arr2.push_back(Person(4, "li"));
    arr2.push_back(Person(4, "li"));
    arr2.push_back(Person(4, "lili"));
    cout << arr2.get_size()<<endl;



    // Person * p = new Person[10];
    printPersonArray(arr2);
    // printPersonArray(arr2);

    return 0;
}


