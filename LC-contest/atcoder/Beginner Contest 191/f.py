""" F - GCD or MIN 
给定n个数字, 每次操作可以选其中两个数组, 然后用 gcd(i,j) 或 min(i,j) 进行替换. 问进行 n-1 操作后剩余的那个数字有多少种可能.
限制: n 2000; 数组范围 C 1e9
提示: 问题等价于, 找到小于等于 mn = min(nums) 的, nums子序列的最大公因数.
    这是因为: 1) 最终结果必然小于等于最小值, 并且一定是某一子序列的 #公因子; 2) 并且我们可以构造操作序列得到该数
思路0: 参考「1819. 序列中不同最大公约数的数目」, 遍历 1...mn, 然后检查是否满足. 这样遍历的复杂度就是 O(C) 了肯定超时
    改进: 先找出所有的公因子, 然后依次判断; 也 TLE 了
思路0.2: 对于每一个数字, 找出其所有的因子, 然后判断该因子是否成立
    如何判断因子g是否可以取到? 遍历nums, 对于其中所有g的倍数取gcd, 若可以得到g则成立.
    超时了, 复杂度分析略. 超时的例子是 `many_divisors`.
思路1: 我们用一个哈希表 t 来存储当前存在的因子. 
    遍历nums, 对于每一个因子g, {g: minPoss} 来记录遍历nums中g的倍数的过程中, 通过计算gcd可以可到的最小值.
    遍历结束后, 统计哈希表中 g==minPoss 的个数即可.
    复杂度: 遍历nums O(n); 每个数的因子最多为 O(d(C)); 每次计算gcd O(logC); 因此总体复杂度 `O(n d(c) log(c))`. 这里的d函数表示小于C的数字中最多的因子数. 已知 `d(10^9)=1344`
    见 [官答](https://atcoder.jp/contests/abc191/editorial/727)

"""
from math import gcd, sqrt
from functools import lru_cache
n = int(input())
nums = set(map(int, input().split()))
mn = min(nums); mx = max(nums)
# ans = 0
t = {}
for num in nums:
    for i in range(1, min(mn+1, int(sqrt(num))+1)):
        if num%i != 0: continue
        if i in t: t[i] = gcd(t[i], num)
        else: t[i] = num
        j = num//i
        if j <= mn:
            if j in t: t[j] = gcd(t[j], num)
            else: t[j] = num
print(sum(1 for k,v in t.items() if v == k))

def f0():
    # 参考了 「1819. 序列中不同最大公约数的数目」 对于可能的结果进行计算, 因为数字范围太大, 不可行
    for g in range(1, mn+1):
        gg = None
        for y in range(g, mx+1, g):
            if y in nums:
                if gg is None: gg = y
                else: gg = gcd(gg, y)
                if gg == g:
                    ans += 1
                    break
def f01():
    poss = set()
    for num in nums:
        for i in range(1, min(mn+1, int(sqrt(num)))+1):
            if num % i == 0:
                poss.add(i)
                if num//i <= mn:
                    poss.add(num//i)
    for g in poss:
        gg = None
        for y in nums:
            if y % g == 0:
                if gg is None: gg = y
                else: gg = gcd(gg, y)
            if gg == g:
                ans += 1
                break

def f02():
    # 超时了 https://atcoder.jp/contests/abc191/submissions/33281826
    # 在因此很多的情况下
    @lru_cache(maxsize=None)
    def test(g):
        gg = None
        for a in nums:
            if a%g==0:
                if gg is None: gg = a
                else: gg = gcd(gg, a)
                if gg == g: return True
        return False
    ans = set()
    for num in nums:
        for g in range(1, min(mn+1, int(sqrt(num)))+1):
            if num % g == 0:
                if g not in ans and test(g):
                    ans.add(g)
                if num//g <= mn and num//g not in ans and test(num//g):
                    ans.add(num//g)

    print(len(ans))
