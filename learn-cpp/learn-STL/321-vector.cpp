#include<vector>
#include <iostream>

using namespace std;

void printVector(vector<int> &v){
    for(vector<int>::iterator it=v.begin(); it<v.end(); it++){
        cout << * it << "\t";
    }
    cout << endl;
}

void test1(){
    // 构造
    vector<int> v1;
    for(int i=0; i<10; i++){
        // v1[i] = i;
        v1.push_back(i+100);
    }
    printVector(v1);

    vector<int> v2(v1.begin(), v1.end());
    printVector(v2);

    vector<int> v3(5, 99);
    printVector(v3);

    vector<int> v4(v3);
    printVector(v4);

}

void test2(){
    // 赋值
    vector<int> v;
    for(int i=0; i<5; i++){
        v.push_back(i);
    }

    vector<int> v1, v2, v3;
    v1 = v;
    printVector(v1);
    
    v2.assign(v1.begin(), v1.end());
    printVector(v2);

    v2.assign(4, 999);  //赋值 4 个 999，注意会覆盖
    printVector(v2);
}

void test3(){
    vector<int> v1;
    for(int i=0; i<10; i++){
        v1.push_back(i);
    }
    printVector(v1);
    cout << "empty(): " << v1.empty() << endl;
    cout << "capacity(): "<< v1.capacity() << endl;
    cout << "size():" << v1.size() << endl;
    v1.resize(15, -1);  // 若指定长度超过，则用第二个参数填充，默认为 0；短则截断
    printVector(v1);
    v1.resize(5);
    printVector(v1);
}

void test4(){
    // 插入和删除
    vector<int> v;
    for(int i=1; i<6; i++){
        v.push_back(i*10);
    }
    printVector(v);

    v.pop_back();
    printVector(v);

    v.insert(v.begin(), 100);
    printVector(v);
    v.insert(v.begin(), 2, 22);
    printVector(v);

    v.erase(v.begin());
    printVector(v);
    v.erase(v.begin(), v.end()-3); //注意 end 指向最后下一个元素
    printVector(v);

    v.clear();
    printVector(v);
}

void test5(){
    //数据存取
    vector<int> v;
    // cout << "here" << endl;
    for(int i=0; i<10; i++){
        v.push_back(i);
    }
    printVector(v);
    for (int i=0; i<10; i++){
        // cout << v[i] << "\t";
        cout << v.at(i) << "\t";
    }
    cout << endl;

    cout << v.front() << v.back() << endl;
}

void test6(){
    vector<int> v;
	for (int i = 0; i < 100000; i++) {
		v.push_back(i);
	}

	cout << "v的容量为：" << v.capacity() << endl;
	cout << "v的大小为：" << v.size() << endl;

	v.resize(3);

	cout << "v的容量为：" << v.capacity() << endl;
	cout << "v的大小为：" << v.size() << endl;

	//收缩内存
	vector<int>(v).swap(v); //匿名对象

	cout << "v的容量为：" << v.capacity() << endl;
	cout << "v的大小为：" << v.size() << endl;
}

void test7(){
    vector<int> v;

    // v.reserve(100000); // 预留空间

    int num = 0;
    int * p = NULL;
    for(int i=0; i<100000; i++){
        v.push_back(i);
        if(p != &v[0]){
            num++;
        }
        p = &v[0];
    }

    cout << v.capacity() << endl;
    v.reserve(100);     //不会缩小（因为小于 size？）
    cout << v.capacity() <<endl;
    v.reserve(200000);
    cout << v.capacity() << endl;

}

int main(){
    test1();
    cout << endl;
    test2();
    cout << endl;
    test3();
    cout << endl;
    test4();
    cout << endl;
    test5();
    cout << endl;
    test6();
    cout << endl;
    test7();
}