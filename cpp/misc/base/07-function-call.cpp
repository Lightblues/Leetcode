#include <iostream>
using namespace std;
 
// 函数声明
// void swap_reference(int &x, int &y);

// 引用的方式传递参数
void swap_reference(int &x, int &y)
{
   int temp;

//    cout << x << y <<endl;
   temp = x; /* 保存地址 x 的值 */
   x = y;    /* 把 y 赋值给 x */
   y = temp; /* 把 x 赋值给 y  */
  
   return;
}

// 指针的方式传递参数
void swap_pointer(int *x, int *y) {
    int temp;
    temp = *x;
    *x = *y;
    *y = temp;
}
 
int main ()
{
    // 局部变量声明
    int a = 100;
    int b = 200;
    
    cout << "交换前，a 的值：" << a << endl;
    cout << "交换前，b 的值：" << b << endl;
    
    /* 调用函数来交换值 */
    swap_reference(a, b);
    // swap_pointer(&a, &b);
 
   cout << "交换后，a 的值：" << a << endl;
   cout << "交换后，b 的值：" << b << endl;
 
   return 0;
}

// 函数定义
