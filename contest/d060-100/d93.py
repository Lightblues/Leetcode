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
https://leetcode-cn.com/contest/biweekly-contest-93
https://leetcode.cn/circle/discuss/xgnLKJ/
@2022 """
class Solution:
    """ 6261. 数组中字符串的最大值 #easy """
    
    """ 6262. 图中最大星和 #medium 星状子图中, 求分数和最大是多少 """
    def maxStarSum(self, vals: List[int], edges: List[List[int]], k: int) -> int:
        n = len(vals)
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v); g[v].append(u)
        ans = -inf
        for c,v in enumerate(vals):
            ss = sorted([vals[i] for i in g[c]], reverse=True)
            # 细节: 注意可能有 没有连边的孤立节点. 
            vn = max(list(accumulate(ss[:k], initial=0))) if len(ss)>0 else 0
            ans = max(ans, v+vn)
        return ans
    
    """ 6263. 青蛙过河 II #medium #review 青蛙需要从第一个跳到最后一个再跳回来, 不能重复石头. 代价为路径上跳跃的最大距离, 问最小代价. 
思路1: 最优结构是, 多一个石子肯定不会使得结果变坏.
    因此, 可以利用每一个石子. 直觉是: 考虑 i+2, i 两个石子的位置. 但没想出为什么可行. #todo
    具体的分析参见
"""
    def maxJump(self, stones: List[int]) -> int:
        ans = stones[1]-stones[0]
        n = len(stones)
        for i in range(2, n):
            ans = max(ans, stones[i]-stones[i-2])
        return ans
    
    """ 6264. 让数组不相等的最小总代价 #hard 有两个相同长度的数组, 每次操作可以在 nums1 中找两个下标元素交换, 目标使得 nums1 和 nums2 中的元素都不相等. 每次交换的代价为两元素idx之和, 问最小代价. 
https://leetcode.cn/problems/minimum-total-cost-to-make-arrays-unequal/
"""
    def minimumTotalCost(self, nums1: List[int], nums2: List[int]) -> int:
        pass
    
    
    

    
sol = Solution()
result = [
    sol.maxStarSum(vals = [1,2,3,4,10,-10,-20], edges = [[0,1],[1,2],[1,3],[3,4],[3,5],[3,6]], k = 2),
]
for r in result:
    print(r)
