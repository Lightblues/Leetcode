from easonsi.util.leetcode import *

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
https://leetcode.cn/contest/weekly-contest-174

T4 难度中等.

@2022 """
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
        
class Solution:
    """ 1337. 矩阵中战斗力最弱的 K 行 """
    def kWeakestRows(self, mat: List[List[int]], k: int) -> List[int]:
        rows = [(sum(row), i) for i,row in enumerate(mat)]
        rows.sort()
        return [i[1] for i in rows[:k]]
    
    """ 1338. 数组大小减半 """
    def minSetSize(self, arr: List[int]) -> int:
        n = len(arr)
        cnt = Counter(arr)
        vals = sorted(cnt.values(), reverse=True)
        acc = 0
        for i,v in enumerate(vals):
            acc += v
            if acc >= n//2: return i+1
    
    """ 1339. 分裂二叉树的最大乘积 #medium 分割一个二叉树的一条边变成两个子树, 要求两个子树的节点和的乘积最大 限制: n 1e5. 每个节点的值 1e4 """
    def maxProduct(self, root: Optional[TreeNode]) -> int:
        # 
        mod = 10**9 + 7
        vals = set()
        def dfs(node):
            if not node: return 0
            v = node.val + dfs(node.left) + dfs(node.right)
            vals.add(v)
            return v
        s = dfs(root)
        return max(v*(s-v) for v in vals) % mod
    
    """ 1340. 跳跃游戏 V #hard 一系列的数字表示每个位置的高度, 跳跃规则为, 允许从i跳到 [i+/-d] 范围内, 要求 [i+1...j] 的元素都 < arr[i] 问最多可以访问多少柱子? 限制: n 1e3; 
思路1: 排序 之后 #遍历.
    考虑简单情况, 连续跳跃的条件是什么? 可以想像一个凸函数往中间跳.
    思路: 对于 (height, i) 递增排序. 
        遍历过程中, 从i往两边找比hight高的柱子, 更新其可跳跃数量.
        注意, 不能遇到第一个高的之后就终止: 因为有k的距离限制. 因此, 需要在遍历过程中维护mx约束.
    复杂度: O(n logn + n*k)
思路2: #记忆化
    `dp[i] = max(dp[j]) + 1`
    复杂度: O(n*k)
[官答](https://leetcode.cn/problems/jump-game-v/solution/tiao-yue-you-xi-v-by-leetcode-solution/)
"""
    def maxJumps(self, arr: List[int], d: int) -> int:
        n = len(arr)
        heights = sorted([(h,i) for i,h in enumerate(arr)])
        maxStep = [1] * n
        for h,i in heights:
            mx = h
            for j in range(i+1, min(i+d+1, n)):
                if arr[j] > mx:
                    maxStep[j] = max(maxStep[j], maxStep[i]+1)
                    mx = arr[j]
            mx = h
            for j in range(i-1, max(i-d-1, -1), -1):
                if arr[j] > mx:
                    maxStep[j] = max(maxStep[j], maxStep[i]+1)
                    mx = arr[j]
        return max(maxStep)
    def maxJumps(self, arr: List[int], d: int) -> int:
        seen = [-1] * len(arr)
        @lru_cache(None)
        def dfs(pos):
            seen[pos] = 1

            i = pos - 1
            while i >= 0 and pos - i <= d and arr[pos] > arr[i]:
                dfs(i)
                seen[pos] = max(seen[pos], seen[i] + 1)
                i -= 1
            i = pos + 1
            while i < len(arr) and i - pos <= d and arr[pos] > arr[i]:
                dfs(i)
                seen[pos] = max(seen[pos], seen[i] + 1)
                i += 1

        for i in range(len(arr)): dfs(i)
        return max(seen)

    
sol = Solution()
result = [
#     sol.kWeakestRows(mat = 
# [[1,1,0,0,0],
#  [1,1,1,1,0],
#  [1,0,0,0,0],
#  [1,1,0,0,0],
#  [1,1,1,1,1]], 
# k = 3),
    sol.maxJumps(arr = [6,4,14,6,8,13,9,7,10,6,12], d = 2),
    sol.maxJumps([83,11,83,70,75,45,96,11,80,75,67,83,6,51,71,64,64,42,70,23,11,24,95,65,1,54,31,50,18,16,11,86,2,48,37,34,65,67,4,17,33,70,16,73,57,96,30,26,56,1,16,74,82,77,82,62,32,90,94,33,58,23,23,65,70,12,85,27,38,100,93,49,96,96,77,37,69,71,62,34,4,14,25,37,70,3,67,88,20,30], 29),
]
for r in result:
    print(r)
