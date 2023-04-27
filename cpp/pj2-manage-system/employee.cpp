#include "employee.h"

Employee::Employee(int id, string name, int dId) {
    this->m_Name = name;
    this->m_Id = id;
    this->m_DeptId = dId;
}

void Employee::showInfo(){
    cout << "Id: " << this->m_Id 
        << "\tName: " << this->m_Name 
        << "\tDeptId: " << this->getDeptName() << endl;
}

string Employee::getDeptName() {
    return "employee";
}