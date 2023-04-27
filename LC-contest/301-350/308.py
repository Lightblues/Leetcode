from easonsi import utils
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
https://leetcode.cn/contest/weekly-contest-308

T4 看到约束想到了CSP问题, 但其实要求拓扑排序还是比较清楚的, 应该直接看出来的.

@2022 """
class Solution:
    """ 6160. 和有限的最长子序列 """
    def answerQueries(self, nums: List[int], queries: List[int]) -> List[int]:
        nums.sort()
        acc = list(accumulate(nums))
        ans = []
        for q in queries:
            ans.append(bisect_right(acc, q))
        return ans
    """ 6161. 从字符串中移除星号 """
    def removeStars(self, s: str) -> str:
        st = []
        for ch in s:
            if ch=="*":
                if st: st.pop()
            else: st.append(ch)
        return "".join(st)
    """ 6162. 收集垃圾的最少总时间 无脑模拟题 """
    def garbageCollection(self, garbage: List[str], travel: List[int]) -> int:
        ans = 0
        mx = [0] * 3
        for i,g in enumerate(garbage):
            ans += len(g)
            if 'M' in g: mx[0] = i
            if 'P' in g: mx[1] = i
            if 'G' in g: mx[2] = i
        acc = list(accumulate(travel, initial=0))
        for i in mx:
            ans += acc[i]
        return ans
    
    """ 2392. 给定条件下构造矩阵 #hard #题型
给定一个k, 要求构造 k*k 的矩阵, 填充 1~k 共k个数字, 其他位置填0. 要求满足行/列约束. 约束的形式是, 给定一组 (i,j), 要求数字i所在行应该在j所在行的上面. 限制: k 400, 约束数量 n 1e4
思路0: 一开始看到约束条件想到 #CSP 问题, 但一想约束满足问题的搜索复杂度似乎不够? 没想清楚
思路1: 实际上就是一个 #拓扑排序. 
    分解行/列的约束条件, 每一个可以通过拓扑排序求解
"""

    
sol = Solution()
result = [
    # sol.answerQueries(nums = [4,5,2,1], queries = [3,10,21]),
    # sol.answerQueries(nums = [2,3,4,5], queries = [1]),
    # sol.removeStars(s = "leet**cod*e"),
    # sol.removeStars(s = "erase*****"),
    # sol.garbageCollection(garbage = ["G","P","GP","GG"], travel = [2,4,3]),
    # sol.garbageCollection(garbage = ["MMM","PGM","GP"], travel = [3,10]),
    sol.buildMatrix(k = 3, rowConditions = [[1,2],[3,2]], colConditions = [[2,1],[3,2]]),
    sol.buildMatrix(k = 3, rowConditions = [[1,2],[2,3],[3,1],[2,3]], colConditions = [[2,1]]),
]
for r in result:
    print(r)
