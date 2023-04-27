#include<iostream>
#include<string>    //好像不引入也行
using namespace std;

int main () {
    // char str1[13] = "runoob";
    // char str2[14] = "google";
    // char str3[13];
    // int len;

    // strcpy(str3, str1);
    // cout << "strcpy(str3, str1): "<< str3 <<endl;
    // strcat(str1, str2);
    // cout << "strcat(str1, str2): " << str1<<endl;
    // len = strlen(str1);
    // cout << "strlen(str1): " << len << endl;
    
    string str1 = "runoob";
    string str2 = "google";
    string str3;
    int  len ;
    
    // 复制 str1 到 str3
    str3 = str1;
    cout << "str3 : " << str3 << endl;
    
    // 连接 str1 和 str2
    str3 = str1 + str2;
    cout << "str1 + str2 : " << str3 << endl;
    
    // 连接后，str3 的总长度
    len = str3.size();
    cout << "str3.size() :  " << len << endl;
    return 0;
}