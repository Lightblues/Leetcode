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
https://leetcode.cn/contest/weekly-contest-320
T2看似考了二叉搜索树但实际上需要二分; T3 的DFS需要一定转换; T4 的DP写了好久好久... 这次难度还是有点高的

@2022 """
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ 6241. 数组中不等三元组的数目 #easy 
思路1: #暴力 因为只要求每个数字不同, 暴力枚举即可. 注意下面用Counter无法降低复杂度 O(n^3)
思路2: 统计每个数字作为中间值的次数 见 [灵神](https://leetcode.cn/problems/number-of-unequal-triplets-in-array/solution/fei-bao-li-zuo-fa-by-endlesscheng-9ekp/)
"""
    def unequalTriplets(self, nums: List[int]) -> int:
        cnts = list(Counter(nums).values())
        n = len(cnts)
        ans = 0
        for i in range(n):
            for j in range(i+1,n):
                for k in range(j+1,n):
                    ans += cnts[i] * cnts[j] * cnts[k]
        return ans
    def unequalTriplets(self, nums: List[int]) -> int:
        nums.sort()
        ans = start = 0
        for i, (x, y) in enumerate(itertools.pairwise(nums)):
            if x != y:
                ans += start * (i - start + 1) * (len(nums) - 1 - i)
                start = i + 1
        return ans

    """ 6242. 二叉搜索树最近节点查询 #medium 对于二叉树执行q次查询, 返回最近的两个值要求 left<=v<=right, 不存在则返回 -1
注意, 本题本题的二叉树可能是一条链! 这样在树上二分可能过不了! 见 [灵神](https://leetcode.cn/problems/closest-nodes-queries-in-a-binary-search-tree/solution/zhong-xu-bian-li-er-fen-cha-zhao-by-endl-m8ez/)
思路1: 展开成数组, 二分查找 #bisect
"""
    def closestNodes(self, root: Optional[TreeNode], queries: List[int]) -> List[List[int]]:
        # 思路0: 直接对于树二分, 居然 TLE
        def q(root: TreeNode, v):
            # get the closest values [left, right]
            if not root: return -1, -1
            if root.val == v: return v, v
            if root.val>v: 
                r = root.val
                l,rr = q(root.left, v)
                if rr!=-1 and rr<r: r = rr
            else: 
                l = root.val
                ll,r = q(root.right, v)
                if ll!=-1 and ll>l: l = ll
            return l,r
        return [q(root, v) for v in queries]
    def closestNodes(self, root: Optional[TreeNode], queries: List[int]) -> List[List[int]]:
        # 思路1: 展开成数组, 二分查找 #bisect
        vals = []
        def f(root:TreeNode):
            if root:
                vals.append(root.val)
                f(root.left); f(root.right)
        f(root)
        vals.sort()
        n = len(vals)
        def q(v):
            idx = bisect_left(vals, v)
            if idx == n: return vals[-1], -1
            if vals[idx]==v: return v, v
            if idx == 0: return -1, vals[0]
            else: return vals[idx-1], vals[idx]
        return [list(q(v)) for v in queries]
    
    """ 6243. 到达首都的最少油耗 #medium 一个树结构, 其他点都有一个人要到达root; 每辆车可以坐seats个人, 问最小的代价多少
思路1: #DFS, 从叶子节点往root走, 统计需要往上走的人数, 这一个节点的代价就是 `ceil(nperson/seats)`
"""
    def minimumFuelCost(self, roads: List[List[int]], seats: int) -> int:
        # 树结构建图
        n = len(roads)+1
        g = [[] for _ in range(n)]
        for u,v in roads:
            g[u].append(v)
            g[v].append(u)
        # 树结构遍历的框架, 直接传入 parent节点即可避免重复访问
        def dfs(u, p):
            nonlocal cost
            nperson = 1
            for v in g[u]:
                if v == p: continue
                nperson += dfs(v, u)
            # 排除跟节点
            if u!=0:
                cost += ceil(nperson/seats)
            return nperson
        cost = 0
        dfs(0, -1)
        return cost
    
    
    """ 6244. 完美分割的方案数 #hard 对于一个数字字符串, 定义其参数 (k,minL) 的「完美分割」为, 将字符串分成k个子串, 最小长度为minL, 并且每个子串以质数数字开头非质数数字结尾
限制: n,k,minL 1e3. 对结果取模
思路1: #DP
    用1/0标记质数/非质数数字, 则符合要求的子串形式是 p=`1...100` 这样的, 还要满足最小长度约束, 因此可以是两个这样的pattern拼接.
    等价问题: 对于一组满足pattern的字符串, 分割成k组, 符合minL要求. 问分割方案数. 这里重要的只是子串长度.
    DP: 定义 `f[i,j]` 表示前i个子串分成j组的方案数, 则有 `f[i,j] = sum{ f[ii,j-1] }`. 这里要求最后一个串满足要求, 也即 sum(ii+1...i)>=minL
        但是这样的复杂度是O(n^3), 要优化.
        注意到, 假如 ii=x 满足要求, 则ii=x-1,x-2... 也一定满足, 因此可以对于f计算前缀和!
参见 [灵神](https://leetcode.cn/problems/number-of-beautiful-partitions/solution/dong-tai-gui-hua-jian-ji-xie-fa-xun-huan-xyw3/)
"""
    def beautifulPartitions(self, s: str, k: int, minLength: int) -> int:
        mod = 10**9+7
        # 转化为等价问题
        ps = "2357"
        if s[0] not in ps or s[-1] in ps: return 0
        s = ''.join(['1'if c in ps else '0' for c in s])
        # 直接用re来匹配, 更方便
        arr = list(map(len, re.findall(r'1+0+', s)))

        # DP
        n = len(arr)
        f = [[0]*(k+1) for _ in range(n+1)]
        facc= [[0]*(k+1) for _ in range(n+1)]
        for i in range(n):
            # 找到满足 minL条件的最后一个串: sum(ii...i) >=minLength
            ii = i
            cc = arr[ii]
            while ii>0 and cc<minLength:    # 注意这里ii的边界
                ii -= 1
                cc += arr[ii]; 
            if cc<minLength: continue
            # 边界:分成1组
            f[i+1][1] = 1
            facc[i+1][1] = facc[i][1]+1
            # 分成多组
            for j in range(2, k+1):
                f[i+1][j] = facc[ii][j-1]
                facc[i+1][j] = (facc[i][j] + f[i+1][j]) % mod
            # naive写法, TLE O(n^3)
            # for j in range(2, k+1):
            #     cc = 0
            #     for ii in range(i,-1,-1):
            #         cc += arr[ii]
            #         if cc>=minLength:
            #             f[i+1][j] = (f[i+1][j] + f[ii][j-1]) % mod
            #             f[i+1][j] = (f[i+1][j] + f[ii][j-1]) % mod
        return f[n][k]
    
sol = Solution()
result = [
    # sol.unequalTriplets(nums = [4,4,2,4,3]),
    # sol.unequalTriplets([1,1,1,1,1,1]),
    # sol.minimumFuelCost(roads = [[3,1],[3,2],[1,0],[0,4],[0,5],[4,6]], seats = 2),
    # sol.minimumFuelCost(roads = [[0,1],[0,2],[0,3]], seats = 5),
    # sol.minimumFuelCost(roads = [], seats = 1),
    sol.beautifulPartitions(s = "23542185131", k = 3, minLength = 2),
    sol.beautifulPartitions(s = "23542185131", k = 3, minLength = 3),
    sol.beautifulPartitions(s = "3312958", k = 3, minLength = 1),
    sol.beautifulPartitions("783938233588472343879134266968", 4, 6)
]
for r in result:
    print(r)
