#include<iostream>
using namespace std;

class AbstractDrinking{
    public:
    virtual void Boil() = 0;
    virtual void Brew() = 0;
    virtual void PourInCup() = 0;
    virtual void PutSomething() = 0;

    void MakeDrink() {
        Boil();
        Brew();
        PourInCup();
        PutSomething();
    }
};

class Coffee: public AbstractDrinking{
    void Boil() {
        cout << "Boilint water..." << endl;
    }
    void Brew() {
        cout << "Brewing coffee..." << endl;
    }
    void PourInCup() {
        cout << "Pouring into cup..." << endl;
    }
    void PutSomething() {
        cout << "Adding milk..." << endl;
    }
};

class Tea: public AbstractDrinking{
    void Boil() {
        cout << "Boiling water..." << endl;
    }
    void Brew() {
        cout << "Brewing tea..." << endl;
    }
    void PourInCup() {
        cout << "Pouring into cup..." << endl;
    }
    void PutSomething() {
        cout << "Adding gouqi..." << endl;
    }
};


void doWork(AbstractDrinking* drink){
    drink->MakeDrink();
    // delete drink;
}

int main () {
    AbstractDrinking * drink;
    drink = new Coffee;
    doWork(drink);
    drink = new Tea;
    doWork(drink);
}