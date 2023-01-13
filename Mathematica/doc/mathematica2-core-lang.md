
## 语言概述

Mathematica 的核心语言与 C 语言的本质区别在于它们的范式：C 语言是命令式的，或者说 **面向过程** 的；而 Mathematica 是 **函数式** 的。它们之间的区别比 C 和 C++、Java 等 **面向对象语言** 之间的区别还要大。按照范式分类的话， Mathematica 更像 Lisp、Haskell 和 OCaml 等语言。

### 历史与联系

Wolfram 原本是学理论物理的，在他的研究中需要做很多复杂的计算。最初是手算，后来开始用计算机。在当时，只有一款计算机代数系统可用，这就是由 MIT 计算机科学与人工智能实验室开发的 Macsyma（Project MAC's SYmbolic MAnipulator，简称 Macsyma）。Wolfram 对 Macsyma 并不满意 ，所以用了几年之后，他开始开发自己的计算机代数系统，这就是后来的 Mathematica。

Mathematica 是用 C 语言编写的，所以运算符的使用习惯、以及条件、循环等控制结构的名字都与 C 语言很像。

Macsyma 是用 MAC Lisp 实现的，要用它实现一些复杂的计算必须深入到它的源程序中，所以不懂 Lisp 语言是不行的。 Wolfram 因此受到 Lisp 的很多影响，Mathematica 的核心语言中与 Lisp 相似的部分就由此而来。

### Lisp 与 Mathematica

Lisp（LISt Processing，简称 Lisp）是第二古老的高级程序语言（最老的是 Fortran，仅比 Lisp 大一岁），它由 John McCarthy 于 1958 年发明。
（Steve Jobs，2011年10月5日逝世；Dennis Ritchie，2011年10月12日逝世；John McCarthy，2011年10月24日逝世。）

Lisp 的含义是"表处理"，所谓"表"，就是形如 `(item1 item2 item3)` 的一个对象，它也叫做 S-表达式（S-expression，Symbolic expression 的简称）。

Lisp 源程序由一系列这样的表嵌套而成：`(item1 (item2 ((item3 item4 item5) item6) (item7 item8)))` 

一个 Lisp 解释器的目标就是求出传递给它的 S-表达式的值。求值的规则是，每个表的第一个条目被认为是函数名，其它条目则被认为是这个函数的自变量。例如，表 (+ 2 2) 的值是 2+2=4，而表 `(+ (+ 2 2) (* 3 5))` 的值是 (2+2)+(3*5)=19。

Lisp 的这种运算表示法叫做 **波兰前缀记法**，是波兰数学家 Jan Łukasiewicz 发明的。这种记法多多少少有些反人类，但是却非常便于计算机处理。

事实上，这样的表达式很容易通过图论中"树"的概念来表达：函数即节点，自变量即分支。

在编译原理中，编译的第一步是将源程序转化为 **抽象语法树**（Abstract Syntax Tree，简称 AST）。Lisp 的这种语法可以认为是在直接书写语法树。

在 Mathematica 中，我们可以用 TreeForm 来获得一个表达式的语法树。

```sh
# 用 TreeForm 来获得一个表达式的语法树
TreeForm[(a + b^n)/z == x]

# 可以用 FullForm 来获得一个表达式在 Mathematica 内部的完整形式
FullForm[(a + b^n)/z == x]
# Equal[Times[Plus[a, Power[b,n]], Power[z,-1]], x]]
# Lisp 中的表达就是 `(= (* (+ a (expt b n)) (expt z -1)) x)`
```

## Mathematica 基本原理

### 第一原理：万物皆表（达式）

在 Mathematica 中，满足如下条件的对象就叫做表达式（expression）：(递归定义)

- 原子对象是表达式；
- 若 F、X1、X2、...、Xn 是表达式，则 F[X1, X2, ..., Xn] 也是表达式。
    - 注意, F不仅可以是一个函数, 可以是任意的表达式, 例如 `(1+2x)[2]`; 这里的 1+2x 可能没啥意义, 但可以通过 TreeForm 画出来, 就是一个图上的节点!

Mathematica 第一原理：**万物皆表（达式）**。

```sh
(* 常见运算符的完整形式 *)
FullForm /@ {a + b, a - b, a*b, a/b, a^b, a == b, a != b, a < b, 
  a <= b, a > b, a >= b, a && b, a || b} 

# 利用 TraditionalForm 得到符号的表达式 (更像论文里面的符号表达)
ForAll[\[Epsilon], \[Epsilon] > 0, 
  Exists[\[Delta], \[Delta] > 0, 
   ForAll[x, Abs[x - Subscript[x, 0]] < \[Delta], 
    Abs[f[x] - f[Subscript[x, 0]]] < \[Epsilon]]]] // TraditionalForm
```

### 第二原理：计算即重写

第一原理关注的仅仅是被计算对象的表示法，它尚未涉及计算本身。Lisp 并不擅长计算，我想这也是 Wolfram 对 Macsyma 和 Lisp 不满意的原因。Mathematica 的计算思想来自于其它 **函数式语言**，如 Haskell、OCaml 等等。要理解这种思想，我们先回忆一下人类是如何计算的。

```sh
# Trace 追踪计算过程
# 语句的目的是计算不定积分 Integrate[Sin[x]^2, x]; 然后代入 {0, 2 Pi} 的值减一下 (定积分) 
# 就是用牛顿莱布尼兹公式求定积分
Trace[(#2 - #1) & @@ (Integrate[Sin[x]^2, x] /. {x -> #} & /@ {0, 2 Pi})]
```

仔细分析这个过程可以发现，在每一步里我们做的其实都是下面这两件事：

- 从待计算对象中识别一些可化简的模式
- 将识别出的模式用已知的规则进行化简

Mathematica 也是这样进行计算的，其中第一步叫做 **模式匹配**，第二步叫做 **规则代入**。基于模式和规则的计算模型在数理逻辑或者计算机科学中叫 **重写系统**（rewriting system）。

Mathematica 第二原理：**计算即重写**。

### 函数式语言

[类比数学中的集合论、范畴论]

Lisp 没有重写系统、Haskell、OCaml 不符合万物皆表，但是人们还是将它们归为一类，称为函数式语言。这是因为这些语言拥有一个共同的原理，那就是把函数视为最基本的、可操作的对象。

在 `Lisp` 中，我们可以通过在一个表前加 "'" 标记的办法来制止 Lisp 解释器对它求值，这样被制止了的表被认为是某种可操作的数据。当我们将一些数据组合成一个表 L 之后，可以通过 (eval L) 强制性地求 L 的值，此时数据 L 被转化成了可执行的代码。"**代码即数据（Code-as-Data）**" 被称为 Lisp 的哲学。

在 `Haskell` 中，每种类型可以视为一个集合，类型之间的函数则成为集合间的映射。映射 `f: X->Y` 和 `g: Y->Z` 的复合 `g.f: X->Z` 可以很容易地通过 Haskell 的"."运算符得到。注意从集合 Y 到集合 Z 的映射全体 Z^Y 也是一个集合，这个集合在 Haskell 语言中自动定义了一个新的类型。于是任何二元函数 `f: X*Y->Z` 都可视为一个从 X 到 Z^Y 的一元函数，记为 `f: X->(Y->Z)`，这种对应被称为函数的 currying。
（Haskell和Curry分别是数理逻辑学家Haskell Brooks Curry的名和姓，事实上还有两个编程语言分别叫Brook和Curry。）
[罗素类型论, 在数学上没有发展, 计算机中发展]

### 第零原理：重要的是函数，而非变量

在 Mathematica 中既可以实现"代码即数据"这种 Lisp 哲学，也可以实现复合和 currying 等函数上的运算，所以人们才将它与 Lisp、Haskell 等语言归在一类。Mathematica 的这一特征是如此重要，以至于我们要将它总结为第零原理。

Mathematica 第零原理：**重要的是函数，而非变量**。

### 模块化

Mathematica 核心语言中还有关于模块化编程的一些内容。这些内容并非某种原理，而是为了构建大型程序而不得不从其它语言中引入的特性：模块与作用域的概念广泛存在于各种程序语言中；而Mathematica 的"语境（context）"概念非常像 C++ 中的"命名空间（namespace）"。

以上就是 Mathematica 核心语言的主要内容：表达式、重写系统、泛函(函数式)编程和模块化。这也将是我们在本课程中学到的东西。

## 表达式与表

根据定义，一个表达式或者是原子，或者是形如 F[X1, X2, \[Ellipsis], Xn] 的函数。事实上，原子也可以看成后者的特殊情况，只要我们把函数的自变量个数取成零就行了。所以，以后我们讨论表达式的时候，总把它写成 F[X1, X2, \[Ellipsis], Xn] 的样子。

### 表达式 (Head) 与 `Map`

给定一个表达式 F[X1, X2, \[Ellipsis], Xn]，我们称 F 是它的"头"。

```sh
Head /@ {1, 1/2, True, "number", a + b, a - b, a*b, a/b, (f + g)[x1, x2, x3]}
# 两种写法等价
h /@ k[x1, x2, x3]
Map[h, k[x1, x2, x3]]
```

（运算符 `/@` 的全名叫 `Map`，是最常用的泛函运算之一。用它可以方便地测试一个函数在一组变量上的作用效果，而不必把这个函数名写很多次。）

我们发现对于原子表达式：符号的头总是 Symbol；数字的头则依赖于它的类型，结果可以是 Integer、Rational、Real 和 Complex；字符串的头总是 String；图片的头是 Image 等等。

利用这个性质，我们可以判断一个表达式是否是原子。

```sh
# 判断是否为原子表达式. 我们的函数 myAtomQ 与系统内建函数 AtomQ 有差不多的功能。
myAtomQ = 
  Function[ex, 
   MemberQ[{Symbol, Integer, Rational, Reals, Complex, String, Image},
     Head[ex]]];
```

### 表 (List) 与 Apply

除了头以外，我们也常常需要将表达式的参数部分取出来。取出来的东西是一些表达式构成的序列，是没有头的。但是在 Mathematica 里所有的表达式都必须有头，所以，为了处理这种无头表达式，Mathematica 引入 **表**（List）这个概念，然后规定所有的无头表达式的头都是 List。

```sh
ex = f[x1, x2, x3];
# 两种写法等价
List @@ ex;
Apply[List, ex]
```

表达式 X1, X2,\[Ellipsis], Xn 构成的表记为 `{X1, X2,\[Ellipsis], Xn}`。
`List` 本身也是 Mathematica 的一个内部函数，它的作用是将输入的表达式序列做成一个表。

```sh
List[1, 2, 3]
```

让我们再回到表达式 F[X1, X2, \[Ellipsis], Xn] 。现在我们知道，它的头以外的部分可以用 List[X1, X2,\[Ellipsis], Xn] 来表示。所以这样一个操作可以简单地认为是将原表达式的头 F 换成了系统内建符号 List。

换头术也是 Mathematica 中最常用的泛函运算之一，它的全名叫 `Apply`，简写形式为 `@@`。

### 序列 (Sequence)

表这种表达式还有一种变体，叫做序列（Sequence）。序列可以认为是没有两边花括号（"{"和"}"）的表，或者说，表是用序列的元素做成了一个新的对象，而序列是某种更原始的东西。

### Part

[这里可以画出表达式的树结构TreeForm来比较]

除了用 Head 和 Apply 以外，Mathematica 还提供了另一种访问复合表达式内部表达式的方法，即系统内建函数 Part，简写形式为 [[\[Ellipsis]]]。
[类似Python的数组访问]

```sh
ex[[-1, -2, -1]]
ex[[{2, 3}]]
ex[[1 ;; 2]]
# 取 1...3, 间隔为2
ex[[1 ;; 3 ;; 2]]
```

还有一些更集中的操作

```sh
# Rest, Most 分别去掉List的第一/最后一项
Function[op, op[f[x1, x2, x3, x4]]] /@ {First, Last, Rest, Most}
Take[f[x1, x2, x3, x4], {2, 3}]
# 从List中去掉所选元素, 保留剩余部分
Drop[f[x1, x2, x3, x4], {2, 3}]
```

表达式的两个值: 长度和深度

```sh
# 长度, 第一层的分支数量
Length[f[g[x1, h[x2, x3]], x4]]
# 最深的深度
Depth[f[g[x1, h[x2, x3]], x4]]
```

### 表的构造

- Range 
- Table
- Array 
- Tuple 
- Outer 外积

```sh
# Range
Range[10]
Range[2, 10]
Range[2, 10, 3]

# Table (查看帮助语法), 可以构造二维的表
Table[i^2 + i + 1, {i, 10}]
Table[KroneckerDelta[i, j - 1] + t KroneckerDelta[i, j + 4], {i, 
   5}, {j, 5}] // MatrixForm
# MatrixForm 可视化查看 (但不能参与运算)

# Array, 注意这里匿名函数的写法
Array[#^2 + # + 1 &, 10]
#^2 + # + 1 & /@ Range[10]

# 类似对于一个List执行乘方操作
Tuples[Range[3], 3]
# 外积. 将两个List组合起来作为f的内容
Outer[f, Range[3], Range[2]] // MatrixForm
```

### 查询和搜索

- MemberQ
- FreeQ
- Position
- Select

### 添加、删除和修改

- 插入
    - 生成新的表达式 
    - Prepend 加在前面, Append 追加, Insert 指定位置插入
    - 原地操作
    - PrependTo, AppendTo
- 删除
    - Delete
- 修改
    - ReplacePart 替换部分
    - (注意会修改原来的List) 可以直接赋值修改: `ex[[1]] = y; ex`
- 排序操作
    - Reverse 反向排序; RotateLeft 向左轮转; RotateRight 向右轮转

### 头部一样的表达式之间的集合运算

- Join
- Union 并集
- Intersection 交集
- Complement 补集

```sh
Union[f[x1, x2], f[x1, x3]]
# 也可以直接对 List 进行去重
Union[{1, 2, 2, 2, 3, 3, 1, 4, 4, 2, 5, 6, 7, 0}]
```

### 排序

- Sort 排序
- Ordering 排序索引
- 

```sh
# 生成 (20,2) 的列表
list = Array[RandomInteger[10] &, {20, 2}]
# 默认字典序
Sort[list]

# 自定义排序规则
Sort[list, Function[{list1, list2}, list1[[1]] < list2[[1]]]]
Sort[list, #1[[1]] < #2[[1]] &]

Sort[list, (#1[[1]] < #2[[
      1]]) || (#1[[1]] == #2[[1]] && #1[[2]] > #2[[2]]) &]
```

```sh
Sort[list]
Ordering[list]
# 等价于排序
list[[Ordering[list]]]
```


