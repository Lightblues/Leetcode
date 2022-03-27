from typing import List, Optional
import collections
import math
import bisect
import heapq
from functools import lru_cache

from torch import maximum
# import sys
# sys.setrecursionlimit(10000)

from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 5268. 找出两数组的不同 """
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        res = [
            [i for i in nums1 if i not in nums2],
            [i for i in nums2 if i not in nums1]
        ]
        return [list(set(i)) for i in res]

    """ 5236. 美化数组的最少删除数 `中`
定义美丽数组: (1) 长度为偶数; (2) 2i, 2i+1 位的数字不相同. 空数组也符合
要求: 将一组数组转为美丽数组, 最少删除的数字个数

输入：nums = [1,1,2,3,5]
输出：1
解释：可以删除 nums[0] 或 nums[1] ，这样得到的 nums = [1,2,3,5] 是一个美丽数组。可以证明，要想使 nums 变为美丽数组，至少需要删除 1 个元素。
输入：nums = [1,1,2,2,3,3]
输出：2
解释：可以删除 nums[0] 和 nums[5] ，这样得到的 nums = [1,2,2,3] 是一个美丽数组。可以证明，要想使 nums 变为美丽数组，至少需要删除 2 个元素。

思路: 贪心. 每遇到 **约束对** 不满足的情况, 这两个数字必然是相同的, 随便删除一个即可.
若出现 [..., 1,1,2,2,3,3, ...] 的情况, 不管是前面删除使得三组相同数字处于不同的约束对, 还是删除最前面的 1, 效果是一样的.
另外需要注意最后长度必须是偶数
 """
    def minDeletion(self, nums: List[int]) -> int:
        res = 0 
        flip = -1 # 标记目前长度的奇偶
        last = None # 上一个数字
        for num in nums:
            if flip==-1:
                last = num
                flip *= -1
            else:
                if num == last:
                    res += 1
                else:
                    last = num
                    flip *= -1
        if flip == 1: # 保证是偶数长度
            res += 1
        return res

    """ 5253. 找到指定长度的回文数
要求得到长度为 l 的回文数中的第 k 个; 超出限制则返回 -1

输入：queries = [1,2,3,4,5,90], intLength = 3
输出：[101,111,121,131,141,999]
解释：
长度为 3 的最小回文数依次是：
101, 111, 121, 131, 141, 151, 161, 171, 181, 191, 201, ...
第 90 个长度为 3 的回文数是 999 。

思路: 递归
注意这里回文数数量限制有两种: (1) 内部回文数可以以0开始, (2) 回文数定义, 例如长度为3的最小回文数为 101. 可知, 长度为 1/2 的回文数数量为 9, 长度为 3/4 的回文数数量为 90; 内部回文数数量为 10, 100, 1000...
因此, 实际上是一个「进制」问题, 可以用递归来解.
需要注意: 题目中要求得到第 ith个回文数, 从1开始; 但是在进制的计算中, 必须应该从0开始. 例如, 进制为10, 则要求得到第11个 (其实是10)回文数, 应该计算 `div(10, 10) = 1, 0`; 在本题中, 外部的需要加上1, 也即 `202`
 """
    def kthPalindrome(self, queries: List[int], intLength: int) -> List[int]:
        maxLen = 15+1 # intLength <=15
        # 辅助
        len2Max = [0]*maxLen # 长度为 l 的回文数的数量
        len2MaxInner = [0]*maxLen # 内部回文数的数量 (没有首位非零的约束)
        for i in range(1, maxLen):
            len2Max[i] = 9 * 10**((i-1)//2)
            len2MaxInner[i] = 10 * 10**((i-1)//2)
        # print(len2Max)

        def get_ith_palindrome_innter(l, ith):
            # 获取长度为 l 的第 ith 个内部回文数 (从0开始)
            # 这里的 ith 是从 0 开始的
            if l<=2:
                return str(ith) * l
            maximumInner = len2MaxInner[l-2]
            x, y = divmod(ith, maximumInner)
            return str(x) + get_ith_palindrome_innter(l-2, y) + str(x)
        
        def get_ith_palindrome(l, ith):
            """ 获取长度为 l 的回文数的第 ith 个
            注意这里的 ith 从1开始
             """
            maximum = len2Max[l]
            if ith > maximum:
                return -1
            if l<=2:
                return str(ith) * l
            maximumInner = len2MaxInner[l-2]
            x, y = divmod(ith-1, maximumInner) # ith 从1开始; 但是做除法的时候一定要从0开始!!!
            return str(x+1) + get_ith_palindrome_innter(l-2, y) + str(x+1)
        
        res = [get_ith_palindrome(intLength, q) for q in queries]
        return [int(i) for i in res]

    """ 5269. 从栈中取出 K 个硬币的最大面值和
给定一组栈和可以取的硬币数量k, 要求取到的面值最大.

输入：piles = [[100],[100],[100],[100],[100],[100],[1,1,1,1,1,1,700]], k = 7
输出：706
解释：
如果我们所有硬币都从最后一个栈中取，可以得到最大面值和。

复杂度: 栈数量 n<=1000; 操作次数 k<=2000
 """
    def maxValueOfCoins(self, piles: List[List[int]], k: int) -> int:
        pass



sol = Solution()
result = [
    # sol.findDifference(nums1 = [1,2,3,3], nums2 = [1,1,2,2]),
    
    # sol.minDeletion(nums = [1,1,2,2,3,3]),
    # sol.minDeletion([1,1,2,3,4]),

    # sol.kthPalindrome(queries = [1,2,3,4,5,90], intLength = 3),
    sol.kthPalindrome(queries = [62], intLength = 4),
    sol.kthPalindrome([696771750,62,47,14,17,192356691,209793716,23,220935614,447911113,5,4,72], 4),
]
for r in result:
    print(r)