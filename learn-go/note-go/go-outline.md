# Go语言大纲

TODO

- [ ] Constructor
- [ ] 接口
- [ ] 类型转换

资源

- doc <https://go.dev/doc/>
    - 中文 <https://go-zh.org/>
    - <https://go.dev/doc/tutorial/getting-started> 提到了如何导入外部的包, 例如在代码中用到了 `import "rsc.io/quote"`, 只要运行 `go mod tidy` 就会分析代码, 然后下载检索到的包, 默认下载为 `~/go/pkg/mod/`.
- [Go语言101](https://gfw.go101.org/article/101.html) 比较体系的一份教材, 有 GitHub 地址 <https://github.com/golang101/golang101>
- [骏马金龙 | Go语言系列文章](https://www.cnblogs.com/f-ck-need-u/p/9832538.html)

- <https://go-zh.org/pkg/builtin/> builtin 基本的类型和函数等
- TODO
    - 看 slice 的一些性质; int 等类型.
    - 单元测试 testing 包
    - 包索引/导入方式

## 简明教程

from <https://go-zh.org/>

### 基本

```go
var c, python, java bool //变量声明
var i, j int = 1, 2 //初始化
// 类型转换
var x, y int = 3, 4
var f float64 = math.Sqrt(float64(x*x + y*y))
var z uint = uint(f)
// 类型推导
v := 42.5 // 修改这里！
fmt.Printf("v is of type %T\n", v)
// 常量
const Pi = 3.14
```

### 流程控制

- for
    - 和 C、Java、JavaScript 之类的语言不同，Go 的 for 语句后面的三个构成部分外没有小括号， 大括号 { } 则是必须的。
    - 初始化语句和后置语句是可选的。此时你可以去掉分号，因为 C 的 while 在 Go 中叫做 for。
    - 如果省略循环条件，该循环就不会结束
- 同 for 一样， if 语句可以在条件表达式前执行一个简单的语句。
    - 该语句声明的变量作用域仅在 if 之内。。

### 更多类型

- 指针
    - 类型 *T 是指向 T 类型值的指针。其零值为 nil。
    - `&` 操作符会生成一个指向其操作数的指针。
    - `*` 操作符表示指针指向的底层值。
- 结构体
    - 一个结构体（struct）就是一组字段（field）。
    - 结构体字段可以通过结构体指针来访问。
    - 如果我们有一个指向结构体的指针 p，那么可以通过 `(*p).X` 来访问其字段 X。不过这么写太啰嗦了，所以语言也允许我们使用隐式间接引用，直接写 `p.X` 就可以。
- 数组
    - 类型 `[n]T` 表示拥有 n 个 T 类型的值的数组。
    - `var a [10]int` 数组的长度是其类型的一部分，因此数组不能改变大小。
- 切片
    - 每个数组的大小都是固定的。而切片则为数组元素提供动态大小的、灵活的视角。
    - 类型 `[]T` 表示一个元素类型为 T 的切片。
    - 切片就像数组的引用
    - 切片拥有 长度 和 容量。可通过表达式 `len(s)` 和 `cap(s)` 来获取
    - 切片的零值是 `nil`。nil 切片的长度和容量为 0 且没有底层数组。
    - 切片可以用内建函数 `make` 来创建，这也是你创建动态数组的方式。
        - make 函数会分配一个元素为零值的数组并返回一个引用了它的切片
    - 向切片增加元素: `func append(s []T, vs ...T) []T`
- 切片的切片
    - 切片可包含任何类型，甚至包括其它的切片。 `board := [][]string{}`
- range
    - for 循环的 `range` 形式可遍历切片或映射。
    - 返回两个值, 第一个值为当前元素的下标，第二个值为该下标所对应元素的一份副本。
    - 可以将下标或值赋予 _ 来忽略它。

```go
// point
i, j := 42, 2701

p := &i         // 指向 i
fmt.Println(*p) // 通过指针读取 i 的值
*p = 21         // 通过指针设置 i 的值
fmt.Println(i)  // 查看 i 的值

p = &j         // 指向 j
*p = *p / 37   // 通过指针对 j 进行除法运算
fmt.Println(j) // 查看 j 的值

// 结构体
type Vertex struct {
  X int
  Y int
}
v := Vertex{1, 2}
v.X = 4
fmt.Println(v.X)

v1 = Vertex{1, 2}  // 创建一个 Vertex 类型的结构体
v2 = Vertex{X: 1}  // Y:0 被隐式地赋予
v3 = Vertex{}      // X:0 Y:0
p  = &Vertex{1, 2} // 创建一个 *Vertex 类型的结构体（指针）

// 数组
var a [2]string
a[0] = "Hello"
a[1] = "World"
fmt.Println(a[0], a[1])
fmt.Println(a)

primes := [6]int{2, 3, 5, 7, 11, 13}
fmt.Println(primes)

// 切片
q := []int{2, 3, 5, 7, 11, 13}
fmt.Println(q)

r := []bool{true, false, true, true, false, true}
fmt.Println(r)

s := []struct {
  i int
  b bool
}{
  {2, true},
  {3, false},
  {5, true},
  {7, true},
  {11, false},
  {13, true},
}
fmt.Println(s)
// make
a := make([]int, 5)  // len(a)=5
b := make([]int, 0, 5) // len(b)=0, cap(b)=5
b = b[:cap(b)] // len(b)=5, cap(b)=5
b = b[1:]      // len(b)=4, cap(b)=4

// 切片的切片
board := [][]string{
  []string{"_", "_", "_"},
  []string{"_", "_", "_"},
  []string{"_", "_", "_"},
}

// range
pow := make([]int, 10)
for i := range pow {
  pow[i] = 1 << uint(i) // == 2**i
}
for _, value := range pow {
  fmt.Printf("%d\n", value)
}
```

#### map

- 映射 map
    - 映射的零值为 nil 。nil 映射既没有键，也不能添加键。
    - make 函数会返回给定类型的映射，并将其初始化备用。
    - 映射的文法与结构体相似，不过必须有键名。
    - 若顶级类型只是一个类型名，你可以在文法的元素中省略它 (见下面的代码)
    - 修改映射
        - 插入或修改元素：`m[key] = elem`
        - 删除元素： `delete(m, key)`
        - 通过双赋值检测某个键是否存在：`elem, ok = m[key]`
            - 若 key 不在映射中，那么 elem 是该映射元素类型的零值。
            - 同样的，**当从映射中读取某个不存在的键时，结果是映射的元素类型的零值**。

```go
// map[type]type
type Vertex struct {
  Lat, Long float64
}
var m map[string]Vertex
m = make(map[string]Vertex)
m["Bell Labs"] = Vertex{
  40.68433, -74.39967,
}
fmt.Println(m["Bell Labs"])
// 若顶级类型只是一个类型名，你可以在文法的元素中省略它
type Vertex struct {
 Lat, Long float64
}
var m = map[string]Vertex{
 "Bell Labs": Vertex{
  40.68433, -74.39967,
 },
 "Google": Vertex{
  37.42202, -122.08408,
 },
} // 简写
var m = map[string]Vertex{
 "Bell Labs": {40.68433, -74.39967},
 "Google":    {37.42202, -122.08408},
}
 m := make(map[string]int)

 m["Answer"] = 42
 fmt.Println("The value:", m["Answer"])

 m["Answer"] = 48
 fmt.Println("The value:", m["Answer"])

 delete(m, "Answer")
 fmt.Println("The value:", m["Answer"])

 v, ok := m["Answer"]
 fmt.Println("The value:", v, "Present?", ok)
```

#### 函数值, 闭包

- 函数值
    - 函数也是值。它们可以像其它值一样传递。
    - 函数值可以用作函数的参数或返回值。
- 函数的闭包
    - 闭包是一个函数值，它引用了其函数体之外的变量。该函数可以访问并赋予其引用的变量的值，换句话说，**该函数被这些变量“绑定”在一起**。
    - 示例如下

```go
// 函数值
func compute(fn func(float64, float64) float64) float64 {
 return fn(3, 4)
}
hypot := func(x, y float64) float64 {
  return math.Sqrt(x*x + y*y)
}
fmt.Println(hypot(5, 12))

fmt.Println(compute(hypot))
fmt.Println(compute(math.Pow))

// 闭包
// 函数 adder 返回一个闭包。每个闭包都被绑定在其各自的 sum 变量上。
func adder() func(int) int {
 sum := 0
 return func(x int) int {
  sum += x
  return sum
 }
}
pos, neg := adder(), adder()
for i := 0; i < 10; i++ {
  fmt.Println(
    pos(i),
    neg(-2*i),
  )
}

// 例子 斐波纳契闭包 `(0, 1, 1, 2, 3, 5, ...)`。
// 注意这里要返回从 0 开始的, 一开始想了好久没想到可以这么简单
// fibonacci is a function that returns
// a function that returns an int.
func fibonacci() func() int {
 f, g := 1, 0
 return func() int {
  f, g = g, f+g
  return f
 }
}
f := fibonacci()
for i := 0; i < 10; i++ {
  fmt.Println(f())
}

```
