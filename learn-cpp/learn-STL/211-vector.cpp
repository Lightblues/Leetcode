#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

void myPrint(int val){
    cout << val << endl;
}

int main() {
    vector<int> v;
    v.push_back(10);
    v.push_back(20);
    v.push_back(30);
    v.push_back(40);
    
    // 三种遍历方式
    //1
    vector<int>::iterator itBegin = v.begin();
    vector<int>::iterator itEnd = v.end();
    while (itBegin != itEnd){
        cout << *itBegin++ << endl;
    }
    //2
    for(vector<int>::iterator it=v.begin(); it!= v.end() ;it++){
        cout << *it << endl;
    }
    //3
    //使用STL提供标准遍历算法  头文件 algorithm
    for_each(v.begin(), v.end(), myPrint);      //右键「转到定义」，似乎是 inline 的。
}