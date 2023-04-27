
from typing import List
import collections



""" @220211
https://leetcode-cn.com/contest/weekly-contest-277
 """
class Solution:
    """ 2148. 元素计数 """
    def countElements(self, nums: List[int]) -> int:
        nums.sort()
        xmin, xmax = nums[0], nums[-1]
        if xmin==xmax:
            return 0
        else:
            return len(nums) - nums.count(xmin) - nums.count(xmax)

    """ 2149. 按符号重排数组 """
    def rearrangeArray(self, nums: List[int]) -> List[int]:
        poss = [i for i in nums if i>0]
        negs = [i for i in nums if i<0]
        result = []
        for i,j in zip(poss, negs):
            result.append(i)
            result.append(j)
        return result

    """ 2150. 找出数组中的所有孤独数字
给你一个整数数组 nums 。如果数字 x 在数组中仅出现 一次 ，且没有 相邻 数字（即，x + 1 和 x - 1）出现在数组中，则认为数字 x 是 孤独数字 。 """
    def findLonely(self, nums: List[int]) -> List[int]:
        counter = collections.Counter(nums)
        result = []
        for num,count in counter.items():
            if count==1 and num-1 not in counter and num+1 not in counter:
                result.append(num)
        return result

    """ 2151. 基于陈述统计最多好人数 #hard 限制: n 15
两种角色: 好人只说真话, 坏人可能真也可能假. 给定一个矩阵表示每个人的陈述 (0,1,2 分别表示 坏人, 好人, 未判断), 要求计算好人最多可能数量
思路1: 使用状态压缩枚举所有可能的情况. 我们可以用 #二进制 来表示一种待定情况
    对于一个mask, 我们可以在 O(n^2) 时间内验证.
    总体复杂度 O(2^n * n^2)
    [灵神](https://leetcode.cn/problems/maximum-good-people-based-on-statements/solution/er-jin-zhi-mei-ju-by-endlesscheng-ttix/)
思路2: #回溯 暴力枚举每个人是好人或坏人, 注意剪枝!!
    [代码随想](https://leetcode-cn.com/problems/maximum-good-people-based-on-statements/solution/hui-su-san-bu-qu-qing-xi-kuang-jia-by-sh-t7en/)
关联: 若坏人一定说假话: [CF](https://codeforces.com/problemset/problem/1594/D)
"""
    def maximumGood(self, statements: List[List[int]]) -> int:
        def check(i: int) -> int:
            cnt = 0  # i 中好人个数
            for j, row in enumerate(statements):  # 枚举 i 中的好人 j
                if (i >> j) & 1:
                    if any(st < 2 and st != (i >> k) & 1 for k, st in enumerate(row)):
                        return 0  # 好人 j 的某个陈述 st 与实际情况矛盾
                    cnt += 1
            return cnt

        return max(check(i) for i in range(1, 1 << len(statements)))



sol = Solution()
results = [
    # sol.countElements(nums = [11,7,2,15]),
    sol.maximumGood([[2,2,2,2,2,2],[2,2,2,1,1,2],[2,2,2,2,2,2],[0,1,0,2,1,2],[0,1,2,1,2,0],[0,0,1,0,2,2]]),
    sol.maximumGood([[2,1,1,1],[1,2,1,1],[1,1,2,1],[1,1,1,2]]),
    sol.maximumGood(statements = [[2,0],[0,2]]),
    sol.maximumGood(statements = [[2,1,2],[1,2,2],[2,0,2]]),
    sol.maximumGood([[2,0,2,2,0],[2,2,2,1,2],[2,2,2,1,2],[1,2,0,2,2],[1,0,2,1,2]]),
    
]
for r in results:
    print(r)