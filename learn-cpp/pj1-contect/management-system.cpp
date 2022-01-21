#include<iostream>
#define MAX 1000

using namespace std;

struct Person {
    string m_Name;
    int m_Sex;
    int m_Age;
    string m_Phone;
    string m_Addr;
};

struct Addressbooks {
    struct Person personArray[MAX];
    int m_Size;
};

void showManu() {
    cout << "***************************" << endl;
	cout << "*****  1、添加联系人  *****" << endl;
	cout << "*****  2、显示联系人  *****" << endl;
	cout << "*****  3、删除联系人  *****" << endl;
	cout << "*****  4、查找联系人  *****" << endl;
	// cout << "*****  5、修改联系人  *****" << endl;
	// cout << "*****  6、清空联系人  *****" << endl;
	cout << "*****  0、退出通讯录  *****" << endl;
	cout << "***************************" << endl;
}


void addPerson(Addressbooks *abs) {
    if (abs->m_Size==MAX) {
        cout << "The contect book is full(1000)." <<endl;
        return;
    } else {
        //name
        string name;
        cout << "name: ";
        cin >> name;
        abs->personArray[abs->m_Size].m_Name = name;
        // cout << "add success" << endl;

        //sex
        int sex = 0;
        cout << "sex. 1 for male, 2 for female: ";
        while (true){
            cin >> sex;
            if (sex==1 || sex==2){
                abs->personArray[abs->m_Size].m_Sex = sex;
                break;
            } else {
                cout << "Error. please input again. ";
            }
        }

        //age
        cout << "age: ";
        int age = 0;
        cin >> age;
        abs->personArray[abs->m_Size].m_Age = age;

        //phone
        cout << "phone: ";
        string phone = "";
        cin >> phone;
        abs->personArray[abs->m_Size].m_Phone = phone;

        //addr
        cout << "addr: ";
        string addr;
        cin >> addr;
        abs->personArray[abs->m_Size].m_Addr = addr;

        abs->m_Size++;

        cout << "Success!" << endl;

        // system('cls');
    }
}


void showPerson(Addressbooks * abs) {
    if (abs->m_Size==0){
        cout << "Addressbook is empty" << endl;
    }
    for (int i=0; i<abs->m_Size; i++){
        cout << abs->personArray[i].m_Name << "\t" <<
            abs->personArray[i].m_Sex << "\t" <<
            abs->personArray[i].m_Age << "\t" <<
            abs->personArray[i].m_Phone << "\t" <<
            abs->personArray[i].m_Addr  << endl;
    }
}




int isExist(Addressbooks *abs, string name) {
    for (int i=0; i< abs->m_Size; i++){
        if (abs->personArray[i].m_Name == name) {
            return i;
        }
    }
    return -1;
}

void deletePerson(Addressbooks * abs) {
    cout << "The person to be deleted: ";
    string name;
    cin >> name;

    int ret = isExist(abs, name);
    if (ret == -1){
        cout << "There is no person name this." << endl;
    } else {
        for (int i=ret; i < abs->m_Size; i++) {
            abs->personArray[i] = abs->personArray[i+1];
        }
        abs->m_Size --;
        cout << "delete succeed" << endl;
    }
}

void showOne(Addressbooks *abs, int i){
    cout << abs->personArray[i].m_Name << "\t" <<
            abs->personArray[i].m_Sex << "\t" <<
            abs->personArray[i].m_Age << "\t" <<
            abs->personArray[i].m_Phone << "\t" <<
            abs->personArray[i].m_Addr  << endl;
}


void findPerson(Addressbooks *abs) {
    cout << "The person to be shown: ";
    string name;
    cin >> name;

    int ret = isExist(abs, name);
    if (ret == -1){
        cout << "No such person. "<<endl;
    } else {
        showOne(abs, ret);
    }
}

int main() {
    int select = 9;

    struct Addressbooks abs;
    abs.m_Size = 0;     //注意需要初始化为 0

    while(true) {
        showManu();
        cin >> select;

        switch (select)
        {
        case 1:
            addPerson(&abs);
            break;
        case 2:
            showPerson(&abs);
            break;
        case 3:
            deletePerson(&abs);
            break;
        case 4:
            findPerson(&abs);
            break;
        case 0:
            cout << "bye~" << endl;
            // break;
            return 0;
        default:
            break;
        }
    }
    



    return 0;
}