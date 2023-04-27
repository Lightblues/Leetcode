#pragma once //防止一个头文件被包含两次
#include<iostream>
using namespace std;
#include "worker.h"
#include <fstream>
#define FILENAME "empFile.txt"

class WorkerManager {
    public: 
        // constructor
        WorkerManager ();
        // deconstructor
        ~WorkerManager () ;

        //show
        void ShowMenu();
        void exitSystem();

        int m_EmpNum;
        Worker ** m_EmpArray;
        void Add_Emp();

        void save();

        bool m_FileIsEmpty; //标志文件是否为空

        int get_EmpNum();

        void init_Emp();

        void Show_Emp();

        void Del_Emp();

        int isExist(int id);

        void Sort_Emp();

        void Clean_File();
};