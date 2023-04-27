from typing import List, Optional
import collections
import math
import bisect
import heapq
import functools, itertools
# from functools import lru_cache
# import sys, os
# sys.setrecursionlimit(10000)
from utils_leetcode import (
    testClass,
)
from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 1991. 找到数组的中间位置 / 0724. 寻找数组的中心下标
    """
    def findMiddleIndex(self, nums: List[int]) -> int:
        # n = len(nums)
        # cumsum = nums[:]
        # for i in range
        s = sum(nums)
        cumsum = 0
        for i in range(len(nums)):
            if cumsum == s-cumsum-nums[i]:
                return i
            cumsum += nums[i]
        return -1
    
    """ 1992. 找到所有的农场组
找到一个 grid 中的所有矩形, 矩形之间满足不相邻

思路: 模拟
"""
    def findFarmland(self, land: List[List[int]]) -> List[List[int]]:
        m,n = len(land), len(land[0])
        farms = []
        lastLine = []
        for i in range(m):
            j = 0
            while j < n:
                if j in lastLine or land[i][j] == 0: 
                    j += 1
                    continue
                jj = j
                while j+1 < n and land[i][j+1]==1: j += 1
                ii = i
                while ii+1 < m and land[ii+1][j]==1: ii += 1
                farms.append((i,jj,ii,j))
                j += 1
            lastLine = [a for a,x in enumerate(land[i]) if x==1]
        return farms
    
    """ 1993. 树上的操作
需要构建一种树结构, 能够实现 Lock, Unlock, Upgrade 操作. 其中 Lock, Unlock 操作针对单个节点比较 naive.
Upgrade(node, user) 操作要求满足: 1) 节点及其祖先节点未上锁, 2) 其孩子节点至少有一个上锁.

思路: 对于节点维护 parent, children, lockUser 属性, 在 Upgrade 操作中向上向下分别遍历检查条件.

输入：
["LockingTree", "lock", "unlock", "unlock", "lock", "upgrade", "lock"]
[[[-1, 0, 0, 1, 1, 2, 2]], [2, 2], [2, 3], [2, 2], [4, 5], [0, 1], [0, 1]]
输出：
[null, true, false, true, true, true, false]

解释：
LockingTree lockingTree = new LockingTree([-1, 0, 0, 1, 1, 2, 2]);
lockingTree.lock(2, 2);    // 返回 true ，因为节点 2 未上锁。
                           // 节点 2 被用户 2 上锁。
lockingTree.unlock(2, 3);  // 返回 false ，因为用户 3 无法解锁被用户 2 上锁的节点。
lockingTree.unlock(2, 2);  // 返回 true ，因为节点 2 之前被用户 2 上锁。
                           // 节点 2 现在变为未上锁状态。
lockingTree.lock(4, 5);    // 返回 true ，因为节点 4 未上锁。
                           // 节点 4 被用户 5 上锁。
lockingTree.upgrade(0, 1); // 返回 true ，因为节点 0 未上锁且至少有一个被上锁的子孙节点（节点 4）。
                           // 节点 0 被用户 1 上锁，节点 4 变为未上锁。
lockingTree.lock(0, 1);    // 返回 false ，因为节点 0 已经被上锁了。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/operations-on-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
    def testLockingTree(self):
        inputs = """["LockingTree","upgrade","upgrade","unlock","lock","upgrade"]
[[[-1,0,3,1,0]],[4,5],[3,8],[0,7],[2,7],[4,6]]"""
        inputs = """["LockingTree","upgrade","upgrade","upgrade","upgrade","unlock","unlock","upgrade","upgrade","upgrade","lock","lock","upgrade","upgrade","unlock","upgrade","upgrade","upgrade","upgrade","unlock","unlock"]
[[[-1,6,5,5,7,0,7,0,0,6]],[5,3],[2,3],[7,39],[1,32],[5,44],[2,15],[1,11],[1,18],[3,7],[5,36],[5,42],[8,5],[1,19],[3,38],[0,27],[4,11],[9,2],[8,41],[5,36],[7,29]]"""
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            print(getattr(class_name, method_name)(*arg))


    """ 1994. 好子集的数目
给定一组数字, 都不大于30. 求满足条件的所有子集的数量, 条件为: 子集中所有数字的乘积可以 = 不同的质数的乘积.
 
输入：nums = [4,2,3,15]
输出：5
解释：好子集为：
- [2]：乘积为 2 ，可以表示为质数 2 的乘积。
- [2,3]：乘积为 6 ，可以表示为互不相同质数 2 和 3 的乘积。
- [2,15]：乘积为 30 ，可以表示为互不相同质数 2，3 和 5 的乘积。
- [3]：乘积为 3 ，可以表示为质数 3 的乘积。
- [15]：乘积为 15 ，可以表示为互不相同质数 3 和 5 的乘积。
 
[here](https://leetcode-cn.com/problems/the-number-of-good-subsets/solution/hao-zi-ji-de-shu-mu-by-leetcode-solution-ky65/)
由于数字都比较小, 可以罗列所有的质数 primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
对于一组数字, 它们所用到的质数可以通过状态压缩来表示, 即 01 表示以上10个质数用到了哪几个, 记为 mask
考虑 DP: 用 dp[i][mask] 表示只使用数字 2~i, 并且所用的数字质数为 mask, 这样的子集的数量.
状态转移方程: 若 数字i本身包含平方因子, 例如 4, 12 等, 则该数字无法采用, dp[i][mask] = dp[i-1][mask];
否则, 假设i包含的质数组合为 subset, 则 dp[i][mask] = dp[i-1][mask] + dp[i-1][mask\subset] * freq[i], 其中的 subset 必然是 mask 的子集, mask\subset 可以异或得到
因此, 从 i=2开始遍历到 30, 最后的结果即 sum(dp[30][1:])
需要注意的是数字 1, 其可以取任意数量, 因此初始化 df[1][0] = 2**freq[1]
"""
    def numberOfGoodSubsets(self, nums: List[int]) -> int:
        MOD = 10**9+7
        
        primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        maskLimit = 1 << len(primes)
        def num2mask(num):
            """ 将数字转换为掩码, 返回 -1 表示 num 不是不同质数的乘积 """
            mask = 0
            for i, prime in enumerate(primes):
                if num % prime == 0:
                    mask += 1 << i
                    num //= prime
            if num != 1:
                return -1
            return mask
        # print(num2mask(10), num2mask(4))
        freq = collections.Counter(nums)
        
        """ dp[i][mask] 表示用 <=i 的数字, 并且「好子集」组合成 mask 的方式的个数
        滚动DP, 这里初始化从 2 开始 (因为 1 不是好子集)"""
        dp = [0] * maskLimit
        dp[0] = 1 # mask=0 表示没有其他数字, 为了下面的 freq[i] * dp[j ^ m] 式子计算的一致性, 初始化为 1
        dp[num2mask(2)] = freq[2]
        # 从 3-30 开始遍历
        for i in range(3, 31):
            newDP = dp[:]
            # newDP[0] = 1
            m = num2mask(i)
            # m == -1 表示数字 i 不是不同质数的乘积
            if m == -1: continue
            for j in range(1, maskLimit):
                if (j & m) == m:
                    newDP[j] += freq[i] * dp[j ^ m]
            dp = newDP
        # 注意数字 1 可以有任意个, 但是总体的乘积不能为 1
        return sum(dp[1:]) * 2**freq[1] % MOD

class Node:
    def __init__(self, id, parent=None) -> None:
        self.id = id
        self.parent = parent
        self.children = []
        self.lockUser = None

class LockingTree:
    """ 
["LockingTree", "lock", "unlock", "unlock", "lock", "upgrade", "lock"]
[[[-1, 0, 0, 1, 1, 2, 2]], [2, 2], [2, 3], [2, 2], [4, 5], [0, 1], [0, 1]]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/operations-on-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
    def __init__(self, parent: List[int]):
        self.id2node = {}
        self.root = Node(-1, None)
        self.id2node[-1] = self.root
        for i in range(len(parent)):
            self.id2node[i] = Node(i)
        for i,p in enumerate(parent):
            node = self.id2node[i]
            node.parent = self.id2node[p]
            self.id2node[p].children.append(node)

    def lock(self, num: int, user: int) -> bool:
        if self.id2node[num].lockUser is not None:
            return False
        self.id2node[num].lockUser = user
        return True

    def unlock(self, num: int, user: int) -> bool:
        if self.id2node[num].lockUser != user:
            return False
        self.id2node[num].lockUser = None
        return True

    def upgrade(self, num: int, user: int) -> bool:
        node = self.id2node[num]
        # 条件1: 未上锁
        if node.lockUser is not None:
            return False
        # 条件2: 祖先未上锁
        p = node.parent
        while p != self.root:
            if p.lockUser is not None:
                return False
            p = p.parent
        # 条件3: 孩子有上锁
        def bfs(node: Node):
            hasLockedChild = False
            q = collections.deque(node.children)
            while q:
                n = q.popleft()
                if n.lockUser is not None:
                    hasLockedChild = True
                    n.lockUser = None
                q.extend(n.children)
            return hasLockedChild
        hasLockedChild = bfs(node)
        if not hasLockedChild:
            return False
        node.lockUser = user
        return True

sol = Solution()
result = [
    # sol.findMiddleIndex(nums = [2,3,-1,8,4]),
    # sol.findFarmland(land = [[1,0,0],[0,1,1],[0,1,1]]),
    
    sol.testLockingTree(),
    
    # 6, 5
    # sol.numberOfGoodSubsets(nums = [1,2,3,4]),
    # sol.numberOfGoodSubsets(nums = [4,2,3,15]),
    # sol.numberOfGoodSubsets([18,28,2,17,29,30,15,9,12]), # 19
]
for r in result:
    print(r)
