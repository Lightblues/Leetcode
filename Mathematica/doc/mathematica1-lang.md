
## 值、变量、类型

以下三种对象称为原子（atom）：

- 符号（Symbol）：由字母和数字（数字不能在起始位置）构成的有限序列
- 数字（Number）：整数、有理数、实数、复数
- 字符串（String）：由双引号" "括起来的任意字符构成的有限序列

系统符号

- 由第一个字母大写的单词组成（Camel命名法）：True、False、FactorInteger、SetAttributes
- 用来做判断的函数末尾通常有"Q"：EvenQ、PrimeQ、MatchQ
- 用人名命名的符号=人名+符号名：EulerGamma、BesselJ、DiracDelta

我们命名自定义符号时，应当避开系统内建符号。一种比较好的做法是，在命名自定义符号时将首字母取为小写字母（camel命名法）。

类型检察

```sh
# 这里写成 "0" 会报错
Plot[Sin[x], {x, 0, 2 Pi}]

# 但这里不会, 保留原字符
Sin["I'm a string!"]
# 可以进行替换得到一个数值!!
Sin["I'm a string!"] /. {"I'm a string!" -> Pi/3}
```

## 条件、循环、子程序

在 C 或者 Pascal 这种面向过程的结构化程序语言中，条件、循环和子程序是最基本的三种结构。有了这三种结构就可以实现一切算法。但是，在 Mathematica 程序中，条件和循环结构其实用得并不多。这是因为条件结构的功能基本上可以通过核心语言中的模式匹配来完成；而循环结构的功能则可以通过表处理和泛函编程完成。等读者熟悉这些核心语言的概念之后，会发现它们比条件和循环结构更灵活、更强大、并且更快。在本节中，为了让熟悉 C 语言的读者比较快地上手，我们简单地介绍一下 Mathematica 中的这些结构。

```sh
# 可以省略后面的语法
If[True, Print["Then"]]
If[False, Print["Then"], Print["Else"]]
# a,b 没有赋值, 无法判断!!
If[a == b, Print["Then"], Print["Else"], Print["Unevaluated"]]
# 可以看表面上的判断!! ===
If[a === b, Print["Then"], Print["Else"], Print["Unevaluated"]]

# 还有多重条件判断
Which[x == 1, 1, x == 2, 2, x == 3, 3, True, Print["x!=1,2,3"]]
# Piecewise 可以进行分段函数, 类似 Which
Plot[Piecewise[{{1, x == 0}, {Sin[x]/x, x != 0}}], {x, -4 Pi, 4 Pi}]

# Switch 语法!
Switch[b, True, 1, False, 0, _, Print["b is not a boolean value!"]]
```

循环

```sh
# Do[expr,n]
Do[Print["哟，"], {3}]; Print["切克闹！"]
# Do[expr, {i, i_max}], 这里没有min, 默认就是从1开始
# Do[expr, {i, i_min, i_max}]
Do[Print[Prime[i]], {i, PrimePi[100]}]
# Do[expr,{i,{i_1, i_2,...}}] 
Do[Print[i, " is a prime number."], {i, {2, 3, 5, 7, 11}}]

# 复杂循环. 
# For. 注意标点符号和 C语言不一样!!
# For[start,test,incr,body]
For[i = 1; t = i, i <= 10, i++, Print[t *= i]]
# While 语法
# While[test,body]
n = 1; While[n < 4, Print[n]; n++]
# 精简, 不加第二个表达式
n = 1234567; While[Not[PrimeQ[++n]]]; n
# 也可以写成下面的形式. 通过Do循环找到, 利用 Throw, Catch 抓取到结果. 
n = 1234567; Catch[Do[If[PrimeQ[i], Throw[i]], {i, n, 2 n}]]
# Catch[expr]
# Catch[expr,form]
```

不推荐使用的：Break、Continue、Return、Goto。

## 函数

两种函数定义, 建议初学者使用方法二的完整形式，因为比较简单易懂。

```sh
# 函数定义方法一：模式匹配+延迟赋值
f[x_] := x^2;
f[x_, y_] := x y;

# 函数定义方法二：纯函数（\[Lambda]-表达式、匿名函数）
f1 = Function[x, x^2];(* 完整形式 *)
f2 = #^2 &; (* 简写形式 *)

g1 = Function[{x, y}, x y];
g2 = #1 #2 &;
```

一个现在比较难看懂的例子

```sh
# 例子：求不大于给定正整数 n 的所有素数的和
(*******类C实现*******)
myPrimeQ = Function[x, i = 2; max = Floor[Sqrt[x]] + 1;
   While[Mod[x, i] != 0 && i < max, i++]; Not[i < max]];

myPrimeSum = Function[n,
   sum = 0; Do[If[myPrimeQ[x], sum += x], {x, 2, n}]; sum];

(*******核心语言实现*******)
(* 为什么这个方法快？因为Mathematica内部储存着前10亿个素数的素数表 *)
myPrimeSum2 = Plus @@ Prime /@ Range@PrimePi[#] &;

(* 比较一下两者的运行时间 *)
Timing[#[100000]] & /@ {myPrimeSum, myPrimeSum2}
```

