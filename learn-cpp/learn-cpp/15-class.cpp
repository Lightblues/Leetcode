#include<iostream>

using namespace std;

class Box {
    public:
    double length;
    double breadth;
    double height;

    // 成员函数声明
    double get(void);
    void set (double len, double bre, double hei);
};

double Box::get(void) {
    return length * height * breadth;
}

void Box::set(double len, double bre, double hei) {
    length = len;
    breadth = bre;
    height = hei;
}

int main() {
    Box Box1, Box2, Box3;
    double volume = 0.0;

    Box1.height = 5.0;
    Box1.breadth = 6;
    Box1.length = 7;

    Box2.height = 10.0;
    Box2.length = 12.0;
    Box2.breadth = 13.0;
    // box 1 的体积
    volume = Box1.height * Box1.length * Box1.breadth;
    cout << "Box1 的体积：" << volume <<endl;
    
    // box 2 的体积
    volume = Box2.height * Box2.length * Box2.breadth;
    cout << "Box2 的体积：" << volume <<endl;

    Box3.set(16, 8, 12);
    volume = Box3.get();
    cout << volume << endl;

    return 0;
}