#include <iostream>

using namespace std;

void test1(){
    //构造
    string s1;
    const char *str = "hello, world";
    // s1 = str;
    string s2(str);
    string s3(s2);
    string s4(10, 'a');
    cout << endl<< s2 << endl << s3<< endl<< s4 << endl; 
}

void test2(){
    string s1;
    string str = "string";
    //赋值
    s1 = str;
    cout << s1<< endl;
    s1 = 'a';
    cout << s1<< endl;
    s1.assign("using assign");
    cout << s1<< endl;
    s1.assign("assign", 2);
    cout << s1<< endl;
    s1.assign(10, 'w');
    cout << s1<< endl;
}

void test3() {
    string s1;
    //拼接
    s1 = "string1";
    s1 += "string2";
    s1 += 'c';
    cout << s1<< endl;
    s1 = "";
    s1.append("abcdefg", 4);
    s1.append("1234567890", 3, 3);
    cout << s1<< endl;
}

void test4() {
    //查找
    string s1("abcdefghijk");
    int pos = s1.find("de");
    if (pos==-1){
        cout << "not found" << endl;
    } else {
        cout << "Position: " << pos << endl;
    }
    pos = s1.rfind("de");
    cout << pos << endl;

    //替换
    s1.replace(2,3, "1111111"); //将第 2 个字符开始的 3 个，替换为第三个参数
    cout << s1 << endl;
}

void test5(){
    //比较
    string s1 = "hello";
	string s2 = "aello";

	int ret = s1.compare(s2);

	if (ret == 0) {
		cout << "s1 等于 s2" << endl;
	} 	else if (ret > 0)	{
		cout << "s1 大于 s2" << endl;
	}	else	{
		cout << "s1 小于 s2" << endl;
	}
}

void test6(){
    string s = "hello";
    cout  << s[0] << s.at(1) << endl;
    s[0] = 'H';
    cout << s << endl;
}

void test7(){
    //插入删除
    string s = "Hello";
    s.insert(3, "[inserted]");
    cout << s << endl;
    s.erase(3, 10);
    cout << s << endl;

    //子串
    cout << s.substr(2, 3) << endl; //从第 2 个字符开始的 3 个
}


int main() {
    test1();
    cout << "--------------"<<endl;
    test2();
    cout << "--------------"<<endl;
    test3();
    cout << "--------------"<<endl;
    test4();
    cout << "--------------"<<endl;
    test5();
    cout << "--------------"<<endl;
    test6();
    cout << "--------------"<<endl;
    test7();
    cout << "--------------"<<endl;
}