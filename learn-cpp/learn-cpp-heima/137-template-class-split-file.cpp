//解决方式1，包含cpp源文件
// #include "137-name.cpp"

//解决方式2，将声明和实现写到一起，文件后缀名改为.hpp
#include "137-name.hpp"

int main() {
    Person<string, int> p("Tommy", 10);
    p.showPerson();
}