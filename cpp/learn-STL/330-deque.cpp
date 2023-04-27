#include<iostream>
#include<deque>
#include<algorithm>     //sort()
using namespace std;

void printDeque(const deque<int> &d){
    // 用 const 限定不允许修改
    //相应地需要使用 const_iterator 类型，否则会报错
    for (deque<int>::const_iterator it=d.begin(); it<d.end(); it++){
        cout << *it << "\t";
    }
    cout << endl;
}

void test1(){
    // 构造
    deque<int> d;
    for(int i=0; i<10; i++){
        d.push_back(i);
    }
    printDeque(d);

    deque<int> d1(d);
    printDeque(d1);

    deque<int> d2(d.begin(), d.end()-2);
    printDeque(d2);
}

void test5(){
    deque<int> d;
    d.push_back(10);
    d.push_back(11);
    d.push_front(20);
    d.push_front(21);
    printDeque(d);
    
    d.insert(d.begin(), 9);
    d.insert(d.begin(), 2, 999);
    printDeque(d);

    deque<int> d1;
    d1.push_back(111);
    d1.push_back(111);
    d1.insert(d1.begin()+1, d.begin(), d.end()); //还有一种重载的三个参数是三个迭代器，在第一个迭代器位置插入后两个之前的数据
    printDeque(d1);  

    d1.erase(d1.begin()+1, d1.end()-1);
    printDeque(d1);
}

void test7(){
    deque<int> d;
    d.push_back(1);
    d.push_back(5);
    d.push_back(3);
    d.push_back(100);
    printDeque(d);
    sort(d.begin(), d.end());       //事实上支持随机访问的容器都支持 sort()
    printDeque(d);
}





int main () {
    test1();
    cout << endl ;
    test5();
    cout << endl ;
    test7();
    cout << endl ;
}
