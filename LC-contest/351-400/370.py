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
https://leetcode.cn/contest/weekly-contest-370
Easonsi @2023 """
class Solution:
    """ 2923. 找到冠军 I """
    def findChampion(self, grid: List[List[int]]) -> int:
        n = len(grid)
        return list(map(sum, grid)).index(n-1)
    
    """ 2924. 找到冠军 II #medium 对于一个DAG描述的强弱关系, 找到是否存在冠军
思路1: 直接看是否有人没有被赢即可
    """
    def findChampion(self, n: int, edges: List[List[int]]) -> int:
        ava = set(range(n))
        for _,u in edges:
            ava.discard(u)
        if len(ava)==1: return ava.pop()
        else: return -1
    
    """ 2925. 在树上执行操作以后得到的最大分数 #medium #树形DP 给定一棵树, 节点上有分数. 选择部分, 使得从根到叶子的路径之和都不能为0. 问可以得到的最大分数.
限制: n 2e4
思路1: 每个节点返回 (a,b) = (子树满足, 子树不满足/也即分数之和). 
    更新 a = max{ sum(b for childs), sum(a for childs)+node.val }
    """
    def maximumScoreAfterOperations(self, edges: List[List[int]], values: List[int]) -> int:
        n = len(values)
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        def dfs(u, fa):
            val = values[u]
            a, b = 0, 0
            for v in g[u]:
                if v==fa: continue
                a1, b1 = dfs(v, u)
                a += a1
                b += b1
            return max(val+a if b!=0 else 0, b), b+val      # 注意叶子结点
        a,b = dfs(0, -1)
        return a
    
    """ 2926. 平衡子序列的最大和 #hard 要求字序列相邻所选 i,j, 满足 arr[j]-arr[i] >= j-i. 求满足条件的子序列最大和
限制: n 1e5
思路1: 
    问题等价, 变换 b[i] = a[i]-i 要求从b中找到递增子序列, 和最大
    采用 #DP 定义 f[i] 表示最后一个元素为i时候的结果. 
        则有 f[i] = max{ f[j] | j<i, b[j]<=b[i] } + b[i]
        注意, 这里需要「在权值不大于b[i]的范围内找到最大值」, 可以用「权值树状数组/权值线段树」来实现. 
    """
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        if all(x < 0 for x in nums): return max(nums)
        
        n = len(nums)
        vals = sorted(v - i for i, v in enumerate(nums) if v >= 0)
        m = len(vals)
        d = {v: i for i, v in enumerate(vals)}
        # 照道理会比 max 快一丁点儿
        def ma(a, b): return a if a > b else b
        seg = SegTree(ma, 0, m)
        for i, v in enumerate(nums):
            if v >= 0:
                x = seg.prod(0, d[v-i] + 1)
                seg.set(d[v-i], x + v)
        return seg.all_prod()

    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        b = sorted(set(x - i for i, x in enumerate(nums)))  # 离散化 nums[i]-i
        t = BIT(len(b) + 1)
        ans = -inf
        for i, x in enumerate(nums):
            j = bisect_left(b, x - i) + 1  # nums[i]-i 离散化后的值（从 1 开始）
            f = max(t.pre_max(j), 0) + x
            ans = max(ans, f)
            t.update(j, f)
        return ans

class SegTree:
    def __init__(self, op, e, n):
        self.op = op
        self.e = e
        self.n = n
        self.log = (n-1).bit_length()
        self.size = 1 << self.log
        self.d = [e] * (2 * self.size)
    def set(self, p, x):
        p += self.size
        self.d[p] = x
        for i in range(1, self.log + 1):
            self.update(p >> i)
    def prod(self, l, r):
        sml = self.e
        smr = self.e
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                sml = self.op(sml, self.d[l])
                l += 1
            if r & 1:
                r -= 1
                smr = self.op(self.d[r], smr)
            l >>= 1
            r >>= 1
        return self.op(sml, smr)
    def all_prod(self):
        return self.d[1]
    def update(self, k):
        self.d[k] = self.op(self.d[2 * k], self.d[2 * k + 1])

# 树状数组模板（维护前缀最大值）
class BIT:
    def __init__(self, n):
        self.tree = [-inf] * n

    def update(self, i: int, val: int) -> None:
        while i < len(self.tree):
            self.tree[i] = max(self.tree[i], val)
            i += i & -i

    def pre_max(self, i: int) -> int:
        mx = -inf
        while i > 0:
            mx = max(mx, self.tree[i])
            i &= i - 1
        return mx

sol = Solution()
result = [
    # sol.findChampion(grid = [[0,0,1],[1,0,1],[0,0,0]]),

    # sol.maximumScoreAfterOperations(edges = [[0,1],[0,2],[0,3],[2,4],[4,5]], values = [5,2,5,2,1,1]),
    # sol.maximumScoreAfterOperations(edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]], values = [20,10,9,7,4,3,5]),
    
    sol.maxBalancedSubsequenceSum(nums = [3,3,5,6]),
]
for r in result:
    print(r)
