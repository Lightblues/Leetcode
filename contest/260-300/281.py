

import bisect
from typing import List, Optional
import collections
import random
import heapq
import math
from functools import lru_cache

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

""" @220206
https://leetcode-cn.com/contest/weekly-contest-281
 """
class Solution:
    """ 6012. 统计各位数字之和为偶数的整数个数 """
    def countEven(self, num: int) -> int:
        def isEven(num):
            l = list(str(num))
            num = sum([int(i) for i in l])
            return num % 2 == 0
        return sum(isEven(i) for i in range(1, num+1))
    
    """ 6013. 合并零之间的节点 """
    def mergeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        result = ListNode(0)
        p = result
        num = 0
        while head:
            if head.val:
                num += head.val
            else:
                if num:
                    newNode = ListNode(num)
                    num = 0
                    p.next = newNode
                    p = p.next
            head = head.next
        return result.next


    """ 6014. 构造限制重复的字符串
给定一组字符, 要求构造字典序最大的字符串, 限制每个字符最多连续的次数.
当两个字符串长度不同时, 先序比较前面部分, 仅当 min(a.length, b.length) 时算较长的字符串字典序较大.

输入：s = "aababab", repeatLimit = 2
输出："bbabaa"
解释：
使用 s 中的一些字符来构造 repeatLimitedString "bbabaa"。 
字母 'a' 连续出现至多 2 次。 
字母 'b' 连续出现至多 2 次。 
因此，没有字母连续出现超过 repeatLimit 次，字符串是一个有效的 repeatLimitedString 。 
该字符串是字典序最大的 repeatLimitedString ，所以返回 "bbabaa" 。 
注意，尽管 "bbabaaa" 字典序更大，但字母 'a' 连续出现超过 2 次，所以它不是一个有效的 repeatLimitedString 。 

根据题意, 应该是按照字典序, 尽量把大字符连续放在前面, 之间插入一个次大字符即可, 即 bbbabbba... 这样的形式(repeatLimit=3)
v0
关键在于构造算法. 这里用 head 记录最大字符, 用 others 列表记录其他字符.
while head 遍历. 关键在如何避免重复? 
v1
每次取最大字符, 后面添加一个次大字符即可! 终止条件是没有次大字符了.
"""
    def repeatLimitedString(self, s: str, repeatLimit: int) -> str:
        d = collections.Counter(s)
        keys = sorted(list(d.keys()), reverse=True)
        result = ""
        head, others = keys[0], keys[1:]
        
        # 辅助函数, 每次取一个次大字符, 当次大字符用完时从 others 列表中 pop
        def updateOthers():
            ch = others[0]
            d[others[0]] -= 1
            if d[others[0]] == 0:
                others.pop(0)
            return ch
        
        while head:
            chrmax = min(repeatLimit, d[head])
            result += head * chrmax

            # 1. 最大字符用完了
            if chrmax == d[head]:
                if others:
                    head, others = others[0], others[1:]
                else:
                    # 当 other 列表为空, return
                    return result
            # 2. 最大字符还有剩余
            else:
                d[head] -= chrmax
                if others:
                    ch = updateOthers()
                    result += ch
                # 当没有其他字符时, return
                else:
                    return result


    """ 6015. 统计可以被 K 整除的下标对数目
给定一个数组 nums 和一个正整数 k, 返回满足条件的下标对 (i, j) 的数目
要求 nums[i] * nums[j] % k == 0

输入：nums = [1,2,3,4,5], k = 2
输出：7
解释：
共有 7 对下标的对应积可以被 2 整除：
(0, 1)、(0, 3)、(1, 2)、(1, 3)、(1, 4)、(2, 3) 和 (3, 4)
它们的积分别是 2、4、6、8、10、12 和 20 。
其他下标对，例如 (0, 2) 和 (2, 4) 的乘积分别是 3 和 15 ，都无法被 2 整除。

n1*n2 % k == 0 的条件: n1和n2 和 k 的最大公约数之积能被k整除, 即 gcd(n1, k) * gcd(n2, k) % k == 0
由于 k 的因子是有限的, 就可以对于 nums 中的数字分组.
对于一个组, 其中的数字与k的最大公约数都是 n1, 假设组大小为 len1
考虑两种情况: 1. 其他组中能够能够配合n1的数字个数为 len2, 则交互共有 len1*len2 个数字; 2. 若 (n1*n1)%k == 0, 即自身就满足条件, 组内组合数为 C(2,len1) = len1*(len1-1)/2
为了避免重复, 对于因子从大到小排序, 每组都和后边的因子比较
 """
    def coutPairs(self, nums: List[int], k: int) -> int:
        # 特殊情况
        if k==1:
            n = len(nums)
            return n*(n-1)//2
        
        # 计算每个数字和 k 的最大公约数, 分组
        gcds = [math.gcd(num, k) for num in nums]
        d = collections.Counter(gcds)
        keys = sorted(list(d.keys()), reverse=True)
        result = 0

        for i,n1 in enumerate(keys):
            nNow = d[n1]
            # 1. n1 和 n2 之积能被 k 整除
            nOthers = 0
            for n2 in keys[i+1:]:
                if n1*n2%k == 0:
                    nOthers += d[n2]
            result += nOthers*nNow
            # 2. n1 自身就满足条件
            if (n1*n1)%k == 0 and n1 > 1:
                # C(nNow, 2)
                result += nNow*(nNow-1)//2

        return result
    
sol = Solution()
rels = [
    # sol.countEven(30),

    # sol.repeatLimitedString(s = "cczazcc", repeatLimit = 3),
    # sol.repeatLimitedString(s = "aababab", repeatLimit = 2),
    # sol.repeatLimitedString(s = "aabababaaaaaaaaaaaaaaaaaaa", repeatLimit = 2),
    
    sol.coutPairs(nums = [1,2,3,4,5], k = 2),
    sol.coutPairs(nums = [1,2,3,4], k = 5),
    sol.coutPairs([8,10,2,5,9,6,3,8,2], 6),
    sol.coutPairs([3,2,6,1,8,4,1], 3),
    sol.coutPairs([5,9,5,5,10,9,2,6,7],2), # 21
]
for r in rels:
    print(r)

