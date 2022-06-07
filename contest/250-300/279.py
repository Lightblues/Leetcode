

import bisect
from typing import List
import collections
import random
import heapq


""" @220206
https://leetcode-cn.com/contest/weekly-contest-279
 """
class Solution:
    """ 6000. 对奇偶下标分别排序
数组中奇数序号递增, 偶数递减 """
    def sortEvenOdd(self, nums: List[int]) -> List[int]:
        evens = nums[::2]
        odds = nums[1::2]
        evens.sort()
        odds.sort(reverse=True)
        result = [0]*len(nums)
        result[::2] = evens
        result[1::2] = odds
        return result

    """ 6001. 重排数字的最小值
给你一个整数 num 。重排 num 中的各位数字，使其值 最小化 且不含 任何 前导零。注意负数.
输入：num = -7605
输出：-7650
解释：-7605 中各位数字的部分可行排列为：-7650、-6705、-5076、-0567。
不含任何前导零且值最小的重排数字是 -7650 。 """
    def smallestNumber(self, num: int) -> int:
        if num == 0:
            return 0
        strs = str(num)
        if strs[0] != '-':
            chars = sorted(strs)
            idx = bisect.bisect_left(chars, '1')
            result = [chars[idx]] + chars[:idx] + chars[idx+1:]
            return int(''.join(result))
        else:
            chars = sorted(strs[1:])
            result = int(''.join(chars[::-1]))
            return -result

    """ 6003. 移除所有载有违禁货物车厢所需的最少时间
 一个 01 序列表示违禁物品, 前后移除一辆火车代价位 1, 移除中间的一辆代价为2, 求移除所有违禁货车最小代价

思路一: 从左边和右边非别累加计算单面的最小代价, 加起来求最小 (其实就是在不同的点分割).
注意 更新公式(DP): 当 s[i+1]=='1' 时 dp[i+1] = min(dp[i]+2, i+1), 因为若从左边全部移除的代价是 i+1, 从中间取走的代价是 +2
为了计算的方便在头部加一个 [0]; 注意到在点 i 处分割的总代价为 dp1[i]+dp2[i+1], 正好错位加和
 
 参见 [here](https://leetcode-cn.com/problems/minimum-time-to-remove-all-cars-containing-illegal-goods/solution/qian-hou-zhui-fen-jie-dp-by-endlesscheng-6u1b/)
 """
    def minimumTime(self, s: str) -> int:
        def search(s):
            dp  = [0]
            isPrefix = True
            for i in range(len(s)):
                if s[i]=='0':
                    isPrefix = False
                    dp.append(dp[-1])
                else:
                    if isPrefix:
                        dp.append(dp[-1]+1)
                    else:
                        dp.append(
                            min(dp[-1]+2, i+1)
                        )
            return dp
        left2right = search(s)
        right2left = search(s[::-1])[::-1]
        result = [i+j for i,j in zip(left2right, right2left)]
        return min(result)

sol = Solution()
res = [
    # sol.sortEvenOdd(nums = [4,1,2,3]),
    # sol.smallestNumber(num = 310),
    # sol.smallestNumber(num = -7605),
    # sol.smallestNumber(0),
    # sol.minimumTime(s = "1100101"),
    # sol.minimumTime("010110"),
]
for r in res:
    print(r)


""" 6002. 设计位集
位集 Bitset 是一种能以紧凑形式存储位的数据结构。

请你实现 Bitset 类。
- Bitset(int size) 用 size 个位初始化 Bitset ，所有位都是 0 。
- void fix(int idx) 将下标为 idx 的位上的值更新为 1 。如果值已经是 1 ，则不会发生任何改变。
- void unfix(int idx) 将下标为 idx 的位上的值更新为 0 。如果值已经是 0 ，则不会发生任何改变。
- void flip() 翻转 Bitset 中每一位上的值。换句话说，所有值为 0 的位将会变成 1 ，反之亦然。
- boolean all() 检查 Bitset 中 每一位 的值是否都是 1 。如果满足此条件，返回 true ；否则，返回 false 。
- boolean one() 检查 Bitset 中 是否 至少一位 的值是 1 。如果满足此条件，返回 true ；否则，返回 false 。
- int count() 返回 Bitset 中值为 1 的位的 总数 。
- String toString() 返回 Bitset 的当前组成情况。注意，在结果字符串中，第 i 个下标处的字符应该与 Bitset 中的第 i 位一致。

条件是 「至多调用 toString 方法 5 次」; 也即主要是要优化其他操作的时间复杂度。

尝试直接用列表存储, 超时了, 可能是 flip, all, one 等操作复杂度较高.
优化为位存储+一个变量intcount存储非零位数量, 从而优化时间复杂度. 
"""
class Bitset:
    def __init__(self, size: int):
        self.bits = [0]*size

    def fix(self, idx: int) -> None:
        self.bits[idx] = 1

    def unfix(self, idx: int) -> None:
        self.bits[idx] = 0

    def flip(self) -> None:
        self.bits = [1-b for b in self.bits]


    def all(self) -> bool:
        return sum(self.bits) == len(self.bits)

    def one(self) -> bool:
        return sum(self.bits) > 0

    def count(self) -> int:
        return sum(self.bits)

    def toString(self) -> str:
        return ''.join(['1' if b else '0' for b in self.bits])

class Bitset2:

    def __init__(self, size: int):
        self.bits = 0
        self.size = size
        self.intcount = 0

    def fix(self, idx: int) -> None:
        if not (self.bits & 1 << idx):
            self.intcount += 1
            self.bits |= 1 << idx

    def unfix(self, idx: int) -> None:
        if self.bits & 1 << idx:
            self.intcount -= 1
            self.bits ^= 1 << idx

    def flip(self) -> None:
        self.bits ^= (1 << self.size) - 1 # 注意要加上 括号, 加减优先级高于位运算!!!
        self.intcount = self.size - self.intcount

    def all(self) -> bool:
        return self.bits == (1 << self.size) - 1

    def one(self) -> bool:
        return self.bits > 0

    def count(self) -> int:
        return self.intcount

    def toString(self) -> str:
        result = []
        ii = 1
        for i in range(self.size):
            result.append(str(int(self.bits & ii > 0)))
            ii <<= 1
        return ''.join(result)

t = Bitset2(2)
print(t.toString())
t.fix(1)
print(t.toString())
t.flip()
print(t.toString())
# Your Bitset object will be instantiated and called as such:
# obj = Bitset(size)
# obj.fix(idx)
# obj.unfix(idx)
# obj.flip()
# param_4 = obj.all()
# param_5 = obj.one()
# param_6 = obj.count()
# param_7 = obj.toString()