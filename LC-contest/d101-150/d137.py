# from easonsi.util.leetcode import *
import enum
from typing import *
from math import inf


# def testClass(inputs):
#     # 用于测试 LeetCode 的类输入
#     s_res = [None] # 第一个初始化类, 一般没有返回
#     methods, args = [eval(l) for l in inputs.split('\n')]
#     class_name = eval(methods[0])(*args[0])
#     for method_name, arg in list(zip(methods, args))[1:]:
#         r = (getattr(class_name, method_name)(*arg))
#         s_res.append(r)
#     return s_res

""" 
https://leetcode.cn/contest/biweekly-contest-137

T4 的前后缀分解比较有意思. 需要分析复杂度! 
Easonsi @2025 """
class Solution:
    """ 3255. 长度为 K 的子数组的能量值 II 一个很奇怪的数组题
限制: k,n 1e5 
"""
    def resultsArray(self, nums: List[int], k: int) -> List[int]:
        acc = 1
        for i in range(1, k-1):
            if nums[i] == nums[i-1]+1: acc += 1
            else: acc = 1
        res = []
        for i in range(k-1, len(nums)):
            if nums[i] == nums[i-1]+1:  acc += 1
            else:  acc = 1
            if acc >= k: res.append(nums[i])
            else: res.append(-1)
        return res
    
    
    """ 3257. 放三个车的价值之和最大 II #hard 在一个board上每个格子有一定分数, 要求放三个车, 使得互不攻击情况下, 之和最大
限制: n 500; 
思路1: #前后缀分解 
    - 枚举中间行的位置 (i,j), 然后看所匹配的 [0...i-1] 行 [i+1...n-1] 行的所选元素. -- 只需要保证所选元素非同列即可! 
    - 要考虑哪些前/后元素? 注意到, 我们只需要记录前后缀不同列最大/次大/第三大的的元素即可! -- 因为答案必然在这三个元素中获取到! 
复杂度: O(mn)
[ling](https://leetcode.cn/problems/maximum-value-sum-by-placing-three-rooks-ii/solutions/2884186/qian-hou-zhui-fen-jie-pythonjavacgo-by-e-gc48/)
思路2: 暴力枚举
    枚举所有的三行所在位置, 然后枚举三列所在的位置即可! -- 也是预处理每一行的最大/次大/第三大元素, 复杂度: O(m^3 + mn) -- 优化比较好可以过!
[TsRepper](https://leetcode.cn/problems/maximum-value-sum-by-placing-three-rooks-ii/solutions/2884062/mei-ju-by-tsreaper-bgpb/)
    """
    def maximumValueSum(self, board: List[List[int]]) -> int:
        m = len(board)
        def update(tmp, row: List[int]):
            for j,x in enumerate(row): # now is (x, j)
                # 将x插入最大/次大/第三大, 并维护不同列
                for k in range(3):
                    if x > tmp[k][0] and all(j!=t[1] for t in tmp[:k]):  # 保证不同列!
                        tmp[k], (x,j) = (x, j), tmp[k]  # swap!
        tmp = [(-inf, -1)] * 3 # 记录最大/次大/第三大元素和所在列
        pre_max = [None] * m
        for i in range(m):
            update(tmp, board[i])
            pre_max[i] = tmp[:]
        tmp = [(-inf, -1)] * 3 # 记录最大/次大/第三大元素和所在列
        suff_max = [None] * m
        for i in range(m-1, -1, -1):
            update(tmp, board[i])
            suff_max[i] = tmp[:]
        # 枚举所有的中间元素
        ans = -inf
        for i in range(1, m-1): # enum the middle row
            for j, x in enumerate(board[i]):
                for y, j2 in pre_max[i-1]:
                    for z, j3 in suff_max[i+1]:
                        if j!=j2 and j!=j3 and j2!=j3:
                            ans = max(ans, x+y+z)
        return ans

    
sol = Solution()
result = [
    # sol.resultsArray(nums = [1,2,3,4,3,2,5], k = 3),
    # sol.resultsArray(nums = [2,2,2,2,2], k = 4),
    # sol.resultsArray([1,30,31,32], 3),

    # sol.maximumValueSum(board = [[-3,1,1,1],[-3,1,-3,1],[-3,2,1,1]]),
    sol.maximumValueSum(board = [[1,2,3],[4,5,6],[7,8,9]])
]
for r in result:
    print(r)
