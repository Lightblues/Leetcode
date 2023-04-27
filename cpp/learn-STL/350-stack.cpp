#include<iostream>
#include<stack>

using namespace std;

void test1(){
    stack<int> s;
    s.push(1);
    s.push(2);
    s.push(3);

    while (!s.empty()) {
		//输出栈顶元素
		cout << "栈顶元素为： " << s.top() << endl;
		//弹出栈顶元素
		s.pop();
	}
	cout << "栈的大小为：" << s.size() << endl;
}

int main(){
    test1();
}