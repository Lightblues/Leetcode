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
https://leetcode.cn/contest/weekly-contest-397
Easonsi @2023 """
class Solution:
    """ 3146. 两个字符串的排列差 """
    def findPermutationDifference(self, s: str, t: str) -> int:
        c2idxs = {}
        c2idxt = {}
        for i,c in enumerate(s):
            c2idxs[c] = i
        for i,c in enumerate(t):
            c2idxt[c] = i
        ans = 0
        for c in c2idxs:
            ans += abs(c2idxs[c] - c2idxt[c])
        return ans
    
    """ 3147. 从魔法师身上吸取的最大能量 """
    def maximumEnergy(self, energy: List[int], k: int) -> int:
        mx = -inf
        n = len(energy)
        for start in range(n-1,n-k-1,-1):
            acc = 0
            for i in range(start, -1, -k):
                acc += energy[i]
                mx = max(mx, acc)
        return mx
        
    
    """ 3148. 矩阵中的最大得分 #medium 从矩阵某一位置出发, 可以跳到正下或者正右方 分数为 score[new]-score[old]; 可以多次, 求累计分数最大值. 
注意到, 等价于, 从 (i,j) 跳到其右下角矩阵的最大差值! 
    """
    def maxScore(self, grid: List[List[int]]) -> int:
        n,m = len(grid),len(grid[0])
        ans = -inf
        for i in range(n-1,-1,-1):
            for j in range(m-1,-1,-1):
                if i == n-1 and j == m-1: continue
                v = grid[i][j]
                mx = -inf
                if i < n-1: mx = grid[i+1][j]
                if j < m-1: mx = max(mx, grid[i][j+1])
                ans = max(ans, mx-v)
                grid[i][j] = max(v,mx)      # 维护右下角矩阵最大值!
        return ans
    
    """ 3149. 找出分数最低的排列 #hard 对于一个由 range(n) 排列得到数组, 要求其某一排列, 使得 score = sum{ |prem[i]-nums[prem[i+1]| } 最小. (相同的话, 按字典序最小)
限制: n 14
思路1: 
    注意到prem经过左右移算到的分数是一样的! 因此, 答案第一个数字是0! 
    接下来, 如何缩减搜索空间? 注意到前面用掉否一组数字的基础上, 对后面有影响的仅仅是
    二进制表示, 这样DP的函数 f(mask, last) 表示用掉mask集合, 最后一个数字为last的最小分数.
        则有 f(mask, last) = min{ f(mask^1<<i, i) + |last-i| } for i in range(n) if mask & 1<<i
        边界: mask 表示全集的情况下, 分数为 |last-nums[0]|
        入口 f(0,0)
    复杂度: 状态数量 2^n * n, 状态转移 O(n)

关联: 
    见 动态规划题单 中的「§9.2 排列型 ② 相邻相关」。如果觉得本题太难，推荐先从较为容易「§9.1 排列型 ① 相邻无关」开始。
    https://leetcode.cn/circle/discuss/tXLS3i/
    """
    def findPermutation(self, nums: List[int]) -> List[int]:
        n = len(nums)
        @lru_cache(None)        # NOTE: 
        def f(mask, last):
            if mask == (1<<n) - 1:
                return abs(last - nums[0])
            ans = inf
            for i in range(n):
                if (mask>>i) & 1 == 0:  # 未使用
                    ans = min(ans, f(mask|1<<i, i) + abs(last-nums[i]))
            return ans
        return f(0,0)
    # TODO: debug


sol = Solution()
result = [
    # sol.maximumEnergy(energy = [5,2,-10,-5,1], k = 3),
    # sol.maxScore(grid = [[4,3,2],[3,2,1]]),
    # sol.maxScore([[9,5,7,3],[8,9,6,1],[6,7,14,3],[2,5,3,1]]),
    sol.findPermutation(nums = [1,0,2]),
    sol.findPermutation([0,2,1]),
]
for r in result:
    print(r)
