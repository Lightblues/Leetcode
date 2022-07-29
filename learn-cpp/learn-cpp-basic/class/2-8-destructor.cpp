#include <iostream>
using namespace std;

class VLA{
public:
    // C++ 中的 new 和 delete 分别用来分配和释放内存，它们与C语言中 malloc()、free() 最大的一个不同之处在于：
    // 用 new 分配内存时会调用构造函数，用 delete 释放内存时会调用析构函数。
    VLA(int len);   //构造函数
    ~VLA();         //析构函数
public:
    void input();   //从控制台输入数组元素
    void show();    //显示数组元素

private:
    // at() 函数只在类的内部使用，所以将它声明为 private 属性
    int *at(int i);  //获取第i个元素的指针
private:
    // m_len 变量不允许修改，所以用 const 进行了限制，这样就只能使用初始化列表来进行赋值
    const int m_len;  //数组长度
    int *m_arr;     //数组指针
    int *m_p;       //指向数组第i个元素的指针
};
VLA::VLA(int len): m_len(len){  //使用初始化列表来给 m_len 赋值
    if(len > 0){ m_arr = new int[len];  /*分配内存*/ }
    else{ m_arr = NULL; }
}
VLA::~VLA(){
    delete[] m_arr;  //释放内存
}
void VLA::input(){
    for(int i=0; m_p=at(i); i++){ cin>>*at(i); }
}
void VLA::show(){
    for(int i=0; m_p=at(i); i++){
        if(i == m_len - 1){ cout<<*at(i)<<endl; }
        else{ cout<<*at(i)<<", "; }
    }
}
int * VLA::at(int i){
    if(!m_arr || i<0 || i>=m_len){ return NULL; }
    else{ return m_arr + i; }
}

int main(){
    //创建一个有n个元素的数组（对象）
    int n;
    cout<<"Input array length: ";
    cin>>n;
    VLA *parr = new VLA(n);
    //输入数组元素
    cout<<"Input "<<n<<" numbers: ";
    parr -> input();
    //输出数组元素
    cout<<"Elements: ";
    parr -> show();
    //删除数组（对象）
    delete parr;
    return 0;
}