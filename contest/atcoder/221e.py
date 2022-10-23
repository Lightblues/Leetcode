""" 221e 难度 1515
https://atcoder.jp/contests/abc221/tasks/abc221_e

输入 n(≤3e5) 和长为 n 的数组 a (1≤a[i]≤1e9)。
输出有多少个 a 的长度至少为 2 的子序列，满足子序列的第一项 ≤ 子序列的最后一项。
由于答案很大，输出答案模 998244353 的结果。 

注：子序列不要求连续。

https://atcoder.jp/contests/abc221/submissions/35791225

这是一道基于逆序对的变形题。
不了解逆序对的同学，可以先看看我的讲解 https://www.bilibili.com/video/BV1tW4y1e7rb

用树状数组实现，这里的问题是，如何把 2 的幂次（中间的子序列的个数）也考虑进去。
我们可以把 2^(i-j) 转换成 2^i / 2^j，那么把 2^j 的逆元加到树状数组中即可。
注意需要离散化。
代码中展示了一个巧妙计算逆元的技巧。

思路1: 
    对于符合要求的下标对 `(i,j)` (也即, arr[i]<=arr[j]), 其可以组成的满足要求的子序列的数量为 `2^{j-i-1}`.
    顺序遍历, 对于下标i, 如何找到前面有多少 <=arr[i] 的元素? 可以用 #树状数组
    还要知道元素的位置? 我们可以分解 `2^{j-i} = 2^j / 2^i`. 因此, 在树状数组中, 我们还可以记录 `2^i` 的值, 完成累加.
    WA: 一开始没有用 #逆元 直接WA, 应该是 1/2^i 的值太大了, 浮点溢出. 


3
1 2 1
# 3
"""
N = int(input())
if N==0: exit()

arr = list(map(int, input().split()))
s = sorted(set(arr))
smap = {v: i for i, v in enumerate(s, 1)}
arr = [smap[v] for v in arr]

mod = 998244353

# 树状数组框架
tree = [0] * (N + 1)
def lowbit(x):
    return x & (-x)
def add(x, v):
    while x <= N:
        tree[x] += v
        x += lowbit(x)
def query(x):
    res = 0
    while x:
        res += tree[x]
        x -= lowbit(x)
    return res

ans = []
for i,a in enumerate(arr):
    s = query(a) % mod
    if s>0: ans.append(pow(2, i-1, mod) * s)
    else: ans.append(0)
    add(a, 1 / pow(2, i, mod))
print(int(sum(ans)) % mod)
