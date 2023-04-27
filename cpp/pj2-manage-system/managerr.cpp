#include "manager.h"

Manager::Manager(int id, string name, int dId) {
    this->m_Name = name;
    this->m_Id = id;
    this->m_DeptId = dId;
}

void Manager::showInfo(){
    cout << "Id: " << this->m_Id 
        << "\tName: " << this->m_Name 
        << "\tDeptId: " << this->getDeptName() << endl;
}

string Manager::getDeptName() {
    return "manager";
}