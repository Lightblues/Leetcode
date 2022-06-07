
import bisect
from distutils.command.config import config
from typing import List
import collections
import random
import heapq


""" @220211
https://leetcode-cn.com/contest/weekly-contest-279
 """
class Solution:
    """ 2148. 元素计数
给你一个整数数组 `nums` ，统计并返回在 `nums` 中同时至少具有一个严格较小元素和一个严格较大元素的元素数目。 """
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

    """ 2151. 基于陈述统计最多好人数 """

    """ 尝试一: DFS. 超时
维护两个数组 goods, bads 记录当前状态下的好人和坏人
对于其他人, DFS 讨论这个人是好人或坏人
- 注意, 坏人的情况不需要讨论, 因为坏人没有提供信息 !
- 若假设第 i 个待定的是好人, 需要递归判断其陈述, n^2 复杂度

反思: 两种极端情况
1. 陈述比较稀疏的情况; 
2. 陈述很稠密, 例如所有人都是好人并且都做了陈述, [[2,1,1,1],[1,2,1,1],[1,1,2,1],[1,1,1,2]]
 """
    def maximumGood0(self, statements: List[List[int]]) -> int:
        n = len(statements)
        result = 0
        def dfs(goods, bads, remains):
            nonlocal result
            result = max(result, len(goods))
            if len(remains) == 0:
                return
            for idx,i in enumerate(remains):
                others = remains[:idx] + remains[idx+1:]
                # 1. 坏人, 不需要判断
                # dfs(goods[:], bads + [i], others)
                # 2. 好人
                # 尝试添加第 i 个人为好人
                t = test(goods[:], bads[:], i)
                if t:
                    newGood, newBad = t
                    dfs(newGood, newBad, [i for i in others if i not in newGood + newBad])
        def test(goods, bads, idx):
            # 判断 idx 为好人是否成立, 若成立, 返回 newGood, newBad
            newGood, newBad = goods[:] + [idx], bads[:]
            q = collections.deque([idx])
            while q:
                i = q.popleft()
                for j, val in enumerate(statements[i]):
                    if val == 0:
                        if j in newGood:
                            return False
                        if j not in newBad:
                            newBad.append(j)
                    elif val == 1:
                        if j in newBad:
                            return False
                        if j not in newGood:
                            newGood.append(j)
                            q.append(j)
            return newGood, newBad
        dfs([], [], list(range(n)))
        return result

    """ 回溯, https://leetcode-cn.com/problems/maximum-good-people-based-on-statements/solution/hui-su-san-bu-qu-qing-xi-kuang-jia-by-sh-t7en/
对于每一个人一次判断其为好人或坏人, 和上面的思路大体复杂度应该是一样的?
只是没有用 test() 前向判断, 会快一点? """
    def maximumGood1(self, statements: List[List[int]]) -> int:
        n = len(statements)
        max_total = 0
        def backtracking(statements, player, good, bad): 
            nonlocal max_total
            # base case 终止条件: 遍历结束
            if player == len(statements): 
                max_total = max(len(good), max_total)
                return
            
            # backtracking 
            for i in range(player, n): 
                # prune
                if i in bad:
                    continue 
                
                # 1. i 是好人
                new_good = set(j for j in range(n) if statements[i][j] == 1 and j not in good)
                new_good.add(i)
                new_bad = set(j for j in range(n) if statements[i][j] == 0 and j not in bad)
                
                if not (good.union(new_good)).isdisjoint(bad.union(new_bad)):
                    # prune 
                    pass
                else: 
                    backtracking(statements, player+1, good.union(new_good), bad.union(new_bad))
                
                # 2. i 是坏人
                if i not in bad:
                    bad.add(i)
            
            if good.intersection(bad):
                pass
            else: 
                max_total = max(len(good), max_total)

        backtracking(statements, 0, set(), set())
        return max_total 

    """ 方法一：使用状态压缩枚举所有可能的情况
https://leetcode-cn.com/problems/maximum-good-people-based-on-statements/solution/ji-yu-chen-shu-tong-ji-zui-duo-hao-ren-s-lfn9/
用一个长度为 n 的二进制数 mask 表示好人坏人情况
- s[i][j]=0, i 认为 j 是坏人, 此时 mask 的 (i,1) and (j,1) 是不合法的
- s[i][j]=1, i 认为 j 是好人, 此时 mask 的 (i,1) and (j,0) 是不合法的
- s[i][j]=2, 无信息
因此, 对于 mask 的 1 位, 可以在 n^2 时间内判断是否合法. 枚举得到最大数量
 """
    def maximumGood(self, statements: List[List[int]]) -> int:
        n = len(statements)

        def check(mask):
            for i in range(n):
                # 仅需要检测好人的陈述
                if mask & (1<<i):
                    for j,val in enumerate(statements[i]):
                        if val == 0 and mask & (1<<j):
                            return False
                        elif val == 1 and not mask & (1<<j):
                            return False
            return True
        
        ans = 0
        for mask in range(1, 1 << n):
            if check(mask):
                # bin(43) == '0b101011'
                ans = max(ans, bin(mask).count('1'))
        return ans



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