#include<iostream>
using namespace std;

class Base{
    public:
    Base() {
        m_A = 100;
    }
    void func() {
        cout << "Base - func()" << endl;
    }
    int m_A;
    static int m_Static;
};
int Base::m_Static = 1;

class Son: public Base{
    public:
    Son(){
        m_A = 200;
    }
    void func() {
        cout << "Son - func() "<< endl;
    }

    int m_A;
    static int m_Static;
};
int Son::m_Static = 2;

int main() {
    Son s;
    cout << s.m_A << endl;
    cout << s.Base::m_A <<endl;
    cout << s.m_Static << endl;
    cout << s.Base::m_Static << endl;
    
    s.func();
    s.Base::func();
}