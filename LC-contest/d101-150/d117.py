from easonsi.util.leetcode import *

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
https://leetcode-cn.com/contest/biweekly-contest-117
T3经典! 居然出了两道可以用「容斥原理」的题目, 不错子. 

Easonsi @2023 """
class Solution:
    """ 2929. 给小朋友们分糖果 II #medium 将n个糖果分给3个人, 要求每个人不超过limit. 问有多少种方法. #题型
限制: n 1e6
思路1: 
    考虑分给两个人的子问题. 
    例如limit=2时, 当 n=0,1,2,3,4 时候, 分别有 1,2,3,2,1 种方法.
思路2: #容斥原理
参见[灵神](https://leetcode.cn/problems/distribute-candies-among-children-ii/solutions/2522969/o1-rong-chi-yuan-li-pythonjavacgo-by-end-2woj/)
 """
    def distributeCandies(self, n: int, limit: int) -> int:
        if n > 3*limit: return 0
        bc_min = max(0, n-limit)
        bc_max = min(limit*2, n)
        if bc_min <= limit <= bc_max:
            return (bc_min+1+limit+1) * (limit-bc_min+1) // 2 + (limit+(limit+1-(bc_max-limit))) * (bc_max-limit) // 2
        else:
            if bc_max > limit:
                bc_max, bc_min = 2*limit-bc_min, 2*limit-bc_max
            return (bc_max+1+bc_min+1) * (bc_max-bc_min+1) // 2

    """ 2930. 重新排列后包含指定子字符串的字符串数目 #medium #题型 重排后, 包括 leet 子串的数量.
限制: n 1e5
思路1: #容斥原理 
    「正难则反」, 考虑「不满足」的情况. 则有三种情况 1] 不含 l; 2] 不含 t; 3] 不含或者只有一个 e. (或的关系)
    至少一个条件: 情况 1/2] 都是 25^n; 对于情况 3], 有 25^n + n*25^{n-1} 种情况.
        当包括了重复计数!
    至少两个条件: 同时不满足1+2] 则有 24^n; 不满足3+1/2] 均为 24^n + n*24^{n-1}
    至少三个条件: 23^n + n*23^{n-1}
    因此, 「不满足」的情况有 3*25^n + n*25^{n-1} - 3*24^n - 2*n*24^{n-1} + 23^n + n*23^{n-1}
    原始答案, 在用 26^n 减去即可
思路2: 记忆化搜索
    记 f[i, l,t,e] 为 i个字符串, 包括 l,t,e 个 'l/t/e' 字符的数量
    f[i, l,t,e] = f[i-1, 0,t,e] + f[i-1, l,0,e] + f[i-1, l,t,max(e-1,0)] + f[i-1, l,t,e] * 23
[](https://leetcode.cn/problems/number-of-strings-which-can-be-rearranged-to-contain-substring/solutions/2522964/olog-n-rong-chi-yuan-li-fu-ji-yi-hua-sou-okjf/)
 """
    def stringCount(self, n: int) -> int:
        # if n<4: return 0
        MOD = 10**9+7
        return (pow(26, n, MOD)
              - pow(25, n - 1, MOD) * (75 + n)
              + pow(24, n - 1, MOD) * (72 + n * 2)
              - pow(23, n - 1, MOD) * (23 + n)) % MOD


    def stringCount(self, n: int) -> int:
        from functools import lru_cache
        @lru_cache(None)
        def dfs(i: int, l: int, t: int, e: int) -> int:
            """ i个字符, 包括 l,t,e 个 'l/t/e' 字符的数量 """
            if i == 0:
                return 1 if l == t == e == 0 else 0
            res = dfs(i - 1, 0, t, e)
            res += dfs(i - 1, l, 0, e)
            res += dfs(i - 1, l, t, max(e - 1, 0))
            res += dfs(i - 1, l, t, e) * 23
            return res % (10 ** 9 + 7)
        return dfs(n, 1, 1, 2)


    """ 2931. 购买物品的最大开销 #hard 太简单了
 """
    def maxSpending(self, values: List[List[int]]) -> int:
        vals = sorted(itertools.chain(*values))
        days = range(1, len(vals)+1)
        return sum(v*d for v,d in zip(vals, days))

sol = Solution()
result = [
    # sol.distributeCandies(n = 5, limit = 2),
    # sol.distributeCandies(3,3),
    # sol.distributeCandies(2,1),
    # sol.distributeCandies(6,1),
    
    sol.stringCount(3),
    sol.stringCount(4),
    sol.stringCount(10),
    
    # sol.maxSpending(values = [[8,5,2],[6,4,1],[9,7,3]]),
    # sol.maxSpending(values = [[10,8,6,4,2],[9,7,5,3,2]]),
]
for r in result:
    print(r)
