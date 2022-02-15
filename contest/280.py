

import bisect
from typing import List
import collections
import random
import heapq
from functools import lru_cache


""" @220206
https://leetcode-cn.com/contest/weekly-contest-280
 """
class Solution:
    """ 6004. 得到 0 的操作数 """
    def countOperations(self, num1: int, num2: int) -> int:
        x,y = sorted([num1, num2])
        count = 0
        while x != 0:
            x,y = sorted([x, y-x])
            count += 1
        return count

    """ 6005. 使数组变成交替数组的最少操作数
交替数组的定义
*   `nums[i - 2] == nums[i]` ，其中 `2 <= i <= n - 1` 。
*   `nums[i - 1] != nums[i]` ，其中 `1 <= i <= n - 1` 。
也即 [1,2,1,2,1] 这种形式

需要注意边界条件 """
    def minimumOperations(self, nums: List[int]) -> int:
        if len(nums)==1:
            return 0
        sub1 = nums[0::2]
        sub2 = nums[1::2]
        count1 = collections.Counter(sub1)
        count2 = collections.Counter(sub2)
        most1 = count1.most_common(2)
        most2 = count2.most_common(2)
        count = 0
        if most1[0][0] == most2[0][0]:
            if len(most1)==len(most2)==1:
                count = max(most1[0][1], most2[0][1])
            if len(most1) > 1:
                count = max(count, most2[0][1] + most1[1][1])
            if len(most2) > 1:
                count = max(count, most1[0][1] + most2[1][1])
        else:
            count = most1[0][1] + most2[0][1]
        return len(nums) - count

    """ 6006. 拿出最少数目的魔法豆
给你一个 **正** 整数数组 `beans` ，其中每个整数表示一个袋子里装的魔法豆的数目。
请你从每个袋子中 **拿出** 一些豆子（也可以 **不拿出**），使得剩下的 **非空** 袋子中（即 **至少** 还有 **一颗** 魔法豆的袋子）魔法豆的数目 **相等** 。一旦魔法豆从袋子中取出，你不能将它放到任何其他的袋子中。

排序, 想像成一个阶梯, 最后留下来的就是一个矩形; 转化为遍历求矩形最大面积
 """
    def minimumRemoval(self, beans: List[int]) -> int:
        beans.sort()
        n = len(beans)
        summ = 0
        maxSquare = 0
        for i,val in enumerate(beans):
            summ += val
            maxSquare = max(maxSquare, val*(n-i))
        return summ - maxSquare

    """ 6007. 数组的最大与和
有编号为 1,2,...,numSlot的篮子, 要求把一个长度为 n 的数组放入篮子中, 每个篮子最多放两个数字!
定义放置的分数为, 数字和篮子编号与 `nums[i] & (assign[i]+1)`, 其中 assign 表示 第 i 个数字放在第 assign[i] 个篮子中

输入：nums = [1,2,3,4,5,6], numSlots = 3
输出：9
解释：一个可行的方案是 [1, 4] 放入篮子 1 中，[2, 6] 放入篮子 2 中，[3, 5] 放入篮子 3 中。
最大与和为 (1 AND 1) + (4 AND 1) + (2 AND 2) + (6 AND 2) + (3 AND 3) + (5 AND 3) = 1 + 0 + 2 + 2 + 3 + 1 = 9 。

*   `n == nums.length`
*   `1 <= numSlots <= 9`
*   `1 <= n <= 2 * numSlots`
*   `1 <= nums[i] <= 15`
 """
    # 暴力回溯, 超时!
    def maximumANDSum0(self, nums: List[int], numSlots: int) -> int:
        records = [0] * numSlots
        
        # recordFull = [[] for _ in range(numSlots)]
        def dfs(idx, curSum, curMax):
            if idx == len(nums):
                # print(recordFull, end=" ")
                # print(curSum)
                return max(curSum, curMax)
            val = nums[idx]
            flag = False
            for i in range(numSlots):
                if (records[i] == 2) or ((val & (i+1)) == 0):
                    # 加了 val & (i+1) 过滤后, 对于 用例 [14,7,9,8,2,4,11,1,9], 8 效果很好
                    # 但对于 [8,13,3,15,3,15,2,15,5,7,6], 8 这种, 很多 15, 13 的, 完全过滤不掉
                    continue
                flag = True
                records[i] += 1
                # recordFull[i].append(val)
                newMax = dfs(idx+1, curSum + (val & (i+1)), curMax)
                curMax = max(newMax, curMax)
                # recordFull[i].remove(val)
                records[i] -= 1
            if not flag:
                # print("ff")
                curMax = max(dfs(idx+1, curSum, curMax), curMax)
            return max(curMax, curSum)

        return dfs(0, 0, 0)
    # from 灵剑2012
    def maximumANDSum2(self, nums: List[int], numSlots: int) -> int:
        ans = 0
        @lru_cache(None)
        def search(state, idx, curSum):
            # 这里用 state 压缩表示存储情况
            nonlocal ans
            if idx >= len(nums):
                ans = max(ans, curSum)
                return
            for j in range(numSlots):
                c = (state >> (2 * j)) & 3
                if c < 2:
                    state2 = (state & ~(3 << (2 * j))) | ((c + 1) << (2 * j))
                    search(state2, idx + 1, curSum + (nums[idx] & (j + 1)))

        search(0, 0, 0)
        return ans

    def maximumANDSum3(self, nums: List[int], numSlots: int) -> int:
        ans = 0
        f = [0] * (1 << (numSlots * 2))
        for i, fi in enumerate(f):
            c = bin(i).count("1")
            if c >= len(nums):
                continue
            for j in range(numSlots * 2):
                if (i & (1 << j)) == 0:
                    s = i | (1 << j)
                    f[s] = max(f[s], fi + ((j // 2 + 1) & nums[c]))
                    ans = max(ans, f[s])
        return ans

    def maximumANDSum(self, nums: List[int], numSlots: int) -> int:
        pass
        # dp = [0] * (1 << (2*numSlots))
        # state = 0
        # for num in nums:

sol = Solution()
rels = [
    # sol.countOperations(num1 = 2, num2 = 3),
    # sol.minimumOperations(nums = [3,1,3,2,4,3]),
    # sol.minimumOperations(nums = [1,2,2,2,2]),
    # sol.minimumOperations([2,2]),
    # sol.minimumRemoval(beans = [2,10,3,2]),
    sol.maximumANDSum(nums = [1,2,3,4,5,6], numSlots = 3),
    sol.maximumANDSum(nums = [1,3,10,4,7,1], numSlots = 9),
    # 大一个真的差了好多……
    sol.maximumANDSum([14,7,9,8,2,4,11,1,9], 8),
    sol.maximumANDSum([8,13,3,15,3,15,2,15,5,7,6], 8)
]
for r in rels:
    print(r)
