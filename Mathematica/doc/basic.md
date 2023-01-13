
用法: 

- Shift+Enter 执行
- 选中右侧的范围, Del进行删除
- 选中函数按 F1 查看帮助

## 计算器

```sh
FactorInteger[2^2^5 + 1]
# 取小数点后
N[E, 200]
# 展开
Expand[(a + b)^3]
# 因式分解
Factor[x^3 + y^3 + z^3 - 3 x y z]
# 解方程 (注意, 这里的相等是两个等号, 一个是赋值!)
Solve[x^3 - 2 x - 1 == 0, x]
```



## 高数


```sh
# 求极限
Limit[(Tan[x] - x)/(x - Sin[x]), x -> 0]
# 偏导数
D[x^x, x]
# 积分 (不定)
Integrate[x^2 Cos[x], x]
# 级数求和!!
Sum[x^(2 n)/(n^2 Binomial[2 n, n]), {n, Infinity}]
# 微分方程
FullSimplify[DSolve[y''[x] + y[x] == 8 x Sin[x], y[x], x]]
# 绘图 (手动设置加一些点, 更加平滑)
Plot[Sin[1/x], {x, 0, 1/Pi}, PlotPoints -> 1000]
```


积分

```sh
# 不定积分
函数名[变量名_]:= 函数;
Integrate[函数名[变量名],变量名]
# 
f[x_] := x^2 + Sin[x] + 1;
Integrate[f[x], x]

# 定积分
# 线积分
Integrate[求积函数,{变量范围}]
# 二重积分
Integrate[求积函数,{变量范围},{变量范围}]
# 
Integrate[E^(p*x + q*y), {x, 0, a}, {y, 0, a}]
```

## 绘图

```sh
# 立体图
Plot3D[函数,{变量范围}]
Plot3D[{函数1,函数2},{变量范围}]
```


