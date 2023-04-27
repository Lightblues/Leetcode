#include <iostream>
 
using namespace std;
 
class Line
{
   public:
      int getLength( void );
      Line( int len );             // 简单的构造函数
      Line( const Line &obj);      // 拷贝构造函数
      ~Line();                     // 析构函数
 
   private:
      int *ptr;
};
 
// 成员函数定义，包括构造函数
Line::Line(int len){
    cout << "调用构造函数" << endl;
    // 为指针分配内存
    // ptr = new int;
    *ptr = len;
}
 
Line::Line(const Line &obj){
    cout << "调用拷贝构造函数并为指针 ptr 分配内存" << endl;
    // ptr = new int;
    *ptr = *obj.ptr; // 拷贝值
}
 
Line::~Line(void){
    cout << "释放内存" << endl;
    // delete ptr;
}

int Line::getLength( void ){
    return *ptr;
}


void display(Line obj){
   cout << "line 大小 : " << obj.getLength() <<endl;
}


//用引用的方式调用就不会用到拷贝构造函数
// void display(Line &obj) {
//     cout << "line length: " << obj.getLength() << endl;
// }
 


// 程序的主函数
int main( ){
   Line line(10);
 
   display(line);
 
   return 0;
}