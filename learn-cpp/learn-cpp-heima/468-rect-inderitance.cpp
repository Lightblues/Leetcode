#include<iostream>
using namespace std;

class Animal{
    public:
    int m_Age;
};

//继承前加virtual关键字后，变为虚继承
//此时公共的父类Animal称为虚基类
class Sheep: public virtual Animal{};
class Tuo: virtual public Animal{};

class SheepTuo: public Sheep, public Tuo{};


int main() {
    SheepTuo st;
    st.Sheep::m_Age = 25;
    st.Tuo::m_Age = 28;
    cout << sizeof(st) << endl;
    cout << st.Sheep::m_Age << st.Tuo::Tuo::m_Age << st.m_Age << endl;

}
