""" 韭菜的季节
数值求解积分
$$
\begin{aligned}
& P(a \leq X \leq b)=\int_a^b \sin (\sqrt{x}) / 5.68 d x \approx \\
& \sum_{i=0}^{n-1} \sin \left(\sqrt{x_i}\right) / 5.68 \Delta x \\
& \text { 其中 } a=x_0<x_1<\cdots<x_n=b, \text { and } x_{i+1}-x_i= \\
& \Delta x \text {. 取 } n=500, \text { 相当于把区间 }[\mathrm{a}, \mathrm{b}] \text { 分成500份。 }
\end{aligned}
$$

思路1: 按照题目的定义 #模拟 #积分
    对于 a=x0, ..., xn=b 分割成 n==500份, 
    求和 sum{ sin(sqrt(xi)) / 4.68 * delta }
"""
import math
N = 500

def f(a,b):
    delta = (b-a)/N
    s = 0
    for i in range(N):
        xi = a + i*delta
        s += math.sin(math.sqrt(xi)) / 5.68 * delta
    return 1 if s>0.5 else 0

n = int(input())
for _ in range(n):
    a,b = map(int, input().split())
    print(f(a,b))
