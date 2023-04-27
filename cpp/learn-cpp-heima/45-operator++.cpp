#include<iostream>
using namespace std;

class MyInteger {
    friend ostream & operator<< (ostream & out, MyInteger i);

    public:
        MyInteger(){
            m_int = 0;
        }
        MyInteger & operator++(){
            this->m_int++;
            return *this;
        }
        MyInteger operator++(int){
            MyInteger temp = *this;
            this->m_int++;
            return temp;
        }

    private:   
        int m_int;
};

ostream & operator<< (ostream & out, MyInteger i){
    out << i.m_int;
    return out;
}

int main() {
    MyInteger i;
    cout << ++(++i) << endl;
    cout << i << endl;

    cout << i++ << endl;
    cout << i << endl;
    //int 类型也不支持 (i++)++ 运算
    int a = 0;
    cout << a++ << endl;
}