#include<iostream>
#include<fstream>
using namespace std;

class Person {
    public:
    // char m_name[64];
    string m_name;
    int m_age;
};

int main () {
    ofstream ofs("person.txt", ios::out | ios::binary);
    Person p = {"张三", 34};
    ofs.write((char *)&p, sizeof(p));
    ofs.close();


    ifstream ifs;
    ifs.open("person.txt", ios::in | ios::binary);
    if (!ifs.is_open()){
        cout << "Open file failed." << endl;
        return 1;
    }

    Person p2;
    ifs.read((char *)&p2, sizeof(p2));
    cout << "name: " << p2.m_name << "\tage: " << p2.m_age << endl;

    ifs.close();
}