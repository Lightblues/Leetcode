## basic

### 基本结构

从功能和实现上说，`Go`的`map`类似于`Java`语言中的`HashMap`，Python语言中的`dict`，`Lua`语言中的`table`，通常使用`hash`实现。遗憾的是，对于该词的翻译并不统一，数学界术语为`映射`，而计算机界众说纷纭莫衷一是。

### 基本包

```go
// fmt 包
fmt.Printf("%d\t%s\n", n, line)
fmt.Fprintf(os.Stderr, "dup2: %v\n", err)   // 输出到stderr

// os 包
// 命令行参数
os.Args[1:]
// 文件读写
f, err := os.Open(fn)
f.close()

// io/ioutil 包
data, err := ioutil.ReadFile(filename)

// strings 包
strings.Join(os.Args[1:], " ")

// bufio 包
input := bufio.NewScanner(os.Stdin)
for input.Scan() {
    counts[input.Text()]++
}

```

### 格式化输出

```sh
%d          十进制整数
%x, %o, %b  十六进制，八进制，二进制整数。
%f, %g, %e  浮点数： 3.141593 3.141592653589793 3.141593e+00
%t          布尔：true或false
%c          字符（rune） (Unicode码点)
%s          字符串
%q          带双引号的字符串"abc"或带单引号的字符'c'
%v          变量的自然形式（natural format）
%T          变量的类型
%%          字面上的百分号标志（无操作数）
```


### 常用功能

文件读写

```go
import (
    "fos"
    "io/ioutil"
)
// 方式1: 以基本的os包, 采取流的形式读取
    counts := make(map[string]int)
    // 下面两种都可以
    f := os.Stdin
    f, err := os.Open(arg)
    if err != nil {
        fmt.Fprintf(os.Stderr, "dup2: %v\n", err)
        continue
    }
    countLines(f, counts)
    f.Close()

// 方式1: 采用 io/ioutil 包读取. 直接将文件内容读入内存
    data, err := ioutil.ReadFile(filename)
    if err != nil {
        fmt.Fprintf(os.Stderr, "dup3: %v\n", err)
        continue
    }
    // 注意结果是 byte slice, 需要转为 string
    strings.Split(string(data), "\n")

// 处理函数
func countLines(f *os.File, counts map[string]int) {
    input := bufio.NewScanner(f)
    for input.Scan() {
        counts[input.Text()]++
    }
    // NOTE: ignoring potential errors from input.Err()
}
```

获取html

```go
import {
    "net/http"
}
    resp, err := http.Get(url)
    if err != nil {
        fmt.Fprintf(os.Stderr, "fetch: %v\n", err)
        os.Exit(1)
    }
    b, err := ioutil.ReadAll(resp.Body)
    // 关闭resp的Body流，防止资源泄露
    resp.Body.Close()
    if err != nil {
        fmt.Fprintf(os.Stderr, "fetch: reading %s: %v\n", url, err)
        os.Exit(1)
    }
    fmt.Printf("%s", b)
```

### 关键字表

Go语言中类似if和switch的关键字有25个；关键字不能用于自定义名字，只能在特定语法结构中使用

```sh
break      default       func     interface   select
case       defer         go       map         struct
chan       else          goto     package     switch
const      fallthrough   if       range       type
continue   for           import   return      var
```

此外，还有大约30多个预定义的名字，比如int和true等，主要对应内建的常量、类型和函数。

```go
内建常量: true false iota nil

内建类型: int int8 int16 int32 int64
          uint uint8 uint16 uint32 uint64 uintptr
          float32 float64 complex128 complex64
          bool byte rune string error

内建函数: make len cap new append copy close delete
          complex real imag
          panic recover
```




### 应用例子

- 通过 math, math/rand 库生成 Lissajous figures, 然后用 image, image/color, image/gif 制作成gif图片.
- 通过 net/http 库获取html页面.
- 并发编程: 简单介绍 goroutine和channel
- go作为server


## 程序结构

### 命名

如果一个名字是在函数内部定义，那么它的就只在函数内部有效。如果是在函数外部定义，那么将在当前包的所有文件中都可以访问。名字的开头字母的大小写决定了名字在包外的可见性。如果一个名字是大写字母开头的（译注：必须是在函数外部定义的包级名字；包级函数名本身也是包级名字），那么它将是导出的，也就是说可以被外部的包访问，例如fmt包的Printf函数就是导出的，可以在fmt包外部访问。包本身的名字一般总是用小写字母。

### 声明

声明语句定义了程序的各种实体对象以及部分或全部的属性。Go语言主要有四种类型的声明语句：var、const、type和func，分别对应变量、常量、类型和函数实体对象的声明。


### 变量

var声明语句可以创建一个特定类型的变量，然后给变量附加一个名字，并且设置变量的初始值。变量声明的一般语法如下：

```go
var 变量名字 类型 = 表达式
```


其中“类型”或“= 表达式”两个部分可以省略其中的一个。如果省略的是类型信息，那么将根据初始化表达式来推导变量的类型信息。如果初始化表达式被省略，那么将用零值初始化该变量。 数值类型变量对应的零值是0，布尔类型变量对应的零值是false，字符串类型对应的零值是空字符串，**接口或引用类型**（包括slice、map、chan和函数）变量对应的零值是nil。数组或结构体等聚合类型对应的零值是每个元素或字段都是对应该类型的零值。

### 赋值

```go
x = 1                       // 命名变量的赋值
*p = true                   // 通过指针间接赋值
person.name = "bob"         // 结构体字段赋值
count[x] = count[x] * scale // 数组、slice或map的元素赋值
```

### 类型 type


变量或表达式的类型定义了对应存储值的属性特征，例如数值在内存的存储大小（或者是元素的bit个数），它们在内部是如何表达的，是否支持一些操作符，以及它们自己关联的方法集等。

```go
type 类型名字 底层类型
```

- keyword: 命名类型; 方法
- 定义类型的作用
    - 区分不同含义的变量, 即使底层数据类型相同, 不同类型的变量之间也无法操作. (例如定义了 `Celsius, Fahrenheit` 两种温度单位).
- 但对于所定义的类型, 其可以和底层类型之间进行比较
    - 例如, Celsius 底层是 float64, 两者可以加减比较
    - 「底层数据类型决定了内部结构和表达方式，也决定是否可以像底层类型一样对内置运算符的支持」

对于每一个类型T，都有一个对应的 **类型转换操作** T(x)，用于将x转为T类型（译注：如果T是指针类型，可能会需要用小括弧包装T，比如`(*int)(0)`）。只有当两个类型的底层基础类型相同时，才允许这种转型操作，或者是两者都是指向相同底层结构的指针类型，这些转换只改变类型而不会影响值本身。

数值类型之间的转型也是允许的，并且在字符串和一些特定类型的slice之间也是可以转换的，在下一章我们会看到这样的例子。这类转换可能改变值的表现。例如，将一个浮点数转为整数将丢弃小数部分，将一个字符串转为`[]byte`类型的slice将拷贝一个字符串数据的副本。在任何情况下，运行时不会发生转换失败的错误（译注: 错误只会发生在编译阶段）。


### 包和文件

- 本地包导入: [here](https://zhuanlan.zhihu.com/p/109828249)

Go语言中的包和其他语言的库或模块的概念类似，目的都是为了支持模块化、封装、单独编译和代码重用。一个包的源代码保存在一个或多个以.go为文件后缀名的源文件中，通常一个包所在目录路径的后缀是包的导入路径；例如包gopl.io/ch1/helloworld对应的目录路径是$GOPATH/src/gopl.io/ch1/helloworld。

### 作用域

- keywords: 作用域; 生命周期;


一个声明语句将程序中的实体和一个名字关联，比如一个函数或一个变量。**声明语句的作用域** 是指源代码中可以有效使用这个名字的范围。
不要将作用域和生命周期混为一谈。声明语句的作用域对应的是一个源代码的文本区域；它是一个编译时的属性。**一个变量的生命周期** 是指程序运行时变量存在的有效时间段，在此时间区域内它可以被程序的其他部分引用；是一个运行时的概念。

声明语句对应的词法域决定了作用域范围的大小。对于内置的类型、函数和常量，比如int、len和true等是在全局作用域的，因此可以在整个程序中直接使用。任何在在函数外部（也就是包级语法域）声明的名字可以在同一个包的任何源文件中访问的。对于导入的包，例如tempconv导入的fmt包，则是对应源文件级的作用域，因此只能在当前的文件中访问导入的fmt包，当前包的其它源文件无法访问在当前源文件导入的包。还有许多声明语句，比如tempconv.CToF函数中的变量c，则是局部作用域的，它只能在函数内部（甚至只能是局部的某些部分）访问。

不同的作用域

- 函数体词法域
- for, if, switch 等隐式的初始化词法域

```go
// 下面的例子同样有三个不同的x变量，每个声明在不同的词法域，一个在函数体词法域，一个在for隐式的初始化词法域，一个在for循环体词法域；只有两个块是显式创建的：
func main() {
    // 函数体词法域
    x := "hello"
    // for隐式的初始化词法域
    for _, x := range x {
        // for循环体词法域
        x := x + 'A' - 'a'
        fmt.Printf("%c", x) // "HELLO" (one letter per iteration)
    }
}
```

再来看一个if的例子:

```go
if x := f(); x == 0 {
    fmt.Println(x)
// 第二个if语句嵌套在第一个内部，因此第一个if语句条件初始化词法域声明的变量在第二个if中也可以访问
} else if y := g(x); x == y {
    fmt.Println(x, y)
} else {
    fmt.Println(x, y)
}
fmt.Println(x, y) // compile error: x and y are not visible here
```

例子: 处理函数回传错误的时候, 下面的两个变量在if语句的隐式作用域中, 注意若在if语句之外使用会报错.

```go
if f, err := os.Open(fname); err != nil {
    return err
} else {
    // f and err are visible here too
    f.ReadByte()
    f.Close()
}

// f.ReadByte() // compile error: undefined f
```

## 基础数据类型

虽然从底层而言，所有的数据都是由比特组成，但计算机一般操作的是固定大小的数，如整数、浮点数、比特数组、内存地址等。进一步将这些数组织在一起，就可表达更多的对象，例如数据包、像素点、诗歌，甚至其他任何对象。Go语言提供了丰富的数据组织形式，这依赖于Go语言内置的数据类型。这些内置的数据类型，兼顾了硬件的特性和表达复杂数据结构的便捷性。

Go语言将数据类型分为四类：基础类型、复合类型、引用类型和接口类型。本章介绍基础类型，包括：数字、字符串和布尔型。复合数据类型——数组（§4.1）和结构体（§4.2）——是通过组合简单类型，来表达更加复杂的数据结构。引用类型包括指针（§2.3.2）、切片（§4.2)）字典（§4.3）、函数（§5）、通道（§8），虽然数据种类很多，但它们都是对程序中一个变量或状态的间接引用。这意味着对任一引用类型数据的修改都会影响所有该引用的拷贝。我们将在第7章介绍接口类型。


### 常量

常量表达式的值在编译期计算，而不是在运行期。每种常量的潜在类型都是基础类型：boolean、string或数字。

所有常量的运算都可以在编译期完成，这样可以减少运行时的工作，也方便其他编译优化。当操作数是常量时，一些运行时的错误也可以在编译时被发现，例如整数除零、字符串索引越界、任何导致无效浮点数的操作等。

**常量间的所有算术运算、逻辑运算和比较运算的结果也是常量**，对常量的类型转换操作或以下函数调用都是返回常量结果：len、cap、real、imag、complex和unsafe.Sizeof（§13.1）。

- 常量的作用
    - 例如可以定义指定长度的数组

```go
const IPv4Len = 4

// parseIPv4 parses an IPv4 address (d.d.d.d).
func parseIPv4(s string) IP {
    var p [IPv4Len]byte
    // ...
}
```


## 复合数据类型

- 四种类型: **数组、slice、map和结构体**
- 数组和结构体是聚合类型；它们的值由许多元素或成员字段的值组成。数组是由同构的元素组成——每个数组元素都是完全相同的类型——结构体则是由异构的元素组成的。数组和结构体都是有固定内存大小的数据结构。相比之下，slice和map则是动态的数据结构，它们将根据需要动态增长。

### 数组

数组是一个由固定长度的特定类型元素组成的序列，一个数组可以由零个或多个元素组成。因为数组的长度是固定的，因此在Go语言中很少直接使用数组。和数组对应的类型是Slice（切片），它是可以增长和收缩动态序列，slice功能也更灵活，但是要理解slice工作原理的话需要先理解数组。

```go
var q [3]int = [3]int{1, 2, 3}
q := [...]int{1, 2, 3}          // 推断长度

var r [3]int = [3]int{1, 2}     // 默认初始化为零值
fmt.Println(r[2]) // "0"
```

除了顺序初始化, 还可以根据idx位置指定对应位置的值, 其他部分还是零值

```go
// 例子1
type Currency int
// 用 iota 来定义一些常量
const (
USD Currency = iota // 美元
EUR                 // 欧元
GBP                 // 英镑
RMB                 // 人民币
)
// 按照 idx:value 的形式初始化数组
symbol := [...]string{EUR: "€", GBP: "￡", RMB: "￥", USD: "$"}
fmt.Println(RMB, symbol[RMB]) // "3 ￥"

// 例子2
r := [...]int{99: -1}
```

数组的比较: 只有当长度相同并且底层类型可比较的时候才行. 下面的例子比较两slice类型数据的消息摘要. (注意, 其中的 %x副词参数，它用于指定以十六进制的格式打印数组或slice全部的元素，%t副词参数是用于打印布尔型数据，%T副词参数是用于显示一个值对应的数据类型)

```go
import "crypto/sha256"

func main() {
    c1 := sha256.Sum256([]byte("x"))
    c2 := sha256.Sum256([]byte("X"))
    fmt.Printf("%x\n%x\n%t\n%T\n", c1, c2, c1 == c2, c1)
    // Output:
    // 2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881
    // 4b68ab3847feda7d6c62c1fbcbeebfa35eab7351ed5e78f4ddadea5df64b8015
    // false
    // [32]uint8
}
```

### 函数接受的是副本

当调用一个函数的时候，函数的每个调用参数将会被赋值给函数内部的参数变量，所以函数参数变量接收的是一个复制的副本，并不是原始调用的变量。因为函数参数传递的机制导致传递大的数组类型将是低效的，并且对数组参数的任何的修改都是发生在复制的数组上，并不能直接修改调用时原始的数组变量。在这个方面，Go语言对待数组的方式和其它很多编程语言不同，其它编程语言可能会隐式地将数组作为引用或指针对象传入被调用的函数。

- 如果想要传入数组还要进行修改, 可以用 **指针**.

```go
// 将传入的数组修改为全零
func zero(ptr *[32]byte) {
    // 方式一
    for i := range ptr {
        ptr[i] = 0
    }
    // 方式二. 因为 `[32]byte{}` 数组字面值初始化都是零值.
    *ptr = [32]byte{}
}
```

> 虽然通过指针来传递数组参数是高效的，而且也允许在函数内部修改数组的值，但是数组依然是僵化的类型，因为数组的类型包含了僵化的长度信息。上面的zero函数并不能接收指向[16]byte类型数组的指针，而且也没有任何添加或删除数组元素的方法。由于这些原因，除了像SHA256这类需要处理特定大小数组的特例外，数组依然很少用作函数参数；相反，我们一般使用slice来替代数组。



## 函数


## 方法/OOP

### 方法声明

- 声明语法: `func (p Point) Distance(q Point) float64 {}`
    - 接收器(receiver): 附加的参数p
- 调用形式: `p.Distance`
    - 选择器: 选择合适的对应p这个对象的Distance方法来执行

```go
// 方法比较一般定义的函数
type Point struct{ X, Y float64 }

// traditional function
func Distance(p, q Point) float64 {
    return math.Hypot(q.X-p.X, q.Y-p.Y)
}

// same thing, but as a method of the Point type
func (p Point) Distance(q Point) float64 {
    return math.Hypot(q.X-p.X, q.Y-p.Y)
```

可以通过实例 `.` 方法进行调用, 也可以像一般的函数那样进行调用 (需要传入作用的对象). 可以看到通过 `.`  方法进行调用更为简洁.

```go
perim := geometry.Path{{1, 1}, {5, 1}, {5, 4}, {1, 1}}
fmt.Println(geometry.Path.Distance(perim)) // "12", standalone function
fmt.Println(perim.Distance())             // "12", method of geometry.Path
```

