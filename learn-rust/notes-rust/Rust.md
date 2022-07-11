
- official: <https://www.rust-lang.org/>
    - repo: <https://github.com/rust-lang/rust>
    - 文档: [《The Rust Programming Language》](https://doc.rust-lang.org/book/), [repo](https://github.com/rust-lang/book) (`rustup doc` 本地打开), 有 [中文版](https://kaisery.github.io/trpl-zh-cn/).
- Rust语言圣经(Rust Course): <https://course.rs/about-book.html> (⭐️)
    - [repo](https://github.com/sunface/rust-course)
    - 配套练习题: <https://zh.practice.rs/>; [repo](https://github.com/sunface/rust-by-practice); [solutions](https://github.com/sunface/rust-by-practice/tree/master/solutions)
- Rusty Book(锈书): <https://rusty.rs/about.html>.
    - awesome+cookbook, [repo](https://github.com/rustlang-cn/rusty-book)

## 安装与配置

```sh

# 启动本地文档
rustup doc


# 安装 Linux, macOS 通用
curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
rustup self uninstall   # 卸载
```

VSCode

- 插件
    - `rust-analyzer` 社区驱动替代了官方的支持插件
    - `CodeLLDB`, Debugger 程序
    - `Even Better TOML`，支持 .toml 文件完整特性
    - `Error Lens`, 更好的获得错误展示

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

