#include<iostream>
#include<list>
using namespace std;

void printList(const list<int> &l){
    for(list<int>::const_iterator it=l.begin(); it!=l.end(); it++){ //注意到不同于 vector 这里的 it 没有 < 比较只能用 !=
        cout << *it << '\t';        
    }
    cout << endl;
}

void test1(){
    list<int> l;
    l.push_back(1);
    l.push_back(2);
    l.push_back(3);
    l.push_back(4);
    printList(l);

    list<int> l1(l);
    printList(l1);

    list<int> l2(l.begin(), l.end());
    printList(l2);

    list<int> l3(3, 999);
    printList(l3);
}

void test5(){
    // 插入与删除
    list<int> l;
    l.push_back(1);
    l.push_back(11);
    l.push_front(2);
    l.push_front(22);
    printList(l);

    l.pop_front();
    l.pop_back();
    printList(l);

    list<int>::iterator it = l.begin();
    l.insert(++it, 1000);
    printList(l);

    it = ++l.begin(); // 注意 ++ 只能前缀
    l.erase(it);
    printList(l);

    l.erase(++l.begin(), --l.end()); // 这里也是
    printList(l);

    l.push_front(111);
    l.push_front(111);
    l.push_back(111);
    printList(l);
    l.remove(111);      //注意这里多了一个 remove 函数，将 list 中所有的该元素删去。
    printList(l);
}

int main() {
    test1();
    cout << endl;
    test5();
}