#include<iostream>

using namespace std;
class Building; 

//友元类
class GoodGay {
    public: 
        GoodGay();
        void visit();
        void visit2();
    private: 
        Building * building;
};

class Building{
	//告诉编译器 goodGay全局函数 是 Building类的好朋友，可以访问类中的私有内容
	friend void goodGay(Building * building);
	//告诉编译器 goodGay类是Building类的好朋友，可以访问到Building类中私有内容
	// friend class GoodGay;
    //告诉编译器  goodGay类中的visit成员函数 是Building好朋友，可以访问私有内容
	friend void GoodGay::visit2();

    public:
        Building()	{
            this->m_SittingRoom = "客厅";
            this->m_BedRoom = "卧室";
        }
    public:
        string m_SittingRoom; //客厅
    private:
        string m_BedRoom; //卧室
};

// 友元函数
void goodGay(Building * building) {
	cout << "好基友正在访问： " << building->m_SittingRoom << endl;
	cout << "好基友正在访问： " << building->m_BedRoom << endl;
}


GoodGay::GoodGay() {
    building = new Building;
}
void GoodGay::visit() {
    cout << "Goodgay visiting " << building->m_SittingRoom << endl;
    // cout << "Goodgay visiting " << building->m_BedRoom << endl;
}
void GoodGay::visit2() {
    cout << "Goodgay visiting " << building->m_SittingRoom << endl;
    cout << "Goodgay visiting " << building->m_BedRoom << endl;
}


void test01() {
	// Building b;
	// goodGay(&b);
    GoodGay gg;
    gg.visit();
    gg.visit2();
}

int main(){
	test01();

	return 0;
}