#include <iostream>
using namespace std;
#include <fstream>

int main() {
    //写文件
    ofstream ofs;
    ofs.open("test.txt", ios::out);
    ofs << "name: zhangsan" << endl;
    ofs << "name: zhangsan" << endl;
    ofs << "name: zhangsan" << endl;
    ofs.close();

    //读文件
    ifstream ifs;
    ifs.open("test.txt", ios::in);
    if (!ifs.is_open()){
        cout << "File open failed." << endl;
        return 1;
    } 

    // method 1
    // char buf[1024] = {0}; //初始化为 0
    // while (ifs >> buf){
    //     cout << buf << endl;
    // }

    //method 2
    // char buf2[1024] = {};
    // while(ifs.getline(buf2, sizeof(buf2))){
    //     cout << buf2 << endl;
    // }

    //method4
    // string buf3;
    // while(getline(ifs, buf3)){
    //     cout << buf3 << endl;
    // }

    //method 4
    char c;
    while((c=ifs.get()) != EOF){
        cout << c;
    }   
    ifs.close();
}