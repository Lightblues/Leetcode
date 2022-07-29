/* 侯杰 */

#include <iostream>

using namespace std;

class complex
{
public:

    // 构造函数, 给定了默认值的情况下, 支持不同的参数传递方式
    complex(double r = 0, double i = 0) : re(r), im(i){};
    // 再写下面的构造函数和默认值形式的冲突了!
    // complex(): re(5), im(5){};

    void show()
    {
        cout << re << " + " << im << "i" << endl;
    }

    // const member function 常数成员函数
    // 在函数 () 后面加 const, 说明不会概念成员变量
    // 作用: `const complex c(2,1)` 来创建一个常量复数, 再调用 `c.real()` 会报错 reference to overloaded function could not be resolved;!!
    double real () const { return re; }
    double imag () const { return im; }
    // 函数重载: 设置值
    void real (double r) { re = r; }

private:
    double re, im;
};

int main(int argc, char const *argv[])
{
    complex c1(1, 2), c2(2), c3;
    c1.show();
    c2.show();
    c3.show();
}
