#include<iostream>
using namespace std;

class MyPrint{
    public:
    //重载的（）操作符 也称为仿函数
    void operator()(string text){
        cout << text << endl;
    }
};

class MyAdd{
    public:
    int operator()(int a, int b){
        return a+b;
    }
};


int main () {
    MyPrint p;
    p("something");
    //匿名对象调用  
    MyPrint()("hifahdi");

    MyAdd a;
    int result = a(1,2);
    //匿名对象调用  
    cout << result << MyAdd()(1,2) << endl;
}