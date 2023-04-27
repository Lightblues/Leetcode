#include "workerManager.h"
#include "employee.h"
#include "manager.h" 
#include "boss.h"

WorkerManager::WorkerManager() {
    this->m_EmpNum = 0;
    this->m_EmpArray = NULL;

    // 情况 1：第一次使用，文件未创建
    ifstream ifs;
    ifs.open(FILENAME, ios::in);
    if(!ifs.is_open()){
        cout << "There is no such file." << endl;
        this->m_EmpNum = 0;
        this->m_EmpArray = NULL;
        this->m_FileIsEmpty = true;
        return;
    }

    // 情况 2：文件存在，但是数据被用户清空
    char ch;
    ifs >> ch;
    if(ifs.eof()){
        cout << "File is empty!" <<endl;
        this->m_EmpNum = 0;
        this->m_EmpArray = NULL;
        this->m_FileIsEmpty = true;
        return;
    }

    // 情况 3：文件存在，并且保存职工的所有数据
    // 在 Add_Emp() 中修改 this->m_FileIsEmpty 标记
    int num = this->get_EmpNum();
    cout << "Worker number: " << num << endl;
    this->m_EmpNum = num;

    // 创建职工数组
    this->m_EmpArray = new Worker *[this->m_EmpNum];
    this->init_Emp();

    //测试代码
	for (int i = 0; i < m_EmpNum; i++)
	{
		cout << "职工号： " << this->m_EmpArray[i]->m_Id
			<< " 职工姓名： " << this->m_EmpArray[i]->m_Name
			<< " 部门编号： " << this->m_EmpArray[i]->m_DeptId << endl;
	}

}

WorkerManager::~WorkerManager() {
    delete[] this->m_EmpArray;      //释放堆区数据
}

void WorkerManager::ShowMenu() {
	cout << "********************************************" << endl;
	cout << "*********  欢迎使用职工管理系统！ **********" << endl;
	cout << "*************  0.退出管理程序  *************" << endl;
	cout << "*************  1.增加职工信息  *************" << endl;
	cout << "*************  2.显示职工信息  *************" << endl;
	cout << "*************  3.删除离职职工  *************" << endl;
	// cout << "*************  4.修改职工信息  *************" << endl;
	// cout << "*************  5.查找职工信息  *************" << endl;
	cout << "*************  6.按照编号排序  *************" << endl;
	cout << "*************  7.清空所有文档  *************" << endl;
	cout << "********************************************" << endl;
	cout << endl;
}

void WorkerManager::exitSystem() {
    cout << "Bye~" << endl;
    exit(0);
}

void WorkerManager::Add_Emp() {
    cout << "The number of worker to be added: ";
    int addNum = 0;
    cin >> addNum;
    if (addNum > 0){
        int newSize = this->m_EmpNum + addNum;
        Worker ** newSpace = new Worker*[newSize];
        if (this->m_EmpArray != NULL) {
            for (int i=0; i<this->m_EmpNum; i++){
                newSpace[i] = this->m_EmpArray[i];
            }
        }
        for(int i=0; i<addNum; i++){
            int id;
            string name;
            int dSelect;
            cout << "请输入第 " << i + 1 << " 个新职工编号：" << endl;
			cin >> id;
			cout << "请输入第 " << i + 1 << " 个新职工姓名：" << endl;
			cin >> name;
			cout << "请选择该职工的岗位：" << endl;
			cout << "1、普通职工" << endl;
			cout << "2、经理" << endl;
			cout << "3、老板" << endl;
			cin >> dSelect;

            Worker * worker = NULL;
            switch (dSelect)
            {
            case 1:
                worker = new Employee(id, name, 1);
                break;
            case 2: 
                worker = new Manager(id, name, 2);
                break;
            case 3:
                worker = new Boss(id, name, 3);
                break;
            default:
                break;
            }
            newSpace[this->m_EmpNum+i] = worker;
            // 误写成了 newSpce[i] = worker; 结果在写入的时候报错 Segmentation fault in Linux ？

        }
        delete[] this->m_EmpArray;
        this->m_EmpArray = newSpace;
        this->m_EmpNum = newSize;
        cout << "Succeed" << endl;
        this->m_FileIsEmpty = false;
        this->save(); //保存到文件
        
    }
}

void WorkerManager::save() {
    ofstream ofs;
    ofs.open(FILENAME, ios::out);

    for (int i=0; i<this->m_EmpNum; i++) {
        ofs << this->m_EmpArray[i]->m_Id << "\t" 
            << this->m_EmpArray[i]->m_Name << "\t" 
            << this->m_EmpArray[i]->m_DeptId << "\t" <<endl;
    }
    ofs.close();
}

int WorkerManager::get_EmpNum(){
    ifstream ifs;
    ifs.open(FILENAME, ios::in);
    int id;
    string name;
    int dId;

    int num = 0;

    while(ifs >> id && ifs>>name && ifs>>dId) {
        num++;
    }
    ifs.close();
    return num;
}

void WorkerManager::init_Emp(){

    ifstream ifs;
    ifs.open(FILENAME, ios::in);
    int id;
    string name;
    int dId;
    int index = 0;
    while(ifs>>id && ifs>>name && ifs>>dId) {
        Worker * worker = NULL;
        if (dId==1){
            worker = new Employee(id, name, dId);
        } else if (dId==2){
            worker = new Manager(id, name, dId);
        } else {
            worker = new Boss(id, name, dId);
        }
        this->m_EmpArray[index] = worker;
        index++;
    }
}


void WorkerManager::Show_Emp(){
    if (this->m_FileIsEmpty){
        cout << "File non-exist or empty!"<< endl;
    } else {
        for (int i=0; i<this->m_EmpNum; i++){
            this->m_EmpArray[i]->showInfo();
        }
    }
}

void WorkerManager::Del_Emp(){
    if(this->m_FileIsEmpty){
        cout << "File non-exist or empty/n";
    } else {
        cout << "Input the ID: "<<endl;
        int id = 0;
        cin >>id;

        int index = this->isExist(id);
        if(index != -1){
            for (int i=index; i<this->m_EmpNum-1; i++){
                this->m_EmpArray[i] = this->m_EmpArray[i+1];
            }
            this->m_EmpNum--;
            this->save();
            cout << "Success" <<endl;
        } else {
            cout << "There is no such ID." << endl; 
        }
    }
}

int WorkerManager::isExist(int id) {
    int index = -1;
    for (int i=0; i<this->m_EmpNum; i++){
        if(this->m_EmpArray[i]->m_Id == id){
            index = i;
            break;
        }
    }
    return index;
}

void WorkerManager::Sort_Emp(){
    if(this->m_FileIsEmpty){
        cout << "File non-exist or empty/n";
    }
    cout << "1 for sorting increasingly and 2 for decreasingly. ";
    int select = 0;
    cin >> select;
    for (int i=0; i<this->m_EmpNum; i++){
        int minOrMax = i;
        for(int j=i+1; j<this->m_EmpNum; j++){  // 升序，找最小
            if (select==1){
                if (m_EmpArray[minOrMax]->m_Id > m_EmpArray[j]->m_Id){
                    minOrMax = j;
                }
            } else {
                if (m_EmpArray[minOrMax]->m_Id < m_EmpArray[j]->m_Id){
                    minOrMax = j;
                }
            }
        }
        if (i != minOrMax){
            Worker * temp = this->m_EmpArray[i];
            this->m_EmpArray[i] = this->m_EmpArray[minOrMax];
            this->m_EmpArray[minOrMax] = temp;
        }
    }
    cout << "the result: " << endl;
    this->Show_Emp();
}

void WorkerManager::Clean_File(){
    ofstream ofs(FILENAME, ios::trunc);
    ofs.close();
    // cout << "Success clean file." <<endl;

    if (this->m_EmpArray != NULL){
        for(int i=0; i< this->m_EmpNum; i++){
            delete this->m_EmpArray[i];
            // 报错 warning: delete called on 'Worker' that is abstract but has non-virtual destructor
            // 在基类 Worker 中加上 Virtual 析构函数后解决。
            // from <https://stackoverflow.com/questions/8764353/what-does-has-virtual-method-but-non-virtual-destructor-warning-mean-durin>
            this->m_EmpArray[i] = NULL;
        }
        this->m_EmpNum = 0;
        delete[] this->m_EmpArray;
        this->m_EmpArray = NULL;
        this->m_FileIsEmpty = true;
    }
    cout << "Success" <<endl;
}
