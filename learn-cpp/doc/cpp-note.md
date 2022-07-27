
Make 参见 [[cpp-make.md]]

## C++ STL

- CPP reference: <https://zh.cppreference.com/w/cpp/container> #3 速查, 表格很完全
- biancheng.net: <http://c.biancheng.net/stl/sequence_container/>

STL 最初由惠普实验室开发，于 1998 年被定为国际标准，正式成为 C++ 程序库的重要组成部分。值得一提的是，如今 STL 已完全被内置到支持 C++ 的编译器中，无需额外安装，这可能也是 STL 被广泛使用的原因之一。


- 序列容器: 主要包括 vector 向量容器、list 列表容器以及 deque 双端队列容器。之所以被称为序列容器，是因为元素在容器中的位置同元素的值无关，即容器不是排序的。将元素插入容器时，指定在什么位置，元素就会位于什么位置。
- 排序容器: 包括 set 集合容器、multiset多重集合容器、map映射容器以及 multimap 多重映射容器。排序容器中的元素默认是由小到大排序好的，即便是插入元素，元素也会插入到适当位置。所以关联容器在查找时具有非常好的性能。
- 哈希容器: C++ 11 新加入 4 种关联式容器，分别是 unordered_set 哈希集合、unordered_multiset 哈希多重集合、unordered_map 哈希映射以及 unordered_multimap 哈希多重映射。和排序容器不同，哈希容器中的元素是未排序的，元素的位置由哈希函数确定。

### STL序列式容器

#### 迭代器

既然类似，完全可以利用泛型技术，将它们设计成适用所有容器的通用算法，从而将容器和算法分离开。但实现此目的需要有一个类似中介的装置，它除了要具有对容器进行遍历读写数据的能力之外，还要能对外隐藏容器的内部差异，从而以统一的界面向算法传送数据。

这是泛型思维发展的必然结果，于是迭代器就产生了。简单来讲，迭代器和 C++ 的指针非常类似，它可以是需要的任意类型，通过迭代器可以指向容器中的某个元素，如果需要，还可以对该元素进行读/写操作。

1) 前向迭代器（forward iterator）  
假设 p 是一个前向迭代器，则 p 支持 `++p，p++，*p` 操作，还可以被复制或赋值，可以用 == 和 != 运算符进行比较。此外，两个正向迭代器可以互相赋值。  
  
2) 双向迭代器（bidirectional iterator）  
双向迭代器具有正向迭代器的全部功能，除此之外，假设 p 是一个双向迭代器，则还可以进行 --p 或者 p-- 操作（即一次向后移动一个位置）。  
  
3) 随机访问迭代器（random access iterator）  
随机访问迭代器具有双向迭代器的全部功能。除此之外，假设 p 是一个随机访问迭代器，i 是一个整型变量或常量，则 p 还支持以下操作：

- p+=i：使得 p 往后移动 i 个元素。
- p-=i：使得 p 往前移动 i 个元素。
- p+i：返回 p 后面第 i 个元素的迭代器。
- p-i：返回 p 前面第 i 个元素的迭代器。
- `p[i]`：返回 p 后面第 i 个元素的引用。

此外，两个随机访问迭代器 p1、p2 还可以用 `<、>、<=、>=` 运算符进行比较。另外，表达式 `p2-p1` 也是有定义的，其返回值表示 p2 所指向元素和 p1 所指向元素的序号之差（也可以说是 p2 和 p1 之间的元素个数减一）。

分类

- 随机访问迭代器: `array, vector, deque`
- 双向迭代: `list, set/multiset, map/multimap,`
- 前向迭代器: `forward_list, unordered_map/unodered_multimap, unordered_set/unordered_umltiset,`
- 不支持迭代器: `stack, queue`

##### 遍历迭代器

```cpp
//遍历 vector 容器。
    vector<int> v{1,2,3,4,5,6,7,8,9,10}; //v被初始化成有10个元素
    
    cout << "第一种遍历方法：" << endl;
    //size返回元素个数
    for (int i = 0; i < v.size(); ++i)
        cout << v[i] <<" "; //像普通数组一样使用vector容器
    //创建一个正向迭代器，当然，vector也支持其他 3 种定义迭代器的方式
    
    cout << endl << "第二种遍历方法：" << endl;
    vector<int>::iterator i;
    //用 != 比较两个迭代器
    for (i = v.begin(); i != v.end(); ++i)
        cout << *i << " ";
    
    cout << endl << "第三种遍历方法：" << endl;
    for (i = v.begin(); i < v.end(); ++i) //用 < 比较两个迭代器
        cout << *i << " ";
   
    cout << endl << "第四种遍历方法：" << endl;
    i = v.begin();
    while (i < v.end()) { //间隔一个输出
        cout << *i << " ";
        i += 2; // 随机访问迭代器支持 "+= 整数"  的操作
    }
```

#### C++序列式容器（STL序列式容器）

- [biancheng](http://c.biancheng.net/view/409.html)

所谓序列容器，即以线性排列（类似普通数组的存储方式）来存储某一指定类型（例如 int、double 等）的数据，需要特殊说明的是，该类容器并不会自动对存储的元素按照值的大小进行排序。

- `array<T,N>`（**数组容器**）：表示可以存储 N 个 T 类型的元素，是 C++ 本身提供的一种容器。此类容器一旦建立，其长度就是固定不变的，这意味着不能增加或删除元素，只能改变某个元素的值；
- `vector<T>`（**向量容器**）：用来存放 T 类型的元素，是一个长度可变的序列容器，即在存储空间不足时，会自动申请更多的内存。使用此容器，在尾部增加或删除元素的效率最高（时间复杂度为 O(1) 常数阶），在其它位置插入或删除元素效率较差（时间复杂度为 O(n) 线性阶，其中 n 为容器中元素的个数）；
- `deque<T>`（**双端队列容器**）：和 vector 非常相似，区别在于使用该容器不仅尾部插入和删除元素高效，在头部插入或删除元素也同样高效，时间复杂度都是 O(1) 常数阶，但是在容器中某一位置处插入或删除元素，时间复杂度为 O(n) 线性阶；
- `list<T>`（**链表容器**）：是一个长度可变的、由 T 类型元素组成的序列，它以双向链表的形式组织元素，在这个序列的任何地方都可以高效地增加或删除元素（时间复杂度都为常数阶 O(1)），但访问容器中任意元素的速度要比前三种容器慢，这是因为 list<T> 必须从第一个元素或最后一个元素开始访问，需要沿着链表移动，直到到达想要的元素。
- `forward_list<T>`（**正向链表容器**）：和 list 容器非常类似，只不过它以单链表的形式组织元素，它内部的元素只能从第一个元素开始访问，是一类比链表容器快、更节省内存的容器。

#### array

- `begin()` 返回指向容器中第一个元素的随机访问迭代器。
- `end()` 返回指向容器**最后一个元素之后一个位置**的随机访问迭代器，通常和 begin() 结合使用。
- `rbegin()` 返回指向最后一个元素的随机访问迭代器。
- rend() 返回指向第一个元素之前一个位置的随机访问迭代器。
- `size()` 返回容器中当前元素的数量，其值始终等于初始化 array 类的第二个模板参数 N。
- `max_size()` 返回容器可容纳元素的最大数量，其值始终等于初始化 array 类的第二个模板参数 N。
- empty() 判断容器是否为空，和通过 size()==0 的判断条件功能相同，但其效率可能更快。
- `at(n)` **返回容器中 n 位置处元素的引用**，该函数自动检查 n 是否在有效的范围内，如果不是则抛出 out_of_range 异常。
- `front()` 返回容器中第一个元素的直接引用，该函数不适用于空的 array 容器。
- `back()` 返回容器中最后一个元素的直接应用，该函数同样不适用于空的 array 容器。
- data() 返回一个指向容器首个元素的指针。利用该指针，可实现复制容器中所有元素等类似功能。
- `fill(val)` 将 val 这个值赋值给容器中的每个元素。
- `array1.swap(array2)` 交换 array1 和 array2 容器中的所有元素，但前提是它们具有相同的长度和类型。

```cpp
std::array<double, 10> values;      // 未初始化
std::array<double, 10> values {};   // 初始化为 0.0
std::array<double, 10> values {0.5,1.0,1.5,,2.0}; // 部分初始化 (其他为 0.0)

// 方法
    std::array<int, 4> values{};
    //初始化 values 容器为 {0,1,2,3}
    for (int i = 0; i < values.size(); i++) {
        values.at(i) = i;
    }
    //使用 get() 重载函数输出指定位置元素
    cout << get<3>(values) << endl;
    //如果容器不为空，则输出容器中所有的元素
    if (!values.empty()) {
        for (auto val = values.begin(); val < values.end(); val++) {
            cout << *val << " ";
        }
    }
```



#### vector

```cpp
std::vector<double> values;     // 空
values.reserve(20);             // 分配 capacity
std::vector<int> primes {2, 3, 5, 7, 11, 13, 17, 19};
std::vector<double> values(20);         // 指定开始时元素数量, 都是默认值 0.0
std::vector<double> values(20, 1.0);    // 指定初始值为 1.0
// 区别于 array, 可以采用变量进行初始化
int num=20;
double value =1.0;
std::vector<double> values(num, value);
```

除了array中的 `begin, end` 等, 方法包括

- size() 返回实际元素个数。
- max_size() 返回元素个数的最大值。这通常是一个很大的值，一般是 232-1，所以我们很少会用到这个函数。
- resize() 改变实际元素的个数。
- capacity() 返回当前容量。
- empty() 判断容器中是否有元素，若无元素，则返回 true；反之，返回 false。
- reserve() 增加容器的容量。
- shrink _to_fit() 将内存减少到等于当前元素实际所使用的大小。
- operator[ ] 重载了 [ ] 运算符，可以向访问数组中元素那样，通过下标即可访问甚至修改 vector 容器中的元素。
- at() 使用经过边界检查的索引访问元素。
- front() 返回第一个元素的引用。
- back() 返回最后一个元素的引用。
- data() 返回指向容器中第一个元素的指针。
- assign() 用新元素替换原有内容。
- `push_back()` 在序列的尾部添加一个元素。
- `pop_back()` 移出序列尾部的元素。
- `insert()` 在指定的位置插入一个或多个元素。
- erase() 移出一个元素或一段元素。
- clear() 移出所有的元素，容器大小变为 0。
- `swap()` 交换两个容器的所有元素。
- emplace() 在指定的位置直接生成一个元素。
- `emplace_back()` 在序列尾部生成一个元素。

```cpp
    //初始化一个空vector容量
    vector<char>value;
    //向value容器中的尾部依次添加 S、T、L 字符
    value.push_back('S');
    value.push_back('T');
    value.push_back('L');
    //调用 size() 成员函数容器中的元素个数
    printf("元素个数为：%d\n", value.size());
    //使用迭代器遍历容器
    for (auto i = value.begin(); i < value.end(); i++) {
        cout << *i << " ";
    }
    cout << endl;
    //向容器开头插入字符
    value.insert(value.begin(), 'C');
    cout << "首个元素为：" << value.at(0) << endl;
```

##### vector添加元素（push_back()和emplace_back()）

`emplace_back()` 和 `push_back()` 的区别，就在于底层实现的机制不同。push_back() 向容器尾部添加元素时，首先会创建这个元素，然后再将这个元素拷贝或者移动到容器中（如果是拷贝的话，事后会自行销毁先前创建的这个元素）；而 emplace_back() 在实现时，则是直接在容器尾部创建这个元素，省去了拷贝或移动元素的过程。

参见 [here](http://c.biancheng.net/view/6826.html) 例子


### STL关联式容器

也就是说，使用关联式容器存储的元素，都是一个一个的“键值对”（ `<key,value>` ），这是和序列式容器最大的不同。除此之外，序列式容器中存储的元素默认都是未经过排序的，而使用关联式容器存储的元素，默认会根据各元素的键值的大小做升序排序。

底层是 **红黑树**. (C++ 11 还新增了 4 种哈希容器，即 unordered_map、unordered_multimap 以及 unordered_set、unordered_multiset。严格来说，它们也属于关联式容器，但由于哈希容器底层采用的是哈希表，而不是红黑树)

- `map` 定义在 <map> 头文件中，使用该容器存储的数据，其各个元素的键必须是唯一的（即不能重复），该容器会根据各元素键的大小，默认进行升序排序（调用 std::less<T>）。
- `set` 定义在 <set> 头文件中，使用该容器存储的数据，各个元素键和值完全相同，且各个元素的值不能重复（保证了各元素键的唯一性）。该容器会自动根据各个元素的键（其实也就是元素值）的大小进行升序排序（调用 std::less<T>）。
- `multimap` 定义在 <map> 头文件中，和 map 容器唯一的不同在于，multimap 容器中存储元素的键可以重复。
- `multiset` 定义在 <set> 头文件中，和 set 容器唯一的不同在于，multiset 容器中存储元素的值可以重复（一旦值重复，则意味着键也是重复的）。

#### pair 类模板

考虑到“键值对”并不是普通类型数据，C++ STL 标准库提供了 pair 类模板，其专门用来将 2 个普通元素 first 和 second（可以是 C++ 基本数据类型、结构体、类自定的类型）创建成一个新元素 `<first, second>`。

- 注意，pair 类模板定义在`<utility>`头文件中

```cpp
// 1) 默认构造函数，即创建空的 pair 对象
pair();
// 2) 直接使用 2 个元素初始化成 pair 对象
pair (const first_type& a, const second_type& b);
// 3) 拷贝（复制）构造函数，即借助另一个 pair 对象，创建新的 pair 对象
template<class U, class V> pair (const pair<U,V>& pr);

// 在 C++ 11 标准中，在引入右值引用的基础上，pair 类模板中又增添了如下 2 个构造函数
// 4) 移动构造函数
template<class U, class V> pair (pair<U,V>&& pr);
// 5) 使用右值引用参数，创建 pair 对象
template<class U, class V> pair (U&& a, V&& b);
```

e.g. 几种创建 pair 对象的方法

```cpp
    // 调用构造函数 1，也就是默认构造函数
    pair <string, double> pair1;
    // 调用第 2 种构造函数
    pair <string, string> pair2("STL教程","http://c.biancheng.net/stl/");  
    // 调用拷贝构造函数
    pair <string, string> pair3(pair2);
    //调用移动构造函数
    pair <string, string> pair4(make_pair("C++教程", "http://c.biancheng.net/cplus/"));
    // 调用第 5 种构造函数
    pair <string, string> pair5(string("Python教程"), string("http://c.biancheng.net/python/"));  
   
    cout << "pair1: " << pair1.first << " " << pair1.second << endl;
    // ...
```

- `<utility>`头文件中除了提供创建 pair 对象的方法之外，还为 pair 对象重载了 `<、<=、>、>=、==、!=` 这 6 的运算符，其运算规则是：对于进行比较的 2 个 pair 对象，先比较 pair.first 元素的大小，如果相等则继续比较 pair.second 元素的大小。










### STL无序关联式容器





## topics

### .h .cpp 文件

- [理解头文件(.h)和源文件(.cpp)](https://blog.csdn.net/John_xyz/article/details/82924597)

下面两种 include 方法分别: 1) 编译器会在系统文件目录下查找; 2) 编译器首先在用户目录下查找，然后在C++安装目录中查找，最后在系统文件中查找

```cpp
#include <>
#include ""
```

#### 头文件 (.h)

- 写类的声明（包括类里面的成员和方法的声明）、函数原型、#define 常数等，但一般来说不写出类的具体实现。
- 在写头文件时需要注意，开头和结尾必须按照如下样式加上预编译语句

```cpp
#ifndef CIRCLE_H
#define CIRCLE_H
// your code
#endif
```

### struct, class

[C和C++中struct](https://github.com/Light-City/CPlusPlusThings/tree/master/basic_content/struct)

struct 作为数据结构的实现体，它默认的数据访问控制是 public 的，而 class 作为对象的实现体，它默认的成员变量访问控制是 private 的。

#### struct

在cpp中, struct

- 能将函数放在结构体声明
- public、protected、private 在C++中可以使用。
- 使用结构体, 可以不加struct (而在C中一定要)
- 可以继承 (C中没有这一概念)
- 若结构体的名字与函数名相同，使用结构体，只能使用带struct定义 (而在C中可以直接调用)

```cpp
#include<iostream>
#include<stdio.h>
struct Base {         
    int v1;
//    private:   //error!
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
    return 0;
}
```

### extern "C"

C++ 调用 C 函数

```cpp
//xx.h
extern int add(...)

//xx.c
int add(){
    
}

//xx.cpp
extern "C" {
    #include "xx.h"
}
```

C 调用 C++ 函数

```c
//xx.h
extern "C"{
    int add();
}
//xx.cpp
int add(){
    
}
// 或者直接写成下面的形式
extern "C" string f(){}

//xx.c
extern int add();
```

### freopen 重定向 标准输入输出

```cpp
// <stdio.h>
FILE *freopen( const char *path, const char *mode, FILE *stream ); 
// 实现重定向，把预定义的标准流文件定向到由path指定的文件中。标准流文件具体是指stdin、stdout和stderr。其
```

e.g.

```cpp
#include <stdio.h>
#include <iostream>
int main()
{ 
    int a,b; 
    freopen("D:\\in.txt","r",stdin);    //输入重定向，输入数据将从D盘根目录下的in.txt文件中读取 
    freopen("D:\\out.txt","w",stdout); //输出重定向，输出数据将保存在D盘根目录下的out.txt文件中 
    while(cin>>a>>b) 
    cout<<a+b<<endl;    // 注意使用endl 
    // C 语法
    // while(scanf("%d %d",&a,&b)!=EOF) 
    // printf("%d\n",a+b);
    fclose(stdin);      //关闭重定向输入
    fclose(stdout);     //关闭重定向输出 
    return 0; 
}
```

### C++11右值引用

see [here](http://c.biancheng.net/view/439.html)

```cpp
class A{};
A & rl = A();  //错误，无名临时变量 A() 是右值，因此不能初始化左值引用 r1
A && r2 = A();  //正确，因 r2 是右值引用
```
