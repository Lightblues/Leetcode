#include<array>
#include <iostream>

using namespace std;


int main() {

    array<int, 5> arr;
    //初始化 values2 为{10，11，12，13，14}
    int initvalue = 10;
    // 通过引用的方式赋值
    for (auto& value : arr) {
        value = initvalue;
        initvalue++;
    }
    cout <<  "Values1 is : ";
    for (auto i = arr.begin(); i < arr.end(); i++) {
        cout << *i << " ";
    }
}