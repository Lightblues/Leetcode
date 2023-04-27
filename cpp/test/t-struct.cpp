#include<iostream>
#include<stdio.h>
struct Base {         
    int v1;
   private:
        int v3;
    public:   //显示声明public
        int v2;
    virtual void print(){       
        printf("%s\n","Base");
    };    
};
struct Derived:Base {         

    public:
        int v2;
    void print(){       
        printf("%s\n","Derived");
    };    
};
int main() {
    Base *b=new Derived();
    b->print();
    struct Base bb;
    bb.v2 = 4;
    printf("%d\n", bb.v2);
    return 0;
}