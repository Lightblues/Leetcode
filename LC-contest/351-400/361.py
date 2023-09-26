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
https://leetcode.cn/contest/weekly-contest-361
https://leetcode.cn/circle/discuss/ZzhMI6/


Easonsi @2023 """
class Solution:
    """ 2843. 统计对称整数的数目 #easy 统计在 [left, right] 范围内的, 长度为 2n, 前后n个数字之和相同的数字数量
限制:  right 1e4
    """
    def countSymmetricIntegers(self, low: int, high: int) -> int:
        ans = 0
        for i in range(low, high+1):
            i = str(i)
            if len(i)%2==0:
                if sum(map(int, i[:len(i)//2])) == sum(map(int, i[len(i)//2:])):
                    ans += 1
        return ans
    
    
    """ 2844. 生成特殊数字的最少操作 #medium 对一个数字, 每次可以删去一个数字, 问最少操作多少次可以得到被 25整除的数字? 注意0也合法. 
    
"""
    def minimumOperations(self, num: str) -> int:
        n = len(num)
        # get the right most 00/25/50/75
        def get_most_left(a,b):
            idx = n-1
            while idx>=0 and num[idx]!=b:
                idx -= 1
            idx -= 1
            while idx>=0 and num[idx]!=a:
                idx -= 1
            return -1 if idx<0 else idx
        left = max(
            get_most_left(*x) for x in "00 25 50 75".split()
        )
        # 注意 10 只需要删除1即可
        mn = n if '0' not in num else n-1
        if left!=-1:
            mn = n-left-2
        return mn
    
    """ 2845. 统计趣味子数组的数目 #medium 对于一个连续子数组, 统计满足 nums[i] % modulo == k 的数量为 cnt, 若其本身也满足 cnt % modulo == k 则叫做「趣味子数组」, 求趣味子数组的数量
限制: n 1e5
思路1: 问题转换, #前缀和 + #哈希表
    将数组转换为 0/1 的数组, 则需要统计和为 k, modulo+k, 2modulo+k, ... 的数量
    也即, 记转换后前缀和为s, 则要求 s[r+1]-s[l] % modulo = k, 也即 s[r+1] % modulo = (s[l]+k) % modulo
    因此, 遍历计数即可!

关联: 推荐按照顺序完成
*   [560\. 和为 K 的子数组](https://leetcode.cn/problems/subarray-sum-equals-k/)
*   [974\. 和可被 K 整除的子数组](https://leetcode.cn/problems/subarray-sums-divisible-by-k/)
*   [523\. 连续的子数组和](https://leetcode.cn/problems/continuous-subarray-sum/)
*   [525\. 连续数组](https://leetcode.cn/problems/contiguous-array/)
"""
    def countInterestingSubarrays(self, nums: List[int], modulo: int, k: int) -> int:
        nums = [1 if x%modulo==k else 0 for x in nums] # 转换为 0/1 数组
        cnt = Counter()
        cnt[k] = 1      # 边界
        acc = 0
        ans = 0
        for x in nums:
            acc += x
            ans += cnt[acc%modulo]
            cnt[(acc+k)%modulo] += 1
        return ans
    
    
    """ 2846. 边权重均等查询 #hard 给定一颗二叉树, 有 [1,26] 的边权. 对于每次查询 [a,b], 计算对于a/b的路径, 最少需要修改多少条边权使所有边权一致. 
限制: n 1e4; q 2e4
思路1: #LCA + #DFS #倍增
    问题等价于, 找到最小公共祖先 LCA, 然后看这条路径上面的权值分布. 
    对于LCA, 可以使用 #倍增法 求解, 复杂度 O(logn)
        见下面的模板 LCA
    我们还需要知道从root出发, 到达点a的路径上的边权分布, 下面用了同LCA的DFS来统计! 
    这样, 对于每个查询, 就可以得到它们路径上的边分布 path(a)+path(b)-path(lca), 找到其中的出现次数最大的边权即可. 
    [小羊](https://leetcode.cn/circle/discuss/ZzhMI6/view/vzX1XG/)
    
关联: 
    0236. 二叉树的最近公共祖先 https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/description/
    1483. 树节点的第 K 个祖先 [灵神](https://leetcode.cn/problems/kth-ancestor-of-a-tree-node/solutions/2305895/mo-ban-jiang-jie-shu-shang-bei-zeng-suan-v3rw/)
"""
    def minOperationsQueries(self, n: int, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
        path = [[] for _ in range(n)]
        for u,v,w in edges:
            path[u].append((v,w-1))
            path[v].append((u,w-1))
        lca = LCA(path, 0)
        
        # 记录每个节点对应路径上, 不同权值的边的数量
        x = 26
        vals = [[0]*x for _ in range(n)]
        # DFS
        st = [0]
        while st:
            u = st.pop()
            for v,w in path[u]:
                if v==lca.parent[0][u]: continue
                for i in range(x):
                    vals[v][i] = vals[u][i]
                vals[v][w] += 1
                st.append(v)
        
        ans = []
        for a,b in queries:
            l = lca.getLCA(a,b)
            tmp = [0] * x
            for i in range(x):
                tmp[i] = vals[a][i] + vals[b][i] - 2*vals[l][i]
            ans.append(sum(tmp) - max(tmp))
        return ans

class LCA:
    def __init__(self, g, root) -> None:
        self.n = len(g)
        self.root = root
        self.num = self.n.bit_length()  # 2^num >= n
        self.depth = [0] * self.n       # 记录深度
        # 记录 2^i 级祖先
        self.parent = [[-1] * self.n for _ in range(self.num)]

        # dfs 从root出发构成 parent, depth
        s = [root]
        while s:
            v = s.pop()
            for u,_ in g[v]:        # (u, w)
                if u==self.parent[0][v]: continue
                self.parent[0][u] = v
                self.depth[u] = self.depth[v] + 1
                s.append(u)
        # 构建 2^i 级祖先
        for k in range(self.num-1):
            for v in range(self.n):
                if self.parent[k][v] == -1:
                    self.parent[k+1][v] = -1
                else:
                    self.parent[k+1][v] = self.parent[k][self.parent[k][v]]
        
    def getLCA(self, u,v):
        """ 找到 u,v 的最近公共祖先, 复杂度 O(logn) """
        if self.depth[u] > self.depth[v]:
            u,v = v,u
        # 使得 u 和 v 在同一深度
        for k in range(self.num):
            if (self.depth[v] - self.depth[u]) >> k & 1:
                v = self.parent[k][v]
        # 二分查找 LCA
        if u==v: return u
        for k in range(self.num-1, -1, -1):
            if self.parent[k][u] != self.parent[k][v]:
                u = self.parent[k][u]
                v = self.parent[k][v]
        return self.parent[0][u]

sol = Solution()
result = [
    # sol.countSymmetricIntegers(low = 1200, high = 1230),

    # sol.minimumOperations(num = "2245047"),
    # sol.minimumOperations(num = "10"),
    # sol.minimumOperations(num = "2908305"),
    
    # sol.countInterestingSubarrays(nums = [3,2,4], modulo = 2, k = 1),
    # sol.countInterestingSubarrays(nums = [3,1,9,6], modulo = 3, k = 0),
    
    sol.minOperationsQueries(n = 7, edges = [[0,1,1],[1,2,1],[2,3,1],[3,4,2],[4,5,2],[5,6,2]], queries = [[0,3],[3,6],[2,6],[0,6]]),

]
for r in result:
    print(r)
