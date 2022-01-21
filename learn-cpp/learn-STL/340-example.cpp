#include<iostream>
#include<vector>
#include<deque>
#include<algorithm>
#include <string>
#include<ctime>
using namespace std;

class Person{
    public:
    Person(string name, int score){
        this->name = name;
        this->score = score;
    }

    string name;
    int score;
};

void createPerson(vector<Person> &pv){
    string names = "ABCDE";
    for(int i=0; i<5; i++){
        string name = "Person"; //注意不能写成 string name = "Person" + names[i]; 这样就变成 C 中的字符串+char 类型错误？
        name += names[i];
        pv.push_back(Person(name, 0));
    }
}

void showPerson(vector<Person> &pv){
    for(int i=0; i<pv.size(); i++){
        cout << pv[i].name << "\t" << pv[i].score << endl;
    }
}
// void showPerson(vector<Person> &pv){
//     for(vector<Person>::iterator it=pv.begin(); it<pv.end(); it++){
//         cout << (*it).name << "\t" << (*it).score << endl;
//     }
// }

void setScore(vector<Person> &pv){
    for(vector<Person>::iterator it=pv.begin(); it<pv.end(); it++){
        deque<int> d;
        cout << it->name<<endl;

        for (int i=0; i<10; i++){
            int score = rand() %41 + 60;        //生成 60-100 的随机数
            d.push_back(score);
        }
        sort(d.begin(), d.end());
        cout << "scores:" ;
        for (int i=0; i<d.size(); i++){
            cout << "\t" << d[i];
        }
        cout << endl;
        d.pop_back();
        d.pop_front();

        int sum = 0;
        for(int i=0; i<10; i++){
            sum += d[i];
        }
        int avg = sum / d.size();
        cout << "avg: " << avg <<endl;
        it->score = avg;
    }
}

int main() {
    srand((unsigned int)time(NULL)); //初始化随机数种子，否则每次运行结果一样

    vector<Person> v;
    createPerson(v);
    // showPerson(v);
    setScore(v);
    showPerson(v);
}