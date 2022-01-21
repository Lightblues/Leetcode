#include<iostream>
using namespace std;

int main() {
    // 下面的三个字符串字面量一致
    string s = "hello, \
dear";
    s = "hello, " "d" "ear";
    s = "hello, dear";
    cout << s <<endl;



}