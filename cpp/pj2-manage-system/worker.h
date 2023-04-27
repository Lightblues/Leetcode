#pragma once
#include<iostream>
using namespace std;

class Worker{
    public: 
        virtual ~Worker(){};
        // 想要 delete 的时候警告 warning: delete called on 'Worker' that is abstract but has non-virtual destructor
        // 添加了 vitual 的析构函数后正常。
        // 并且只能是 virtual 的
        virtual void showInfo() = 0;
        virtual string getDeptName() = 0;
        int m_Id;
        string m_Name;
        int m_DeptId;
};