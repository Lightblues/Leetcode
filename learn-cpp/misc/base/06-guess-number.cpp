#include<iostream>
#include<ctime>

using namespace std;

int main() {
    srand((unsigned int)time(NULL));    // 随机种子
    int num = rand()%100 + 1;
    int val;

    while (1){
        cin >> val;
        if (val > num){
            cout << "Too big." << endl;
        } else if (val < num) {
            cout << "Too small." << endl;
        } else {
            cout << "You've got it, the num is " << num << endl;
            break;
        }
    }


    return 0;
}