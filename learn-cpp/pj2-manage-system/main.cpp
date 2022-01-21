
#include<iostream>
using namespace std;
#include "workerManager.h"
#include "worker.h"
#include "employee.h"
#include "manager.h"
#include "boss.h"

// void test() {
//     Worker * worker = NULL;
//     worker = new Employee(1, "zhangsan", 1);
//     worker->showInfo();
//     worker = new Manager(2, "lisi", 2);
//     worker->showInfo();
//     worker = new Boss(3, "wangwu", 3);
//     worker->showInfo();
// }

int main() {
    // test();

    // 菜单逻辑
    WorkerManager wm;
    int choice = 9;
    while(true) {
        wm.ShowMenu();
        cout << "Input command: " << endl;
        cin >> choice;
        switch (choice)
        {
        case 0:
            wm.exitSystem();
            break;
        case 1: 
            wm.Add_Emp();
            break;
        case 2:
            wm.Show_Emp();
            break;
        case 3:
            wm.Del_Emp();
            break;
        case 6:
            wm.Sort_Emp();
            break;
        case 7:
            wm.Clean_File();
            break;
        default:
            break;
        }
    }
    


    return 0;
}