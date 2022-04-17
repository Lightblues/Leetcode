import re
from typing import List, Optional
import collections
import math
import bisect
import heapq
from functools import lru_cache

from rsa import DecryptionError
# import sys
# sys.setrecursionlimit(10000)

from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 6037. 按奇偶性交换后的最大数字
注意审题! 是 奇偶性 相同的数字可以交换, 而不是 奇偶index"""
    def largestInteger(self, num: int) -> int:
        # num_list = list(str(num))
        # evens = sorted(num_list[::2], reverse=True)
        # odds = sorted(num_list[1::2], reverse=True)
        # num_list[::2] = evens
        # num_list[1::2] = odds
        # return int("".join(num_list))
        
        num_list = list(str(num))
        even_idxs = [i for i,nn in enumerate(num_list) if int(nn)%2==0]
        even_sorted = sorted([num_list[i] for i in even_idxs], reverse=True)
        for i,nn in zip(even_idxs, even_sorted):
            num_list[i] = nn
        odd_idxs = [i for i,nn in enumerate(num_list) if int(nn)%2==1]
        odd_sorted = sorted([num_list[i] for i in odd_idxs], reverse=True)
        for i,jj in zip(odd_idxs, odd_sorted):
            num_list[i] = jj
        return int("".join(num_list))
    
    """ 6038. 向表达式添加括号后的最小结果 
在括号左右添加一对括号, 例如 `"12+34"` 变为 `"1(2+3)4"` 也即左中右三个元素的乘积, 要求最小化结果
"""
    def minimizeResult(self, expression: str) -> str:
        left, right = expression.split("+")
        result = float('inf')
        result_exp = ""
        # for i in range(len(left)):
        #     for j in range(1, len(right)+1):
        #         l = int(left[:i]) if i>0 else 1
        #         mid = int(left[i:]) + int(right[:j])
        #         r = int(right[j:]) if j<len(right) else 1
        #         if result > l*mid*r:
        #             result = l*mid*r
        #             result_exp = expression[:i] + "(" + expression[i:i+j+3] + ")" + expression[i+j+3:]
        # return result_exp
        
        for i in range(len(left)):
            for j in range(len(right)):
                l = int(left[:i]) if i>0 else 1
                r = int(right[-j:]) if j>0 else 1
                mid = eval(expression[i:len(expression)-j])
                if l*r*mid < result:
                    result = l*r*mid
                    result_exp = expression[:i] + "(" + expression[i:len(expression)-j] + ")" + expression[len(expression)-j:]
        return result_exp
    
    """ 6039. K 次增加后的最大乘积
给你一个非负整数数组 `nums` 和一个整数 `k`, 可以将k分配到数组元素上 (相加), 要求乘积最大.

思路: intuition是填充最小的那些数字. 因此可以看作是阶梯水池蓄水的问题.
注意复杂度: nums.length, k 为 1e5. 最开始遍历index时, 每次都修改 nums[:index], 复杂度为 O(n^2) 会超时. 修改为记录便利的终止位置后一次性修改.
    """
    def maximumProduct(self, nums: List[int], k: int) -> int:
        mod = 10**9+7
        l = len(nums)
        nums = sorted(nums)
        
        # 遍历, 模拟阶梯蓄水池蓄水
        index = 1
        while index != l and k>0:
            delta = nums[index]-nums[index-1]
            if k > delta*index:
                k -= delta*index
                # 1) 刚开始直接修改 nums[:index]
                # nums[:start] = [nums[start]] * start
                index += 1
            else:
                # flag = False
                break
        # 2) 变为, 最后修改 nums[:index]
        nums[:index-1] = [nums[index-1]] * (index-1)
        
        # 填充剩余的 k
        a,b = divmod(k, index)
        nums[:index] = [nums[0]+a] * index
        nums[:b] = [nums[0]+1] * b
        
        res = 1
        for num in nums:
            res = (res * num) % mod
        return res
    
    """ 6040. 花园的最大总美丽值
数组 flowers 代表每个花园的花数量, 数字 newFlowers, 可以分配到各个花园中. 所以花园的分数定义为: 
1) 花的数量至少为 `target` 的花园为「完善的」, 每个花园有 `full` 分;
2) 剩余「不完善」的花园, 总共有 `min(num_flower) * partial`, 也即这些花园中数量最少的花 * 一个分值.

输入：flowers = [2,4,5,3], newFlowers = 10, target = 5, full = 2, partial = 6
输出：30
解释：Alice 可以按以下方案种花
- 在第 0 个花园种 3 朵花
- 在第 1 个花园种 0 朵花
- 在第 2 个花园种 0 朵花
- 在第 3 个花园种 2 朵花
花园里花的数目为 [5,4,5,5] 。总共种了 3 + 0 + 0 + 2 = 5 朵花。
有 3 个花园是完善的。
不完善花园里花的最少数目为 4 。
所以总美丽值为 3 * 2 + 4 * 6 = 6 + 24 = 30 。
没有其他方案可以让花园总美丽值超过 30 。
注意，Alice可以让所有花园都变成完善的，但这样她的总美丽值反而更小。
"""
    def maximumBeauty(self, flowers: List[int], newFlowers: int, target: int, full: int, partial: int) -> int:
        l = len(flowers)
        # 先对 flowers 排序
        flowers.sort()
        
        # need_for_target 从后往前, 表示将从 i 开始最后的花园变为target所需的最少花费, -1表示无法
        need_for_target = [-1] * (l+1)
        need_for_target[-1] = 0
        for i in range(l-1, -1, -1):
            if flowers[i] >= target:
                need_for_target[i] = 0
            else:
                need_for_target[i] = need_for_target[i+1] + target-flowers[i]
                if need_for_target[i] > newFlowers:
                    break
        # need_for_partial, 表示将阶梯填充到第i个位置的高度, 所需的数量
        left_flowers = newFlowers
        need_for_partial = [-1] * (l)
        need_for_partial[0] = 0
        for i in range(1, l):
            needed = (flowers[i] - flowers[i-1]) * i
            if left_flowers >= needed:
                left_flowers -= needed
                need_for_partial[i] = need_for_partial[i-1] + needed
            else:
                break
        # 补充不完善花园的右边界
        left_partial = len([i for i in need_for_partial if i>=0])
        
        result = 0
        for i in range(l, -1, -1): # 注意, 从 l 开始, 因为边界情况: l==1时, 可能可能都不填充为target更好
            score = 0
            if need_for_target[i] == -1 or need_for_target[i] > newFlowers:
                break
            score += full * (l-i)
            # 边界: i==0 说明全变为完善花园, 没有不完善花园
            if i>0:
                left_flowers = newFlowers - need_for_target[i]
                # 注意搜索边界不能超过 left_partial
                left = min(left_partial, i)
                idx = bisect.bisect_right(need_for_partial, left_flowers, 0, left)
                minn = flowers[idx-1] + (left_flowers-need_for_partial[idx-1]) // (idx)
                minn = min(minn, target-1)
                score += partial * minn
            result = max(result, score)
        return result

sol = Solution()
result = [
    # sol.largestInteger(num = 65875),
    # sol.largestInteger(247),
    
    # sol.minimizeResult(expression = "247+38"),
    # sol.minimizeResult(expression = "999+999"),
    # sol.minimizeResult("12+34"),
    
    sol.maximumProduct(nums = [0,4], k = 5),
    sol.maximumProduct(nums = [6,3,3,2], k = 2),
    # 20, 216
    
    # sol.maximumBeauty(flowers = [1,3,1,1], newFlowers = 7, target = 6, full = 12, partial = 1), # 14
    # sol.maximumBeauty(flowers = [2,4,5,3], newFlowers = 10, target = 5, full = 2, partial = 6), # 30
    # sol.maximumBeauty([13], 18, 15, 9, 2), # 28
    # sol.maximumBeauty([20,1,15,17,10,2,4,16,15,11], 2, 20, 10, 2), # 14
    # sol.maximumBeauty([5,19,1,1,6,10,18,12,20,10,11],6,20,3, 11), # 47
]
for r in result:
    print(r)