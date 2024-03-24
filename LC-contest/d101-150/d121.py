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
https://leetcode-cn.com/contest/biweekly-contest-121


T4 有点难受orz

Easonsi @2023 """
class Solution:
    """ 2996. 大于等于顺序前缀和的最小缺失整数 """
    def missingInteger(self, nums: List[int]) -> int:
        i = 0; n = len(nums)
        while i+1<n and nums[i+1]==nums[i]+1:
            i += 1
        s = sum(nums[:i+1])
        ss = set(nums)
        while s in ss:
            s += 1
        return s
    
    """ 2997. 使数组异或和等于 K 的最少操作次数 """
    def minOperations(self, nums: List[int], k: int) -> int:
        x = 0
        for xx in nums:
            x ^= xx
        x ^= k
        return x.bit_count()
    
    """ 2998. 使 X 和 Y 相等的最少操作次数 在合法的前提下, 可以对于x /5, /11, -1, +1, 文最少经过多少次可以变为 y """
    def minimumOperationsToMakeEqual(self, x: int, y: int) -> int:
        vis = set()
        cand = [x]; d = 0
        while cand:
            new_cand = []
            for i in cand:
                if i == y: return d
                if i in vis: continue
                vis.add(i)
                new_cand += [i+1, i-1]
                if i%5 == 0: new_cand.append(i//5)
                if i%11 == 0: new_cand.append(i//11)
            cand = new_cand
            d += 1
        return -1
    
    """ 2999. 统计强大整数的数目 #hard 定义「强大」的数以字符串s所代表的数字结尾, 同时每个数位都 <=limit
限制: n 1e15; limit 1e9
思路1: 问题变为 f(finish, limit, s) 求小于等于finish的数字中，满足条件的数的个数
    假设 finish = ab..sss, 可以先看小于 a0.. 中每个位数小于等于limit的个数; 再加上 b..sss 中每个位数小于等于limit的个数
见 [ling](https://leetcode.cn/problems/count-the-number-of-powerful-integers/solutions/2595149/shu-wei-dp-shang-xia-jie-mo-ban-fu-ti-da-h6ci/)
"""
    # WA!!!!
    # def numberOfPowerfulInt(self, start: int, finish: int, limit: int, s: str) -> int:
    #     n = len(s)
    #     def f(x):
    #         xx, re = divmod(x, 10**n)
    #         # 若末尾比s大的情况下, 可以取前缀0
    #         ans = 1 if x>=int(s) else 0
    #         base = 0
    #         while xx:
    #             xx, b = divmod(xx, 10)
    #             ans += min(b, limit) * (limit+1)**base
    #             if base==0 and b <= limit and int(re < int(s)):
    #                 ans -= 1
    #             base += 1
    #         return ans
    #     return f(finish) - f(start-1)


sol = Solution()
result = [
    # sol.minOperations(nums = [2,1,3,4], k = 1),
    # sol.minimumOperationsToMakeEqual(x = 54, y = 2),
    sol.numberOfPowerfulInt(start = 1, finish = 6000, limit = 4, s = "124"),
    sol.numberOfPowerfulInt(start = 15, finish = 215, limit = 6, s = "10"),
    sol.numberOfPowerfulInt(start = 1000, finish = 2000, limit = 4, s = "3000"),
    sol.numberOfPowerfulInt(1, 971, 9, "72"),
    sol.numberOfPowerfulInt(15, 1440, 5, "14"),
]
for r in result:
    print(r)
