- 《[Go语言圣经](https://yar999.gitbook.io/gopl-zh/)》
    - [The Go Programming Language](http://www.gopl.io/)
    - code: <https://github.com/adonovan/gopl.io/>

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

Go语言将数据类型分为四类：**基础类型、复合类型、引用类型和接口类型**。本章介绍 **基础类型**，包括：数字、字符串和布尔型。**复合数据类型** ——数组（§4.1）和结构体（§4.2）——是通过组合简单类型，来表达更加复杂的数据结构。**引用类型** 包括指针（§2.3.2）、切片（§4.2)）字典（§4.3）、函数（§5）、通道（§8），虽然数据种类很多，但它们都是对程序中一个变量或状态的间接引用。这意味着对任一引用类型数据的修改都会影响所有该引用的拷贝。我们将在第7章介绍接口类型。


### 整型

Go语言同时提供了有符号和无符号类型的整数运算。这里有int8、int16、int32和int64四种截然不同大小的有符号整形数类型，分别对应8、16、32、64bit大小的有符号整形数，与此对应的是uint8、uint16、uint32和uint64四种无符号整形数类型。

这里还有两种一般对应特定CPU平台机器字大小的有符号和无符号整数 `int` 和 `uint`；其中int是应用最广泛的数值类型。这两种类型都有同样的大小，32或64bit，但是我们不能对此做任何的假设；因为不同的编译器即使在相同的硬件平台上可能产生不同的大小。

**Unicode字符 `rune` 类型是和int32等价的类型，通常用于表示一个Unicode码点**。这两个名称可以互换使用。**同样 `byte` 也是uint8类型的等价类型**，byte类型一般用于强调数值是一个原始的数据而不是一个小的整数。

最后，还有一种无符号的整数类型uintptr，没有指定具体的bit大小但是足以容纳指针。uintptr类型只有在底层编程是才需要，特别是Go语言和C语言函数库或操作系统接口相交互的地方。我们将在第十三章的unsafe包相关部分看到类似的例子。

不管它们的具体大小，`int`、`uint` 和 `uintptr` 是不同类型的兄弟类型。其中int和int32也是不同的类型，即使int的大小也是32bit，**在需要将int当作int32类型的地方需要一个显式的类型转换操作**，反之亦然。

其中有符号整数采用2的补码形式表示，也就是最高bit位用作表示符号位，一个n-bit的有符号数的值域是从 $-2^{n-1}$ 到 $2^{n-1}-1$ 。无符号整数的所有bit位都用于表示非负数，值域是0到 $2^n-1$。例如，int8类型整数的值域是从-128到127，而uint8类型整数的值域是从0到255。

#### 运算符 优先级

按照优先级排序

```go
*      /      %      <<       >>     &       &^
+      -      |      ^
==     !=     <      <=       >      >=
&&
||
```

算术运算符+、-、`*`和`/`可以适用与于整数、浮点数和复数，但是取模运算符%仅用于整数间的运算。对于不同编程语言，%取模运算的行为可能并不相同。在Go语言中，%取模运算符的符号和被取模数的符号总是一致的，因此`-5%3`和`-5%-3`结果都是-2。除法运算符`/`的行为则依赖于操作数是否为全为整数，比如`5.0/4.0`的结果是1.25，但是5/4的结果是1，因为整数除法会向着0方向截断余数。

如果一个算术运算的结果，不管是有符号或者是无符号的，如果需要更多的bit位才能正确表示的话，就说明计算结果是溢出了。超出的高位的bit位部分将被丢弃。如果原始的数值是有符号类型，而且最左边的bit为是1的话，那么最终结果可能是负的

```go
// 计算溢出
var u uint8 = 255
fmt.Println(u, u+1, u*u) // "255 0 1"

var i int8 = 127
fmt.Println(i, i+1, i*i) // "127 -128 1"
```

#### 位运算

Go语言还提供了以下的bit位操作运算符，前面4个操作运算符并不区分是有符号还是无符号数

```go
&      位运算 AND
|      位运算 OR
^      位运算 XOR
&^     位清空 (AND NOT)
<<     左移
>>     右移
```

位操作运算符`^`作为二元运算符时是按位异或（XOR），当用作一元运算符时表示按位取反；也就是说，它返回一个每个bit位都取反的数。位操作运算符`&^`用于按位置零（AND NOT）：表达式`z = x &^ y`结果z的bit位为0，如果对应y中bit位为1的话，否则对应的bit位等于x相应的bit位的值。 (其实就是先对y取反, 然后再AND x. 下面例子中, 用集合的角度来看的话, 就是 difference)

```go
// 位运算: 集合视角
var x uint8 = 1<<1 | 1<<5
var y uint8 = 1<<1 | 1<<2

fmt.Printf("%08b\n", x) // "00100010", the set {1, 5}
fmt.Printf("%08b\n", y) // "00000110", the set {1, 2}

fmt.Printf("%08b\n", x&y)  // "00000010", the intersection {1}
fmt.Printf("%08b\n", x|y)  // "00100110", the union {1, 2, 5}
fmt.Printf("%08b\n", x^y)  // "00100100", the symmetric difference {2, 5}
fmt.Printf("%08b\n", x&^y) // "00100000", the difference {5}

for i := uint(0); i < 8; i++ {
    if x&(1<<i) != 0 { // membership test
        fmt.Println(i) // "1", "5"
    }
}

fmt.Printf("%08b\n", x<<1) // "01000100", the set {2, 6}
fmt.Printf("%08b\n", x>>1) // "00010001", the set {0, 4}
```

#### 数字: 十六进制

任何大小的整数字面值都可以用以0开始的八进制格式书写，例如0666；或用以0x或0X开头的十六进制格式书写，例如0xdeadbeef。十六进制数字可以用大写或小写字母。如今八进制数据通常用于POSIX操作系统上的文件访问权限标志，十六进制数字则更强调数字值的bit位模式。

当使用fmt包打印一个数值时，我们可以用%d、%o或%x参数控制输出的进制格式，就像下面的例子：

```go
o := 0666
fmt.Printf("%d %[1]o %#[1]o\n", o) // "438 666 0666"
x := int64(0xdeadbeef)
fmt.Printf("%d %[1]x %#[1]x %#[1]X\n", x)
// Output:
// 3735928559 deadbeef 0xdeadbeef 0XDEADBEEF
```


请注意fmt的两个使用技巧。通常Printf格式化字符串包含多个%参数时将会包含对应相同数量的额外操作数，但是%之后的 `[1]` 副词告诉Printf函数再次使用第一个操作数。第二，%后的 `#` 副词告诉Printf在用%o、%x或%X输出时生成0、0x或0X前缀。



#### 字符

字符面值通过一对单引号直接包含对应字符。最简单的例子是ASCII中类似'a'写法的字符面值，但是我们也可以通过转义的数值来表示任意的Unicode码点对应的字符，马上将会看到这样的例子。

字符使用 `%c` 参数打印，或者是用 `%q` 参数打印带单引号的字符

```go
ascii := 'a'
unicode := '国'
newline := '\n'
fmt.Printf("%d %[1]c %[1]q\n", ascii)   // "97 a 'a'"
fmt.Printf("%d %[1]c %[1]q\n", unicode) // "22269 国 '国'"
fmt.Printf("%d %[1]q\n", newline)       // "10 '\n'"
```




### 浮点数

Go语言提供了两种精度的浮点数，`float32` 和 `float64`。它们的算术规范由IEEE754浮点数国际标准定义，该浮点数规范被所有现代的CPU支持。

这些浮点数类型的取值范围可以从很微小到很巨大。浮点数的范围极限值可以在math包找到。常量math.MaxFloat32表示float32能表示的最大数值，大约是 3.4e38；对应的math.MaxFloat64常量大约是1.8e308。它们分别能表示的最小值近似为1.4e-45和4.9e-324。

一个float32类型的浮点数可以提供大约6个十进制数的精度，而float64则可以提供约15个十进制数的精度；通常应该优先使用float64类型，因为float32类型的累计计算误差很容易扩散，并且float32能精确表示的正整数并不是很大（译注：因为float32的有效bit位只有23个，其它的bit位用于指数和符号；当整数大于23bit能表达的范围时，float32的表示将出现误差）

```go
// float32 精度有限
var f float32 = 16777216 // 1 << 24
fmt.Println(f == f+1)    // "true"!
```

- 可以通过e或E来指定指数部分

用Printf函数的 `%g` 参数打印浮点数，将采用更紧凑的表示形式打印，并提供足够的精度，但是对应表格的数据，使用 `%e`（带指数）或 `%f` 的形式打印可能更合适。所有的这三个打印形式都可以指定打印的宽度和控制打印精度。

```go
// 很小或很大的数最好用科学计数法书写，通过e或E来指定指数部分
const Avogadro = 6.02214129e23  // 阿伏伽德罗常数
const Planck   = 6.62606957e-34 // 普朗克常数

// 通过 %f 控制输出
for x := 0; x < 8; x++ {
    fmt.Printf("x = %d e^x = %8.3f\n", x, math.Exp(float64(x)))
}
```

#### NaN 等特殊值

math包中除了提供大量常用的数学函数外，还提供了IEEE754浮点数标准中定义的特殊值的创建和测试：正无穷大和负无穷大 `+Inf, -Inf`，分别用于表示太大溢出的数字和除零的结果；还有NaN非数，一般用于表示无效的除法操作结果0/0或Sqrt(-1).

```go
var z float64
fmt.Println(z, -z, 1/z, -1/z, z/z) // "0 -0 +Inf -Inf NaN"
```

- NaN 无法直接比较

函数 `math.IsNaN` 用于测试一个数是否是非数NaN，`math.NaN` 则返回非数对应的值。虽然可以用math.NaN来表示一个非法的结果，但是测试一个结果是否是非数NaN则是充满风险的，因为NaN和任何数都是不相等的（译注：在浮点数中，NaN、正无穷大和负无穷大都不是唯一的，每个都有非常多种的bit模式表示）：

```go
nan := math.NaN()
fmt.Println(nan == nan, nan < nan, nan > nan) // "false false false"
```



### 复数

Go语言提供了两种精度的复数类型：complex64和complex128，分别对应float32和float64两种浮点数精度。内置的complex函数用于构建复数，内建的real和imag函数分别返回复数的实部和虚部

```go
var x complex128 = complex(1, 2) // 1+2i
var y complex128 = complex(3, 4) // 3+4i
fmt.Println(x*y)                 // "(-5+10i)"
fmt.Println(real(x*y))           // "-5"
fmt.Println(imag(x*y))           // "10"

// 数字加上一个 i 表示复数
fmt.Println(1i * 1i) // "(-1+0i)", i^2 = -1
x := 1 + 2i
y := 3 + 4i


// mat/cmplx 包
fmt.Println(cmplx.Sqrt(-1)) // "(0+1i)"
```



### 布尔型

一个布尔类型的值只有两种：true和false。if和for语句的条件部分都是布尔类型的值，并且==和<等比较操作也会产生布尔型的值。一元操作符`!`对应逻辑非操作，因此`!true`的值为`false`，更罗嗦的说法是`(!true==false)==true`，虽然表达方式不一样，不过我们一般会采用简洁的布尔表达式，就像用x来表示`x==true`。

布尔值可以和&&（AND）和||（OR）操作符结合，并且可能会有短路行为：如果运算符左边值已经可以确定整个布尔表达式的值，那么运算符右边的值将不在被求值

```go
// 利用短路结构确保安全
s != "" && s[0] == 'x'

// && 的优先级比 || 高
if 'a' <= c && c <= 'z' ||
    'A' <= c && c <= 'Z' ||
    '0' <= c && c <= '9' {
    // ...ASCII letter or digit...
}
```



### 字符串

一个字符串是一个不可改变的字节序列。字符串可以包含任意的数据，包括byte值0，但是通常是用来包含人类可读的文本。文本字符串通常被解释为采用UTF8编码的Unicode码点（rune）序列，我们稍后会详细讨论这个问题。

内置的len函数可以返回一个字符串中的字节数目（不是 rune 字符数目），索引操作 s[i] 返回第i个字节的字节值，i必须满足0 ≤ i< len(s)条件约束。

- 字符串可索引和切片
    - 如果索引超出字符串范围或者j小于i的话将导致panic异常

```go
s := "hello, world"
fmt.Println(len(s))      // "12"
fmt.Println(s[0], s[7])  // "104 119" ('h' and 'w')
// Printf 输出
fmt.Printf(s[:2] + "\n") // "he"
fmt.Printf("%c\n", s[2]) // "l"
```

- 字符串可比较 (==和<)
- `+` 操作
- 字符串不可变 (字符串变量可以更换绑定, 但是不会对于字符串中某一字符进行修改)

不变性意味如果两个字符串共享相同的底层数据的话也是安全的，这使得复制任何长度的字符串代价是低廉的。同样，一个字符串s和对应的子字符串切片s[7:]的操作也可以安全地共享相同的内存，因此字符串切片操作代价也是低廉的。在这两种情况下都没有必要分配新的内存。


### 常量

**常量表达式的值在编译期计算，而不是在运行期**。每种常量的潜在类型都是基础类型：boolean、string或数字。

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

#### 函数接受的是副本

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


### Slice 切片

Slice（切片）代表变长的序列，序列中每个元素都有相同的类型。一个slice类型一般写作 `[]T`，其中T代表slice中元素的类型；slice的语法和数组很像，只是没有固定长度而已。

数组和slice之间有着紧密的联系。一个slice是一个轻量级的数据结构，提供了访问数组子序列（或者全部）元素的功能，而且slice的底层确实引用一个数组对象。一个slice由三个部分构成： **指针、长度和容量** 。指针指向第一个slice元素对应的底层数组元素的地址，要注意的是slice的第一个元素并不一定就是数组的第一个元素。长度对应slice中元素的数目；长度不能超过容量，容量一般是从slice的开始位置到底层数据的结尾位置。内置的len和cap函数分别返回slice的长度和容量。

要注意的是slice类型的变量s和数组类型的变量a的初始化语法的差异。slice和数组的字面值语法很类似，它们都是用花括弧包含一系列的初始化元素，但是对于slice并没有指明序列的长度。这会隐式地创建一个合适大小的数组，然后slice的指针指向底层的数组。**就像数组字面值一样，slice的字面值也可以按顺序指定初始化值序列，或者是通过索引和元素值指定，或者的两种风格的混合语法初始化**。

#### make 创建 slice

```go
make([]T, len)      // 此时底层创建的数组长度等于len, 也即对于该slice, cap==len
make([]T, len, cap) // same as make([]T, cap)[:len]
// 也可以指定cap, 预留可能的增长.
```

在底层，make创建了一个匿名的数组变量，然后返回一个slice；只有通过返回的slice才能引用底层匿名的数组变量。在第一种语句中，slice是整个数组的view。在第二个语句中，slice只引用了底层数组的前len个元素，但是容量将包含整个的数组。额外的元素是留给未来的增长用的。


#### slice 比较

和数组不同的是，slice之间不能比较，因此我们不能使用==操作符来判断两个slice是否含有全部相等元素。不过标准库提供了高度优化的 `bytes.Equal` 函数来判断两个字节型slice是否相等（`[]byte`），但是对于其他类型的slice，我们必须自己展开每个元素进行比较

```Go
// 例如: 实现比较slice 
// 除了 []byte 之间的比较可以用 bytes.Equal 之外, 其他的slice需要手动实现比较
func equal(x, y []string) bool {
    if len(x) != len(y) {
        return false
    }
    for i := range x {
        if x[i] != y[i] {
            return false
        }
    }
    return true
}
```

> 为何slice不直接支持比较运算符呢？这方面有两个原因。第一个原因，一个slice的元素是间接引用的，一个slice甚至可以包含自身。虽然有很多办法处理这种情形，但是没有一个是简单有效的。
> 第二个原因，因为slice的元素是间接引用的，一个固定值的slice在不同的时间可能包含不同的元素，因为底层数组的元素可能会被修改。并且Go语言中map等哈希表之类的数据结构的key只做简单的浅拷贝，它要求在整个声明周期中相等的key必须对相同的元素。对于像指针或chan之类的引用类型，==相等测试可以判断两个是否是引用相同的对象。一个针对slice的浅相等测试的==操作符可能是有一定用处的，也能临时解决map类型的key问题，但是slice和数组不同的相等测试行为会让人困惑。因此，安全的做法是直接禁止slice之间的比较操作。


#### nil: slice支持和nil比较

!!! note
    nil 和长度容量为0的slice 非常类似. 但需要注意两者细微的差异.

**一个零值的slice等于nil**。一个nil值的slice并没有底层数组。一个nil值的slice的长度和容量都是0，但是也有非nil值的slice的长度和容量也是0的，例如 `[]int{}` 或 `make([]int, 3)[3:]`。与任意类型的nil值一样，我们可以用 `[]int(nil)` 类型转换表达式来生成一个对应类型slice的nil值。

```go
var s []int    // len(s) == 0, s == nil
s = nil        // len(s) == 0, s == nil
s = []int(nil) // len(s) == 0, s == nil
s = []int{}    // len(s) == 0, s != nil
```

如果你需要测试一个slice是否是空的，使用 `len(s) == 0` 来判断，而不应该用 `s == nil` 来判断。除了和nil相等比较外，一个nil值的slice的行为和其它任意0长度的slice一样；例如reverse(nil)也是安全的。除了文档已经明确说明的地方，所有的Go语言函数应该以相同的方式对待nil值的slice和0长度的slice。

### Map 哈希表

**哈希表** 是一种巧妙并且实用的数据结构。它是一个无序的key/value对的集合，其中所有的key都是不同的，然后通过给定的key可以在常数时间复杂度内检索、更新或删除对应的value。

在Go语言中，**一个 `map` 就是一个哈希表的引用**，map类型可以写为 `map[K]V`，其中K和V分别对应key和value。map中所有的key都有相同的类型，所有的value也有着相同的类型，但是key和value之间可以是不同的数据类型。其中K对应的key必须是支持 `==` 比较运算符的数据类型，所以map可以通过测试key是否相等来判断是否已经存在。虽然浮点数类型也是支持相等运算符比较的，但是将浮点数用做key类型则是一个坏的想法，正如第三章提到的，最坏的情况是可能出现的NaN和任何浮点数都不相等。对于V对应的value数据类型则没有任何的限制。

```go
ages := make(map[string]int) // mapping from strings to ints
// 初始化
ages := map[string]int{
    "alice":   31,
    "charlie": 34,
}
// 特殊: 创建空map
map[string]int{}
```

#### map 操作

- 所有这些操作是安全的，即使这些元素不在map中也没有关系；如果一个查找失败将返回value类型对应的零值
- map中的元素并不是一个变量，因此 **我们不能对map的元素进行取址操作**
    - 禁止对map元素取址的原因是map可能随着元素数量的增长而重新分配更大的内存空间，从而可能导致之前的地址无效。
- 要想遍历map中全部的key/value对的话，可以使用range风格的for循环实现，和之前的slice遍历语法类似

```GO
ages["alice"] = 32
fmt.Println(ages["alice"]) // "32"
// 删除
map[string]int{}

// 操作是安全的
ages["bob"] = ages["bob"] + 1 // happy birthday!
ages["bob"]++       // 等价

// 不合法
// _ = &ages["bob"] // compile error: cannot take address of map element

// 遍历
for name, age := range ages {
    fmt.Printf("%s\t%d\n", name, age)
}
```


#### 组合: 复合类型的 value

Map的value类型也可以是一个聚合类型，比如是一个map或slice。

- 技巧: 函数惰性初始化map

其中addEdge函数惰性初始化map是一个惯用方式，也就是说在每个值首次作为key时才初始化。addEdge函数显示了如何让map的零值也能正常工作；即使from到to的边不存在，`graph[from][to]` 依然可以返回一个有意义的结果。

```go
// 嵌套map的例子
var graph = make(map[string]map[string]bool)

func addEdge(from, to string) {
    edges := graph[from]
    if edges == nil {
        edges = make(map[string]bool)
        graph[from] = edges
    }
    edges[to] = true
}

func hasEdge(from, to string) bool {
    // 即使没有初始化 (graph[from]==nil), 也是有类型的, 因此会返回bool 的默认值.
    return graph[from][to]
}
```


#### map 的迭代顺序是随机的

Map的迭代顺序是不确定的，并且不同的哈希函数实现可能导致不同的遍历顺序。**在实践中，遍历的顺序是随机的，每一次遍历的顺序都不相同**。这是故意的，每次都使用随机的遍历顺序可以强制要求程序不会依赖具体的哈希函数实现。**如果要按顺序遍历key/value对，我们必须显式地对key进行排序**，可以使用sort包的Strings函数对字符串slice进行排序。下面是常见的处理方式：

```go
import "sort"

var names []string
for name := range ages {
    names = append(names, name)
}
sort.Strings(names)
for _, name := range names {
    fmt.Printf("%s\t%d\n", name, ages[name])
}
```

- map类型的零值是nil，也就是 **没有引用任何哈希表**
- map上的大部分操作，包括查找、删除、len和range循环都可以安全工作在nil值的map上，它们的行为和一个空的map类似。但是向一个nil值的map存入元素将导致一个panic异常
- 因此, 在向map存数据前必须先创建map (指向哈希表)

```go
var ages map[string]int
fmt.Println(ages == nil)    // "true"
fmt.Println(len(ages) == 0) // "true"

// 注意在修改 nil map (没有指向底层的哈希表) 是非法的.
// ages["carol"] = 21 // panic: assignment to entry in nil map
```

#### 从map中取值

!!! note
    之前说到, 查询map中的值是安全的, 不存在的话会返回零值. 那如何判断是已有的还是默认返回? 可以用 `age, ok := ages["bob"]` 的形式. (再搭配 `if !ok` 检查)

```GO
// 经常这样写: 用ok来判断是否存在
if age, ok := ages["bob"]; !ok { /* ... */ }
// 展开的写法
age, ok := ages["bob"]
if !ok { /* "bob" is not a key in this map; age == 0. */ }
```


#### map 比较

同样只能和nil进行比较. 下面实现了一般的比较写法.

```go
func equal(x, y map[string]int) bool {
    if len(x) != len(y) {
        return false
    }
    for k, xv := range x {
        // 注意用ok来检查 k在y的键中.
        if yv, ok := y[k]; !ok || yv != xv {
            return false
        }
    }
    return true
}
```

#### map 来实现 set

Go语言中并没有提供一个set类型，但是map中的key也是不相同的，可以用map实现类似set的功能。

- 例如, `map[string]bool` 记录字符串 set

有时候我们需要一个map或set的key是slice类型，但是map的key必须是可比较的类型，但是slice并不满足这个条件。不过，我们可以通过两个步骤绕过这个限制。第一步，定义一个辅助函数 `k`，将slice转为map对应的string类型的key，确保只有x和y相等时 `k(x) == k(y)` 才成立。然后创建一个key为string类型的map，在每次对map操作时先用k辅助函数将slice转化为string类型。

使用同样的技术可以处理任何不可比较的key类型，而不仅仅是slice类型。这种技术对于想使用自定义key比较函数的时候也很有用，例如在比较字符串的时候忽略大小写。同时，辅助函数 `k(x)` 也不一定是字符串类型，它可以返回任何可比较的类型，例如整数、数组或结构体等。

```go
// 使用map来记录提交相同的字符串列表的次数
var m = make(map[string]int)

// fmt.Sprintf函数将字符串列表转换为一个字符串以用于map的key
// %q, 输出 带双引号的字符串"abc"或带单引号的字符'c'
func k(list []string) string { return fmt.Sprintf("%q", list) }

func Add(list []string)       { m[k(list)]++ }
func Count(list []string) int { return m[k(list)] }
```

### 结构体 struct

结构体是一种聚合的数据类型，是由零个或多个任意类型的值聚合成的实体。每个值称为结构体的成员。用结构体的经典案例处理公司的员工信息，每个员工信息包含一个唯一的员工编号、员工的名字、家庭住址、出生日期、工作岗位、薪资、上级领导等等。所有的这些信息都需要绑定到一个实体中，可以作为一个整体单元被复制，作为函数的参数或返回值，或者是被存储到数组中，等等。

```go
// 声明了一个叫Employee的命名的结构体类型
type Employee struct {
    ID        int
    // Name      string
    // Address   string

    // 相同类型的, 可以进行合并
    Name, Address string
    DoB       time.Time
    Position  string
    Salary    int
    ManagerID int
}
// 声明了一个Employee类型的变量
var dilbert Employee

// . 操作访问成员
dilbert.Salary -= 5000 // demoted, for writing too few lines of code

// 指针. 可以对整个struct, 也可以是成员
position := &dilbert.Position
*position = "Senior " + *position // promoted, for outsourcing to Elbonia

// 对于 *Employee 指针类型, 可以直接用 `.` 操作使用; 等价于下面第二种写法
var employeeOfTheMonth *Employee = &dilbert
employeeOfTheMonth.Position += " (proactive team player)"
(*employeeOfTheMonth).Position += " (proactive team player)"
```

- 如果结构体成员名字是以大写字母开头的，那么该成员就是导出的；这是Go语言导出规则决定的。一个结构体可能同时包含导出和未导出的成员。
- 一个命名为S的结构体类型将不能再包含S类型的成员：因为一个聚合的值不能包含它自身。（该限制同样适应于数组。）但是S类型的结构体可以包含`*S`指针类型的成员，这可以让我们创建递归的数据结构，比如链表和树结构等。
- 空结构体 `struct{}`

> 如果结构体没有任何成员的话就是空结构体，写作 `struct{}`。它的大小为0，也不包含任何信息，但是有时候依然是有价值的。有些Go语言程序员用map带模拟set数据结构时，用它来代替map中布尔类型的value，只是强调key的重要性，但是因为节约的空间有限，而且语法比较复杂，所有我们通常避免这样的用法。

```go
seen := make(map[string]struct{}) // set of strings
// ...
if _, ok := seen[s]; !ok {
    seen[s] = struct{}{}
    // ...first time seeing s...
}
```


#### 在函数中使用结构体

```go
// 将根据给定的员工ID返回对应的员工信息结构体的指针
func EmployeeByID(id int) *Employee { /* ... */ }

// 可以使用点操作符号来访问成员, 或者进行修改.
fmt.Println(EmployeeByID(dilbert.ManagerID).Position) // "Pointy-haired boss"

id := dilbert.ID
EmployeeByID(id).Salary = 0 // fired for... no real reason
```

后面的语句通过EmployeeByID返回的结构体指针更新了Employee结构体的成员。如果将EmployeeByID函数的返回值从 `*Employee` 指针类型改为 `Employee` 值类型，那么更新语句将不能编译通过，因为在赋值语句的左边并不确定是一个变量（译注：调用函数返回的是值，并不是一个可取地址的变量）。

#### 例子: 树搜索

注意struct不能嵌套(正如list一样), 但允许在其中定义结构体指针. 下例展示了树节点的定义, 以及实现的 树排序.

```go
/* 树排序
调用: Sort(slice) 即可
*/
type tree struct {
 value       int
 left, right *tree
}

// Sort sorts values in place.
func Sort(values []int) {
 var root *tree
 for _, v := range values {
  root = add(root, v)
 }
 appendValues(values[:0], root)
}

// appendValues appends the elements of t to values in order
// and returns the resulting slice.
func appendValues(values []int, t *tree) []int {
 if t != nil {
  values = appendValues(values, t.left)
  values = append(values, t.value)
  values = appendValues(values, t.right)
 }
 return values
}

func add(t *tree, value int) *tree {
 if t == nil {
  // Equivalent to return &tree{value: value}.
  t = new(tree)
  t.value = value
  return t
 }
 if value < t.value {
  t.left = add(t.left, value)
 } else {
  t.right = add(t.right, value)
 }
 return t
}
```

### JSON

JavaScript对象表示法（JSON）是一种用于发送和接收结构化信息的标准协议。在类似的协议中，JSON并不是唯一的一个标准协议。 XML（§7.14）、ASN.1 和 Google的Protocol Buffers 都是类似的协议，并且有各自的特色，但是由于简洁性、可读性和流行程度等原因，JSON是应用最广泛的一个。

Go语言对于这些标准格式的编码和解码都有良好的支持，由标准库中的 `encoding/json、encoding/xml、encoding/asn1` 等包提供支持（译注：Protocol Buffers的支持由 `github.com/golang/protobuf` 包提供），并且这类包都有着相似的API接口。本节，我们将对重要的encoding/json包的用法做个概述。

JSON是对JavaScript中各种类型的值 —— **字符串、数字、布尔值和对象** —— Unicode本文编码。它可以用有效可读的方式表示第三章的基础数据类型和本章的数组、slice、结构体和map等聚合数据类型。

基本的JSON类型有 **数字（十进制或科学记数法）、布尔值（true或false）、字符串**，其中字符串是以双引号包含的Unicode字符序列，支持和Go语言类似的反斜杠转义特性，不过JSON使用的是`\Uhhhh`转义数字来表示一个UTF-16编码（译注：UTF-16和UTF-8一样是一种变长的编码，有些Unicode码点较大的字符需要用4个字节表示；而且UTF-16还有大端和小端的问题），而不是Go语言的rune类型。

这些基础类型可以通过JSON的数组和对象类型进行递归组合。一个JSON数组是一个有序的值序列，写在一个方括号中并以逗号分隔；一个JSON数组可以用于编码Go语言的数组和slice。一个JSON对象是一个字符串到值的映射，写成以系列的name:value对形式，用花括号包含并以逗号分隔；JSON的对象类型可以用于编码Go语言的map类型（key类型是字符串）和结构体。

```sh
# 对应表达关系
boolean         true
number          -273.15
string          "She said \"Hello, BF\""
array           ["gold", "silver", "bronze"]
object          {"year": 1980,
                 "event": "archery",
                 "medals": ["gold", "silver", "bronze"]}
```

#### Marshal, Unmarshal

例子: 电影结构体


```go
// 结构体定义和实例
type Movie struct {
    Title  string
    Year   int  `json:"released"`       // 结构体成员Tag
    Color  bool `json:"color,omitempty"`
    Actors []string
}
var movies = []Movie{
    {Title: "Casablanca", Year: 1942, Color: false,
        Actors: []string{"Humphrey Bogart", "Ingrid Bergman"}},
    {Title: "Cool Hand Luke", Year: 1967, Color: true,
        Actors: []string{"Paul Newman"}},
    {Title: "Bullitt", Year: 1968, Color: true,
        Actors: []string{"Steve McQueen", "Jacqueline Bisset"}},
    // ...
}
// 输出
// [{"Title":"Casablanca","released":1942,"Actors":["Humphrey Bogart","Ingrid Bergman"]},
// {"Title":"Cool Hand Luke","released":1967,"color":true,"Actors":["Paul Newman"]},
// {"Title":"Bullitt","released":1968,"color":true,"Actors":["Steve McQueen","Jacqueline Bisset"]}]

// Marshal 转为紧凑形式的字符串
data, err := json.Marshal(movies)
if err != nil {
    log.Fatalf("JSON marshaling failed: %s", err)
}
fmt.Printf("%s\n", data)
// 相应的, MarshalIndent 将产生整齐缩进的输出
data, err := json.MarshalIndent(movies, "", "    ")
```

在编码时，默认使用Go语言结构体的成员名字作为JSON的对象（通过reflect反射技术，我们将在12.6节讨论）。只有导出的结构体成员才会被编码，这也就是我们为什么选择用大写字母开头的成员名称。

细心的读者可能已经注意到，其中Year名字的成员在编码后变成了released，还有Color成员编码后变成了小写字母开头的color。这是因为构体成员Tag所导致的。一个构体成员Tag是和在编译阶段关联到该成员的元信息字符串

结构体的成员Tag可以是任意的字符串面值，但是通常是一系列用空格分隔的key:"value"键值对序列；因为值中含义双引号字符，因此成员Tag一般用原生字符串面值的形式书写。json开头键名对应的值用于控制encoding/json包的编码和解码的行为，并且encoding/...下面其它的包也遵循这个约定。成员Tag中json对应值的第一部分用于指定JSON对象的名字，比如将Go语言中的TotalCount成员对应到JSON中的total_count对象。Color成员的Tag还带了一个额外的 `omitempty` 选项，表示当Go语言结构体成员为空或零值时不生成JSON对象（这里false为零值）。果然，Casablanca是一个黑白电影，并没有输出Color成员。


**编码的逆操作是解码**，对应将JSON数据解码为Go语言的数据结构，Go语言中一般叫unmarshaling，通过json.Unmarshal函数完成。下面的代码将JSON格式的电影数据解码为一个结构体slice，结构体中只有Title成员。通过定义合适的Go语言数据结构，我们可以选择性地解码JSON中感兴趣的成员。当Unmarshal函数调用返回，slice将被只含有Title信息值填充，其它JSON成员将被忽略。

```go
var titles []struct{ Title string }
if err := json.Unmarshal(data, &titles); err != nil {
    log.Fatalf("JSON unmarshaling failed: %s", err)
}
fmt.Println(titles) // "[{Casablanca} {Cool Hand Luke} {Bullitt}]"
```

#### 例子: GitHub 查询 issues

[ch4-05](https://yar999.gitbook.io/gopl-zh/ch4/ch4-05)

许多web服务都提供JSON接口，通过HTTP接口发送JSON格式请求并返回JSON格式的信息。为了说明这一点，我们通过Github的issue查询服务来演示类似的用法。

下面定义了一些类型

```go
// Package github provides a Go API for the GitHub issue tracker.
// See https://developer.github.com/v3/search/#search-issues.
package github

import "time"

const IssuesURL = "https://api.github.com/search/issues"

type IssuesSearchResult struct {
    TotalCount int `json:"total_count"`
    Items          []*Issue
}

type Issue struct {
    Number    int
    HTMLURL   string `json:"html_url"`
    Title     string
    State     string
    User      *User
    CreatedAt time.Time `json:"created_at"`
    Body      string    // in Markdown format
}

type User struct {
    Login   string
    HTMLURL string `json:"html_url"`
}
```

然后是查询函数

> 在早些的例子中，我们使用了json.Unmarshal函数来将JSON格式的字符串解码为字节slice。但是这个例子中，我们使用了基于流式的解码器json.Decoder，它可以从一个输入流解码JSON数据，尽管这不是必须的。如您所料，还有一个针对输出流的json.Encoder编码对象。

```go
package github

import (
    "encoding/json"
    "fmt"
    "net/http"
    "net/url"
    "strings"
)

// main 的调用形式: ./issues repo:golang/go is:open json decoder 传入后面的 args
// SearchIssues queries the GitHub issue tracker.
func SearchIssues(terms []string) (*IssuesSearchResult, error) {
    // 因为用户提供的查询条件可能包含类似`?`和`&`之类的特殊字符，为了避免对URL造成冲突，我们用url.QueryEscape来对查询中的特殊字符进行转义操作。
    q := url.QueryEscape(strings.Join(terms, " "))
    resp, err := http.Get(IssuesURL + "?q=" + q)
    if err != nil {
        return nil, err
    }

    // We must close resp.Body on all execution paths.
    // (Chapter 5 presents 'defer', which makes this simpler.)
    if resp.StatusCode != http.StatusOK {
        resp.Body.Close()
        return nil, fmt.Errorf("search query failed: %s", resp.Status)
    }

    var result IssuesSearchResult
    // 使用了基于流式的解码器json.Decoder，它可以从一个输入流解码JSON数据
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        resp.Body.Close()
        return nil, err
    }
    resp.Body.Close()
    return &result, nil
}
```

### 文本和HTML模板





## 函数

> 我们已经见过许多函数了。现在，让我们多花一点时间来彻底地讨论函数特性。本章的运行示例是一个网络蜘蛛，也就是web搜索引擎中负责抓取网页部分的组件，它们根据抓取网页中的链接继续抓取链接指向的页面。一个网络蜘蛛的例子给我们足够的机会去探索递归函数、匿名函数、错误处理和函数其它的很多特性。

### 函数声明

函数声明包括函数名、形式参数列表、返回值列表（可省略）以及函数体。

```go
func name(parameter-list) (result-list) {
    body
}
```

#### 函数的标识符

```go
// 函数的标识符
func add(x int, y int) int   {return x + y}
func sub(x, y int) (z int)   { z = x - y; return}
func first(x int, _ int) int { return x }       // .blank identifier(译者注：即下文的_符号)可以强调某个参数未被使用
func zero(int, int) int      { return 0 }

fmt.Printf("%T\n", add)   // "func(int, int) int"
fmt.Printf("%T\n", sub)   // "func(int, int) int"
fmt.Printf("%T\n", first) // "func(int, int) int"
fmt.Printf("%T\n", zero)  // "func(int, int) int"
```

函数的类型被称为 **函数的标识符**。如果两个函数形式参数列表和返回值列表中的变量类型一一对应，那么这两个函数被认为有相同的类型和标识符。形参和返回值的变量名不影响函数标识符也不影响它们是否可以以省略参数类型的形式表示。

**每一次函数调用都必须按照声明顺序为所有参数提供实参（参数值）**。在函数调用时，Go语言没有默认参数值，也没有任何方法可以通过参数名指定形参，因此形参和返回值的变量名对于函数调用者而言没有意义。

在函数体中，函数的形参作为局部变量，被初始化为调用者提供的值。函数的形参和有名返回值作为函数最外层的局部变量，被存储在相同的词法块中。

**实参通过值的方式传递，因此函数的形参是实参的拷贝**。对形参进行修改不会影响实参。但是，如果实参包括引用类型，如指针，slice(切片)、map、function、channel等类型，实参可能会由于函数的间接引用被修改。

**你可能会偶尔遇到没有函数体的函数声明，这表示该函数不是以Go实现的**。这样的声明定义了函数标识符。

```go
package math
// 你可能会偶尔遇到没有函数体的函数声明，这表示该函数不是以Go实现的*
func Sin(x float64) float //implemented in assembly language
```

### 递归

例子: 处理HTML

```go
// 遍历HTML的节点树，从每一个anchor元素的href属性获得link,将这些links存入字符串数组中，并返回这个字符串数组
// visit appends to links each link found in n and returns the result.
func visit(links []string, n *html.Node) []string {
    if n.Type == html.ElementNode && n.Data == "a" {
        for _, a := range n.Attr {
            if a.Key == "href" {
                links = append(links, a.Val)
            }
        }
    }
    for c := n.FirstChild; c != nil; c = c.NextSibling {
        links = visit(links, c)
    }
    return links
}


// 通过递归的方式遍历整个HTML结点树，并输出树的结构。在outline内部，每遇到一个HTML元素标签，就将其入栈，并输出。
// 注意支持传入 nil. 
// outline(nil, doc)
func outline(stack []string, n *html.Node) {
    if n.Type == html.ElementNode {
        stack = append(stack, n.Data) // push tag
        fmt.Println(stack)
    }
    // 注意, 只有入栈而没有进行出栈, 因为被调用者接收的是stack的拷贝
    for c := n.FirstChild; c != nil; c = c.NextSibling {
        outline(stack, c)
    }
}
```

大部分编程语言使用固定大小的函数调用栈，常见的大小从64KB到2MB不等。固定大小栈会限制递归的深度，当你用递归处理大量数据时，需要避免栈溢出；除此之外，还会导致安全性问题。与相反, **Go语言使用可变栈，栈的大小按需增加(初始时很小)**。这使得我们使用递归时不必考虑溢出和安全问题。


### 多返回值

```go
// findLinks performs an HTTP GET request for url, parses the
// response as HTML, and extracts and returns the links.
func findLinks(url string) ([]string, error) {
    resp, err := http.Get(url)
    if err != nil {
        return nil, err
    }
    if resp.StatusCode != http.StatusOK {
        resp.Body.Close()
        return nil, fmt.Errorf("getting %s: %s", url, resp.Status)
    }
    doc, err := html.Parse(resp.Body)
    resp.Body.Close()
    if err != nil {
        return nil, fmt.Errorf("parsing %s as HTML: %v", url, err)
    }
    return visit(nil, doc), nil
}

// 调用
links, err := findLinks(url)
links, _ := findLinks(url) // errors ignored
```

在findlinks中，有4处return语句，每一处return都返回了一组值。前三处return，将http和html包中的错误信息传递给findlinks的调用者。第一处return直接返回错误信息，其他两处通过fmt.Errorf（§7.8）输出详细的错误信息。如果findlinks成功结束，最后的return语句将一组解析获得的连接返回给用户。

在finallinks中，我们必须确保resp.Body被关闭，释放网络资源。**虽然Go的垃圾回收机制会回收不被使用的内存，但是这不包括操作系统层面的资源，比如打开的文件、网络连接**。因此我们必须显式的释放这些资源。

- bare return

如果一个函数将所有的返回值都显示的变量名，那么该函数的return语句可以省略操作数。这称之为 **bare return**。

### 错误

在Go中有一部分函数总是能成功的运行。比如strings.Contains和strconv.FormatBool函数，对各种可能的输入都做了良好的处理，使得运行时几乎不会失败，除非遇到灾难性的、不可预料的情况，比如运行时的内存溢出。导致这种错误的原因很复杂，难以处理，从错误中恢复的可能性也很低。

还有一部分函数只要输入的参数满足一定条件，也能保证运行成功。比如time.Date函数，该函数将年月日等参数构造成time.Time对象，除非最后一个参数（时区）是nil。这种情况下会引发panic异常。panic是来自被调函数的信号，表示发生了某个已知的bug。一个良好的程序永远不应该发生panic异常。

对于大部分函数而言，永远无法确保能否成功运行。这是因为错误的原因超出了程序员的控制。举个例子，任何进行I/O操作的函数都会面临出现错误的可能，只有没有经验的程序员才会相信读写操作不会失败，即时是简单的读写。因此，当本该可信的操作出乎意料的失败后，我们必须弄清楚导致失败的原因。

在Go的错误处理中，错误是软件包API和应用程序用户界面的一个重要组成部分，程序运行失败仅被认为是几个预期的结果之一。

对于那些 **将运行失败看作是预期结果的函数，它们会返回一个额外的返回值，通常是最后一个，来传递错误信息**。

- 如果导致失败的原因只有一个，额外的返回值可以是一个布尔值，通常被命名为ok。
- 通常，导致失败的原因不止一种，尤其是对I/O操作而言，用户需要了解更多的错误信息。因此，额外的返回值不再是简单的布尔类型，而是 `error` 类型

内置的error是接口类型。我们将在第七章了解接口类型的含义，以及它对错误处理的影响。现在我们只需要明白error类型可能是nil或者non-nil。nil意味着函数运行成功，non-nil表示失败。对于non-nil的error类型,我们可以通过调用error的Error函数或者输出函数获得字符串类型的错误信息。

- 区分异常 exception

在Go中，函数运行失败时会返回错误信息，这些错误信息被认为是一种预期的值而非异常（exception），这使得Go有别于那些将函数运行失败看作是异常的语言。虽然Go有各种异常机制，但这些机制仅被使用在处理那些未被预料到的错误，即bug，而不是那些在健壮程序中应该被避免的程序错误。对于Go的异常机制我们将在5.9介绍。

Go这样设计的原因是由于对于某个应该在控制流程中处理的错误而言，将这个错误以异常的形式抛出会混乱对错误的描述，这通常会导致一些糟糕的后果。当某个程序错误被当作异常处理后，这个错误会将堆栈根据信息返回给终端用户，这些信息复杂且无用，无法帮助定位错误。

正因此，Go使用控制流机制（如if和return）处理异常，这使得编码人员能更多的关注错误处理。

### 函数值

在Go中，函数被看作第一类值（first-class values）：函数像其他值一样，拥有类型，可以被赋值给其他变量，传递给函数，从函数返回。对函数值（function value）的调用类似函数调用。

```go
// 函数签名/标识符
func square(n int) int { return n * n }
func negative(n int) int { return -n }
func product(m, n int) int { return m * n }

f := square
fmt.Println(f(3)) // "9"

f = negative
fmt.Println(f(3))     // "-3"
fmt.Printf("%T\n", f) // "func(int) int"

f = product // compile error: can't assign func(int, int) int to func(int) int


// 零值: nil
var f func(int) int
f(3) // 此处f的值为nil, 会引起panic错误
// 可以与nil进行比较
// 但是函数值之间是不可比较的，也不能用函数值作为map的key。
var f func(int) int
if f != nil {
    f(3)
}
```

#### 作用: 将函数作为参数传递

**函数值使得我们不仅仅可以通过数据来参数化函数，亦可通过行为**. strings.Map对字符串中的每个字符调用add1函数，并将每个add1函数的返回值组成一个新的字符串返回给调用者。

```go
    func add1(r rune) rune { return r + 1 }

    fmt.Println(strings.Map(add1, "HAL-9000")) // "IBM.:111"
    fmt.Println(strings.Map(add1, "VMS"))      // "WNT"
    fmt.Println(strings.Map(add1, "Admix"))    // "Benjy"
```


例子: 格式化输出HTML节点结构

```go
// forEachNode 遍历HTML页面的所有结点. 对于HTML的层级按照缩紧输出. 格式化输出的方式是, 对每个节点前后调用 pre, post 函数
// forEachNode针对每个结点x,都会调用pre(x)和post(x)。
// pre和post都是可选的。
// 遍历孩子结点之前,pre被调用
// 遍历孩子结点之后，post被调用
func forEachNode(n *html.Node, pre, post func(n *html.Node)) {
    if pre != nil {
        pre(n)
    }
    for c := n.FirstChild; c != nil; c = c.NextSibling {
        forEachNode(c, pre, post)
    }
    if post != nil {
        post(n)
    }
}

// 全局变量, 记录节点深度. 辅助输出.
var depth int
func startElement(n *html.Node) {
    if n.Type == html.ElementNode {
        fmt.Printf("%*s<%s>\n", depth*2, "", n.Data)
        depth++
    }
}
func endElement(n *html.Node) {
    if n.Type == html.ElementNode {
        depth--
        fmt.Printf("%*s</%s>\n", depth*2, "", n.Data)
    }
}
```

### 匿名函数


### 可变参数


### Deferred 函数


### Panic 异常


### Recover 捕获异常


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

