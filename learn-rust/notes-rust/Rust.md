
- official: <https://www.rust-lang.org/>
    - repo: <https://github.com/rust-lang/rust>
    - 文档: [《The Rust Programming Language》](https://doc.rust-lang.org/book/), [repo](https://github.com/rust-lang/book) (`rustup doc` 本地打开), 有 [中文版](https://kaisery.github.io/trpl-zh-cn/).
- Rust语言圣经(Rust Course): <https://course.rs/about-book.html> (⭐️)
    - [repo](https://github.com/sunface/rust-course)
    - 配套练习题: <https://zh.practice.rs/>; [repo](https://github.com/sunface/rust-by-practice); [solutions](https://github.com/sunface/rust-by-practice/tree/master/solutions)
    - 还可以搭配写算法: [Rust算法教程](https://algos.rs/about-book.html)
- Rusty Book(锈书): <https://rusty.rs/about.html>.
    - awesome+cookbook, [repo](https://github.com/rustlang-cn/rusty-book)

以下为 Rust Course 学习笔记.

## 安装与配置

```sh
# 启动本地文档
rustup doc


# 安装 Linux, macOS 通用
curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
rustup self uninstall   # 卸载
```

### VSCode

- VSCode: <https://code.visualstudio.com/docs/languages/rust>
- 插件
    - `rust-analyzer` 社区驱动替代了官方的支持插件
    - `CodeLLDB`, Debugger 程序
    - `Even Better TOML`，支持 .toml 文件完整特性
    - `Error Lens`, 更好的获得错误展示

所提供的一些功能

- IntelliSense
    - Inlay hints 推断变量类型
    - Hover information 鼠标停留查看信息
    - Auto completions
- Semantic syntax highlighting
    - 例如mut变量是有下划线的. 可以在 `editor.semanticTokenColorCustomizations` 设置
- Linting
    - provided by rustc and clippy, to detect issues with your source code
    - 可以通过以下开启 [clippy](https://github.com/rust-lang/rust-clippy): change the **Rust-analyzer \> Check on Save: Command** (`rust-analyzer.checkOnSave.command`) setting to `clippy` instead of the default `check`
- Formatting
    - 通过 [rustfmt](https://github.com/rust-lang/rustfmt),
    - 快捷键 `Shift+Option+F`

Debug

注意需要安装插件 `Microsoft C++` (ms-vscode.cpptools) 或 `CodeLLDB` (vadimcn.vscode-lldb)


## Cargo

```sh
cargo new world_hello

# 编译并运行 (默认debug模式, 尽快编译不做优化)
cargo run
cargo build & ./target/debug/world_hello
# 相较于debug模型的是release
cargo run --release
cargo build --release

# Cargo 的编译还是比较慢的, check快速检查代码是否正确
cargo check
```

### Cargo.toml

`Cargo.toml` 是 `cargo` 特有的**项目数据描述文件**; `Cargo.lock` 文件是 `cargo` 工具根据同一项目的 `toml` 文件生成的**项目依赖详细清单**. 一般只需要看toml即可.

什么情况下该把 `Cargo.lock` 上传到 git 仓库里？很简单，当你的项目是一个可运行的程序时，就上传 `Cargo.lock`，如果是一个依赖库项目，那么请把它添加到 `.gitignore` 中

定义项目依赖: 三种方式

- 基于 Rust 官方仓库 `crates.io`，通过版本说明来描述
- 基于项目源代码的 git 仓库地址，通过 URL 来描述
- 基于本地项目的绝对路径或者相对路径，通过类 Unix 模式的路径来描述

```toml
[dependencies]
rand = "0.3"
hammer = { version = "0.5.0"}
color = { git = "https://github.com/bjz/color-rs" }
geometry = { path = "crates/geometry" }

```

## Rust 基础

### 变量绑定与解构

- 变量绑定
- 可变 `mut` (不同于常量)
- 使用下划线开头忽略未使用的变量 (否则有warning)
- 变量解构变量遮蔽(shadowing): 允许使用相同名字不同类型的变量, 需要重新声明

#### 变量解构

```rust
fn main() {
    let (a, mut b): (bool,bool) = (true, false);
    // a = true,不可变; b = false，可变
    println!("a = {:?}, b = {:?}", a, b);

    b = true;
    assert_eq!(a, b);
}
```

解构式赋值

```rust
struct Struct {
    e: i32
}

fn main() {
    let (a, b, c, d, e);

    (a, b) = (1, 2);
    // _ 代表匹配一个值，但是我们不关心具体的值是什么，因此没有是一个变量名而是使用了 _
    [c, .., d, _] = [1, 2, 3, 4, 5];
    Struct { e, .. } = Struct { e: 5 };

    assert_eq!([1, 2, 1, 4, 5], [a, b, c, d, e]);
}

```

### 基本类型

- 数值类型: 有符号整数 (`i8`, `i16`, `i32`, `i64`, `isize`)、 无符号整数 (`u8`, `u16`, `u32`, `u64`, `usize`) 、浮点数 (`f32`, `f64`)、以及有理数、复数
- 字符串：字符串字面量和字符串切片 `&str`
- 布尔类型： `true`和`false`
- 字符类型: 表示单个 Unicode 字符，存储为 4 个字节
- 单元类型: 即 `()` ，其唯一的值也是 `()`

类型推导

```rust
// 报错: 编译器在这里无法推导出我们想要的类型：整数？浮点数？字符串？
let guess = "42".parse().expect("Not a number!");
// 给定显式的类型: 下面两种方式
let guess: i32 = ...
... "42".parse::<i32>()
```

#### basic types 例子

```rust
fn main() {
    // 默认类型为 i32
    let x = 5;
    assert_eq!("i32".to_string(), type_of(&x));
}

// 以下函数可以获取传入参数的类型，并返回类型的字符串形式，例如  "i8", "u8", "i32", "u32"
fn type_of<T>(_: &T) -> String {
    format!("{}", std::any::type_name::<T>())
}

```


#### 数值类型

整数类型

- `i8, i16, i32, i64, i128, isize, u8,..., usize` 分别表示有/无符号整数, isize表示按照架构默认 (一般用作索引)
- 字面量: `98_222, 0xff, 0o77, 0b1111_0000` 分别表示不同的进制; 对于u8, 也即一字节的整数, 还可以用 `b'A'` 来表示.

格式化输出

```rust
    println!("0011 XOR 0101 is {:04b}", 0b0011u32 ^ 0b0101);
    println!("1 << 5 is {}", 1u32 << 5);
```


关于整型溢出

- 注意, 在 Rust中, debug模式编译的时候会检查, 若发生则会panic
- 而 release编译时, 则不会检查, 若发生会按照「会按照补码循环溢出（two’s complement wrapping）的规则处理」
- 要显式处理溢出, 可以使用标准库针对原始数字类型提供的这些方法
    - 使用 `wrapping_*` 方法在所有模式下都按照补码循环溢出规则处理，例如 `wrapping_add`
    - 如果使用 `checked_*` 方法时发生溢出，则返回 `None` 值
    - 使用 `overflowing_*` 方法返回该值和一个指示是否存在溢出的布尔值
    - 使用 `saturating_*` 方法使值达到最小值或最大值

浮点类型

- `f32, f64` 注意在现代的 CPU 中两者速度几乎相同.
- 注意浮点数的精度问题
    - 例如, `assert!(0.1 + 0.2 == 0.3);` 会报错! 因为 `0.1+0.2` 的结果在 f64 表示下会有一个很小的剩余 (Python中也是一样的).
    - 要 **比较浮点数是否相等**, 可以用 `(0.1_f64 + 0.2 - 0.3).abs() < 0.00001`
- 注意, 在使用类型相应方法, 需要显式指定而不能只用子面量, 例如 `13.14_f32.round()` 进行取整.

类型转换

- 可以用 `as` 进行类型转换, 例如 `let v: u16 = 38_u8 as u16;`

数字运算

- 见 [Appendix B](https://course.rs/appendix/operators.html)

位运算

- `&|^, !, <<, >>`

序列 range

- `1..5` 生成 1到4, 而 `1..=5` 则包括了5.
- 只能采用数字或字符, 例如 `'a'..='z'`

```rust
for i in 1..=5 {
    println!("{}",i);
}

// 
use std::ops::{Range, RangeInclusive};
fn main() {
    assert_eq!((1..5), Range{ start: 1, end: 5 });
    assert_eq!((1..=5), RangeInclusive::new(1, 5));
}
```

有理数, 复数

- std 中并没有, 可以用 [num](https://crates.io/crates/num) 包

```rust
use num::complex::Complex;

 fn main() {
   let a = Complex { re: 2.1, im: -1.2 };
   let b = Complex::new(11.1, 22.2);
   let result = a + b;

   println!("{} + {}i", result.re, result.im)
 }
```



#### 字符、布尔、单元类型

- 字符 char
    - 表示Unicode字符, 占用4个字节
    - 只能用 `''` 表示
    - 用 `std::mem::size_of_val(&x)` 查看空间占用
- 布尔 bool
    - `true` 和 `false`
- 单元类型
    - 唯一的值是 `()`, 注意其占用空间为0
    - main, println 的返回值就是 `()` (没有返回值的函数在 Rust 中是有单独的定义的：`发散函数( diverge function )`)
    - 你可以用 `()` 作为 `map` 的值，表示我们不关注具体的值，只关注 `key`。 这种用法和 Go 语言的 `struct{}` 类似，可以作为一个值用来占位，但是完全**不占用**任何内存

#### 语句和表达式

- 语句和表达式 (statement, expression)
    - 语句执行了一定的操作, 没有返回值
    - 用 `{}` 包裹的段中, 若最后的一个是表达式, 那个整个快就是一个表达式 (有返回值)
    - 注意, 表达式的结尾不能带有 `;`, 不然就变成了语句

#### 函数

- 和其他语言差不多, 不多做介绍
- 注意, 函数声明语句中, `()` 内的所有 identifier 都要明确类型; 返回值默认为 `()`, 否则需要明确
- `!` 作为返回类型时, 说明该函数永不返回( diverge function ), 一般会造成程序崩溃?

```rust
fn main() {
    println!("Success!");
}

fn get_option(tp: u8) -> Option<i32> {
    match tp {
        1 => {
            // TODO
        }
        _ => {
            // TODO
        }
    };
    
    // 这里与其返回一个 None，不如使用发散函数替代
    never_return_fn()
}

// 使用三种方法实现以下发散函数
fn never_return_fn() -> ! {
    // 也是一种panic?
    unimplemented!()
}
fn never_return_fn() -> ! {
    panic!()
}
use std::thread;
use std::time;
fn never_return_fn() -> ! {
    loop {
        std::thread::sleep(std::time::Duration::from_secs(1))
    }
}
```

### 所有权和借用

!!! note
    Rust 之所以能成为万众瞩目的语言，就是因为其内存安全性。在以往，内存安全几乎都是通过 GC 的方式实现，但是 GC 会引来性能、内存占用以及 Stop the world 等问题，在高性能场景和系统编程上是不可接受的，因此 Rust 采用了与(错)众(误)不(之)同(源)的方式：所有权系统。

处理内存的方式:

- 垃圾回收机制(GC)，在程序运行时不断寻找不再使用的内存，典型代表：Java、Go
- 手动管理内存的分配和释放, 在程序中，通过函数调用的方式来申请和释放内存，典型代表：C++
- 通过所有权来管理内存，编译器在编译时会根据一系列规则进行检查

什么是内存安全? 来看C的一段糟糕的代码:

```c
int* foo() {
    int a;          // 变量a的作用域开始
    a = 100;
    char *c = "xyz";   // 变量c的作用域开始
    return &a;
}                   // 变量a和c的作用域结束
```

这里的问题: 1) 返回了a的指针, 但局部变量a在作用域之外已经被回收, 因此造成了「悬空指针(Dangling Pointer)」问题; 2) c时常量字符串存储于常量区, 但作为局部变量直到程序结束才会被回收, 造成内存浪费.

栈(Stack)与堆(Heap)

- 栈: 连续空间, 数据大小都一致. 进栈, 出栈
- 堆: 大小不确定, 需要在堆中查找一块足够大的空间, 叫做 分配(allocating).
- 性能: 显然栈的处理和分配都要快很多.

所有权原则

- Rust 中每一个值都被一个变量所拥有，该变量被称为值的所有者
- 一个值同时只能被一个变量所拥有，或者说一个值只能拥有一个所有者
- 当所有者(变量)离开作用域范围时，这个值将被丢弃(drop)

明确几个概念:

- 克隆(深拷贝): 涉及堆性能较差, Rust 不会自动执行, 例如对于String可以手动 `s1.clone()`
- 拷贝(浅拷贝): 只发生在栈上, 对于基本变量都是自动 Copy, 因此 **不会发生所有权问题**
    - 哪些是可 Copy的? 处理之前介绍的基本类型
    - 元组中的类型都是可 Copy的情况. 比如，`(i32, i32)` 是 `Copy` 的，但 `(i32, String)` 就不是
    - 不可变引用 `&T`, 例如 `let x: &str = "hello, world";`. 但是 可变引用 `&mut T` 是不可以 Copy的

#### 函数传值与返回

- 将值传给函数, 也会发生移动/复制. 也上面 `=` 赋值的情况类似, 栈内的在传入后仍然可用, 但堆中的的由于所有权进行了「移交」, 之后将不可用 (例如下面例子中的 s2).

```rust
fn main() {
    let s1 = gives_ownership();         // gives_ownership 将返回值
                                        // 移给 s1
    let s2 = String::from("hello");     // s2 进入作用域
    let s3 = takes_and_gives_back(s2);  // s2 被移动到 takes_and_gives_back 中,
                                        // s2 不可再被访问
                                        // 它也将返回值移给 s3
    println!("{}, {}", s1, s3);     // 这里使用 s2 会报错: value borrowed here after move
} // 这里, s3 移出作用域并被丢弃。s2 也移出作用域，但已被移走，
  // 所以什么也不会发生。s1 移出作用域并被丢弃

fn gives_ownership() -> String {             // gives_ownership 将返回值移动给
                                             // 调用它的函数
    let some_string = String::from("hello"); // some_string 进入作用域.
    some_string                              // 返回 some_string 并移出给调用的函数
}
// takes_and_gives_back 将传入字符串并返回该值
fn takes_and_gives_back(a_string: String) -> String { // a_string 进入作用域
    a_string  // 返回 a_string 并移出给调用的函数
}
```

#### 部分 move

当解构一个变量时，可以同时使用 `move` 和引用模式绑定的方式。当这么做时，部分 `move` 就会发生：变量中一部分的所有权被转移给其它变量，而另一部分我们获取了它的引用。

在这种情况下，原变量将无法再被使用，但是它没有转移所有权的那一部分依然可以使用，也就是之前被引用的那部分。

```rust
fn ownership_partly_transfer(){
    struct Person {
        name: String,
        age: Box<u8>,
    }

    let person = Person {
        name: String::from("Alice"),
        age: Box::new(20),
    };

    // 通过这种解构式模式匹配，person.name 的所有权被转移给新的变量 `name`
    // 但是，这里 `age` 变量确是对 person.age 的引用, 这里 ref 的使用相当于: let age = &person.age 
    let Person { name, ref age } = person;

    println!("The person's age is {}", age);
    println!("The person's name is {}", name);

    // Error! 原因是 person 的一部分已经被转移了所有权，因此我们无法再使用它
    //println!("The person struct is {:?}", person);

    // 虽然 `person` 作为一个整体无法再被使用，但是 `person.age` 依然可以使用
    println!("The person's age from person struct is {}", person.age);
}
```


#### Ownership 例子



```rust
// 下面用了三种方式来得到两个相等的字符串
fn f_clone(){
    let x = String::from("hello, world");
    let y = x.clone();
    println!("{},{}",x,y);
}
fn f_str() {
    let x = "hello, world";
    let y = x;
    println!("{},{}",x,y);
}
fn f_pointer() {
    let x = &String::from("hello, world");
    let y = x;
    println!("{},{}",x,y);
}
```

如何两次使用heap中的变量?

```rust
fn main() {
    let s = String::from("hello, world");
    print_str(s.clone());       // 进行clone
    println!("{}", s);
}

fn print_str(s: String)  {
    println!("{}",s);
}
```

注意, 所有权的转移与可变性是独立的.

```rust
    let s = String::from("hello, ");
    let mut s1 = s;     // 不加 mut 会报错
    s1.push_str("world")
```

### 引用与借用

上一节中, 每个heap数据只能传入一次, 显然很不方便.

#### 引用与解引用

就是指针的概念

```rust
    let x = 5;
    let y = &x;

    assert_eq!(5, x);
    assert_eq!(5, *y);
```

#### 不可变引用

引用默认是不可变的. 因此, 我们无需放弃指向对象的所有权.

```rust
fn main() {
    let s1 = String::from("hello");
    let len = calculate_length(&s1);

    println!("The length of '{}' is {}.", s1, len);
}

fn calculate_length(s: &String) -> usize {
    // 但是不能 修改不可变引用所引用的对象!
    // s.push_str(", world");
    s.len()
}
```

#### 可变引用

- 语法: 用 `mut T` 声明
- 可变引用只能存在一个 (不可变可以多个); 可变和不可变引用不能同时存在.
- 注意, 不同于变量作用域, 引用的作用域是直到「最后一次使用的位置」 (方便写代码).
    - 叫做: Non-Lexical Lifetimes(NLL)，专门用于找到某个引用在作用域(})结束前就不再被使用的代码位置

```rust
fn bollow_changable(){
    let mut s = String::from("hello");

    // 可变引用只能存在一个
    let r1 = &mut s;
    // let r2 = &mut s;
    println!("{}", r1);
    println!("{}", r1);

    // 引用的作用域到「最后一次使用的位置」
    let r2 = &mut s;
    r2.push_str(", world");
    println!("{}", r2);
}
```

引用的对象必须是有效的, 例如下面的代码会报错:

```rust
fn main() {
    let reference_to_nothing = dangle();
}

fn dangle() -> &String {
    let s = String::from("hello");
    // 返回一个对象已经被销毁的引用, 报错.
    &s
}

```

#### bollow 例子

利用String展示可变, 不可变的基本使用方式:

```rust
fn main() {
    let s = String::from("hello, ");
    borrow_object(&s)
}
fn borrow_object(s: &String) {}

// 可变, 注意引入需要 `&mut s`
fn main() {
    // 同时这里的 s 也需要声明是 mut
    let mut s = String::from("hello, ");
    push_str(&mut s)
}
fn push_str(s: &mut String) {
    s.push_str("world")
}
```

对于 String 的引用.

```rust
fn main() {
    let mut s = String::from("hello, ");    // 类型为 mut String

    let p = &mut s;                 // 类型为 mut String 的引用
    // 是一个引用
    println!("{}", get_addr(p));
    // 报错, 因为 println 传入的是 immutable borrow, 与上面的p 的 mutable borrow 冲突
    // println!("{}", s);
    
    // 但 p 可以直接用 String 的方法!
    p.push_str("world");
}

fn get_addr(r: &String) -> String {
    format!("{:p}", r)
}
```

`ref` 与 `&` 类似, 也是得到一个值的引用, 用法有所不同

```rust
fn main() {
    let c = '中';

    let r1 = &c;
    // 填写空白处，但是不要修改其它行的代码
    let ref r2 = c;

    assert_eq!(*r1, *r2);
    
    // 判断两个内存地址的字符串是否相等
    assert_eq!(get_addr(r1),get_addr(r2));
}

// 获取传入引用的内存地址的字符串形式
fn get_addr(r: &char) -> String {
    format!("{:p}", r)
}
```

借用与可变性

```rust
// 错误: 从不可变对象借用可变
fn main() {
    // 注意, 不能从不可变对象借用可变. 所以这一行必须是 mut的
    // let s = String::from("hello, ");
    let mut s = String::from("hello, ");

    borrow_object(&mut s)
}
fn borrow_object(s: &mut String) {}

// Ok: 从可变对象借用不可变
fn main() {
    let mut s = String::from("hello, ");
    // 从 mut 以不可变的形式来借用是合法的.
    borrow_object(&s);
    
    s.push_str("world");
}
fn borrow_object(s: &String) {}
```


### 复合类型

!!! todo

- String: <https://doc.rust-lang.org/std/string/struct.String.html>

#### 字符串和切片

和Go语言类似; 注意切片就是部分引用 (可变/不可变).

##### 切片语法

切片语法: `&s[0..5]`. 注意其中包含了一个 range (因此 `&s[0..=5]` 也是可以的).

```rust
let s = String::from("hello world");

let hello = &s[0..5];
let world = &s[6..11];
```

上面创建了一个不可变切片 (类型为 `&str`); 若s为 `mut String`, 则可通过 `&mut s[0..5]` 创建可变切片.

##### 什么是字符串

顾名思义，字符串是由字符组成的连续集合，但是在上一节中我们提到过，**Rust 中的字符是 Unicode 类型，因此每个字符占据 4 个字节内存空间，但是在字符串中不一样，字符串是 UTF-8 编码，也就是字符串中的字符所占的字节数是变化的(1 - 4)**，这样有助于大幅降低字符串所占用的内存空间。

Rust 在语言级别，只有一种字符串类型： `str`，它通常是以引用类型出现 `&str`，也就是上文提到的字符串切片。虽然语言级别只有上述的 `str` 类型，但是在标准库里，还有多种不同用途的字符串类型，其中使用最广的即是 `String` 类型。

`str` 类型是硬编码进可执行文件，也无法被修改，但是 `String` 则是一个可增长、可改变且具有所有权的 UTF-8 编码字符串，**当 Rust 用户提到字符串时，往往指的就是 `String` 类型和 `&str` 字符串切片类型，这两个类型都是 UTF-8 编码**。

除了 `String` 类型的字符串，Rust 的标准库还提供了其他类型的字符串，例如 `OsString`， `OsStr`， `CsString` 和 `CsStr` 等，注意到这些名字都以 `String` 或者 `Str` 结尾了吗？它们分别对应的是具有所有权和被借用的变量。

###### 字符串字面量是切片

字面量类型为 `&str`, 也即 `let s: &str = "Hello, world!";`. 它是一个 **不可变引用**.

#### String 与 &str 之间的转化

```rust
// &str 转 String
String::from("hello,world")
"hello,world".to_string()

// String 转 &str
fn string_str_trans() {
    let mut s = String::from("hello,world!");
    // 取引用转为 &str 类型
    say_hello(&s);
    say_hello(&mut s[..5]); // 切片也是一种引用
    say_hello(s.as_str());
}
fn say_hello(s: &str) {
    println!("{}", s);
}
```


##### 字符串操作

```rust
let mut s = String::from("Hello ");
```


- 追加 (Push): `push, push_str` 原地操作 (因此需要 mut)
    - `s.push('r');`
- 插入 (Insert): `insert, insert_str`
    - `s.insert(5, ',');`
- 替换 (Replace)
    - 下面两个返回新的字符串 (因此支持 Srtring 和 &str)
        - `s.replace("rust", "RUST");`; 替换所有匹配
        - `s.replacen("rust", "RUST", 1);` 替换指定数量
    - 将指定位置进行替换 (原地操作)
        - `s.replace_range(7..8, "R");`
- 删除 (Delete) 原地操作
    - `pop` —— 删除并返回字符串的最后一个字符
    - `remove` —— 删除并返回字符串中指定位置的字符
    - `truncate` —— 删除字符串中从指定位置开始到结尾的全部字符
    - `clear` —— 清空字符串
- 连接 (Catenate)
    - 使用 `+` 或者 `+=` 连接字符串，要求右边的参数必须为字符串的切片引用（Slice)类型
        - 注意实际上 add 的函数签名为 `fn add(self, s: &str) -> String`. 在下面的第二个例子中, s1 的所有权发生了转移
    - 使用 `format!` 连接字符串. 类似 println

```rust
fn string_catenate() {
    let string_append = String::from("hello ");
    let string_rust = String::from("rust");
    // &string_rust会自动解引用为 &str
    let result = string_append + &string_rust;
    // 必须是 mut
    let mut result = result + "!";
    result += "!!!";

    println!("连接字符串 + -> {}", result);
}
```

```rust
fn string_add() {
    let s1 = String::from("hello,");
    let s2 = String::from("world!");
    // 在下句中，s1的所有权被转移走了，因此后面不能再使用s1
    let s3 = s1 + &s2;
    assert_eq!(s3, "hello,world!");
    // 下面的语句如果去掉注释，就会报错
    // println!("{}",s1);
}
```

##### 字符串转义 (escape)

用 `\`  输出 ASCII, `\u{211D}` 的形式输出 Unicode.

```rust
fn main() {
    // 通过 \ + 字符的十六进制表示，转义输出一个字符
    let byte_escape = "I'm writing \x52\x75\x73\x74!";
    println!("What are you doing\x3F (\\x3F means ?) {}", byte_escape);

    // \u 可以输出一个 unicode 字符
    let unicode_codepoint = "\u{211D}";
    let character_name = "\"DOUBLE-STRUCK CAPITAL R\"";

    println!(
        "Unicode character {} (U+211D) is called {}",
        unicode_codepoint, character_name
    );

    // 换行了也会保持之前的字符串格式
    let long_string = "String literals
                        can span multiple lines.
                        The linebreak and indentation here ->\
                        <- can be escaped too!";
    println!("{}", long_string);
}
```

禁止转义

```rust
fn main() {
    println!("{}", "hello \\x52\\x75\\x73\\x74");
    let raw_str = r"Escapes don't work here: \x3F \u{211D}";
    println!("{}", raw_str);

    // 如果字符串包含双引号，可以在开头和结尾加 #
    let quotes = r#"And then I said: "There is no escape!""#;
    println!("{}", quotes);

    // 如果还是有歧义，可以继续增加，没有限制
    let longer_delimiter = r###"A string with "# in it. And even "##!"###;
    println!("{}", longer_delimiter);
}
```


##### 操作UTF-8字符串

chars 依次获取字符串; bytes 得到每一个底层字节数组的值. 而要按照char来获取子串, 标准库中没有, 或许可以用 [utf8\_slice](https://crates.io/crates/utf8_slice).

```rust
for c in "中国人".chars() {}
for b in "中国人".bytes() {
    println!("{}", b);
}
```
