#include<iostream>
#include<queue>
#include<string>

using namespace std;

class Person{
    public:
    Person(string name, int age){
        this->m_name = name;
        this->m_age = age;
    }
    string m_name;
    int m_age;
};

void test1(){
    queue<Person> q;
    q.push(Person("zhang", 12));
    q.push(Person("li", 23));
    q.push(Person("wang", 23));

    //队列不提供迭代器，更不支持随机访问
    while(!q.empty()){
        cout << "front: " << q.front().m_name << q.front().m_age << endl;
        cout << "bask: " << q.back().m_name << q.back().m_age << endl;

        q.pop();
        cout << "size: " << q.size() << endl;
    }


}

int main(){
    test1();
}