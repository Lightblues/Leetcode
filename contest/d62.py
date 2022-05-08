from tkinter import N
from typing import List, Optional
import collections
import math
import bisect
import heapq
import functools, itertools
# from functools import lru_cache
# import sys, os
# sys.setrecursionlimit(10000)
# from utils_leetcode import testClass
from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-62
@20220506 补 """
class Solution:
    """ 2022. 将一维数组转变成二维数组 """
    def construct2DArray(self, original: List[int], m: int, n: int) -> List[List[int]]:
        if len(original) != m*n:
            return []
        res = []
        for i in range(m):
            res.append(original[i*n: (i+1)*n])
        return res
    
    """ 2023. 连接后等于目标字符串的字符串对
给定一组字符串 和一个目标字符串 target, 返回从这组字符串中选择两个拼接可以得到 target 的组合数量.
"""
    def numOfPairs(self, nums: List[str], target: str) -> int:
        prefixMap = collections.defaultdict(int)
        postfixMap = collections.defaultdict(int)
        for num in nums:
            l = len(num)
            if num==target[:l]:
                prefixMap[l] += 1
            if num==target[-l:]:
                postfixMap[l] += 1
        ans = 0
        for l in prefixMap:
            ans += prefixMap[l] * postfixMap[len(target)-l]
        """ 修正项: target = xyxy 的形式, prefixMap[2] = a, postfixMap[2] = a
        上面错误计算为 a*a, 而实际上应该是 C(a, 2) * 2 = a*(a-1), 因此进行修正 ans -= a
        """
        ll = len(target)
        if ll%2==0 and target[:ll//2]==target[ll//2:]:
            ans -= prefixMap[ll//2]
        return ans
    
    """ 2024. 考试的最大困扰度
给定一个包含两种元素的序列, 最大改动数量为 k, 尽可能使得出现的连续相同元素最大

思路: #双指针 #滑动窗口
针对每种元素遍历数组 (可以写成一个函数), 在双指针遍历过程中, 维护左右指针之间的修改数量不超过 k. 具体而言, 可以 for 循环 right, 在超出条件的时候步进 left
参 [here](https://leetcode-cn.com/problems/maximize-the-confusion-of-an-exam/solution/kao-shi-de-zui-da-kun-rao-du-by-leetcode-qub5/)
"""
    def maxConsecutiveAnswers(self, answerKey: str, k: int) -> int:
        def get_ans(ch: str) -> int:
            left = 0    # 左指针
            sum = 0     # 记录修改的数量
            ans = 0
            # 遍历右指针, 当不满足条件是移动左指针
            for right in range(len(answerKey)):
                sum += answerKey[right] != ch
                while sum > k:
                    sum -= answerKey[left] != ch
                    left += 1
                ans = max(ans, right - left + 1)
            return ans
        return max(get_ans(ch) for ch in "TF")
    
    """ 2025. 分割数组的最多方案数 #题型
给定一个数组和一个数字k, 允许将数组中的某一个数字修改为k (也可以不修改), 要求最大化满足条件的分割数量.
条件: 给定一个 1<=pivot<n, 将数组分割为 nums[0:pivot-1] 和 nums[pivot:n-1] 两部分 (闭区间), 使得两部分的和相等.

思路: #双哈希表
计数组的前缀和为 cumsum, 总和为 total.
在不修改的情况下, 合法分割为 cumsum[i] = total-cumsum[i], 即 cumsum[i] = total/2.
考虑修改的情况: 将第i个元素进行修改, 记变化量为 d = k-nums[i], 对于i之前的元素其累计和不变, 之后的元素累计和增加d.
    因此, 1) 对于之前的元素, 合法条件变为 cumsum[j] = total+d-cumsum[j], 即 cumsum[j] = (total+d)/2; 2) 对i及其之后的元素, cumsum[j]+d = (total+d)-(cumsum[j]+d), 即 cumsum[j] = (total-d)/2
因此, 在遍历修改元素 i 的过程中, 用双哈希表记录前后的 cumsum分布情况.
参 [前缀和+双哈希表+枚举修改元素](https://leetcode-cn.com/problems/maximum-number-of-ways-to-partition-an-array/solution/qian-zhui-he-ha-xi-biao-mei-ju-xiu-gai-y-l546/)
注意: 这里要求的分割点必须在数组的中间, 在维护双哈希表的时候应该去掉total的情况. (见代码)
"""
    def waysToPartition(self, nums: List[int], k: int) -> int:
        rightMap = collections.defaultdict(int) # 前缀和数量统计
        cumsum  = [nums[0]]
        for i in range(1, len(nums)):
            rightMap[cumsum[-1]] += 1 # 这里 rightMap 用的是上一时刻的 cumsum. 这是因为分割要求 1<=pivot<n, 也即分割不能为首尾而只能出现在数组中间
            cumsum.append(cumsum[-1] + nums[i])
        total = cumsum[-1]
        ans = rightMap[total//2] if total%2==0 else 0
        
        # 在遍历修改过程中动态维护双哈希表
        leftMap = collections.defaultdict(int)
        # 从0开始, 注意开始状态: rightMap 共计 n-1 个, leftMap 为空.
        for i,num in enumerate(nums):
            d = k-num
            # 注意判断 (total+d)%2==才可能合法
            new = leftMap[(total+d)//2] + rightMap[(total-d)//2] if (total+d)%2==0 else 0
            ans = max(ans, new)
            # 动态维护左右前缀和 map, 注意用的是原来的 cumsum而和 k 无关
            s = cumsum[i]
            leftMap[s] += 1
            rightMap[s] -= 1
        return ans

sol = Solution()
result = [
    # sol.construct2DArray(original = [1,2,3,4], m = 2, n = 2),
    # sol.construct2DArray(original = [1,2], m = 1, n = 1),
    
    # sol.numOfPairs(nums = ["777","7","77","77"], target = "7777"),
    # sol.numOfPairs(nums = ["1","1","1"], target = "11"),
    
    # sol.maxConsecutiveAnswers(answerKey = "TTFF", k = 2),
    # sol.maxConsecutiveAnswers(answerKey = "TFFT", k = 1 ),
    
    sol.waysToPartition(nums = [2,-1,2], k = 3),
    sol.waysToPartition(nums = [22,4,-25,-20,-15,15,-16,7,19,-10,0,-13,-14], k = -33),
]
for r in result:
    print(r)
