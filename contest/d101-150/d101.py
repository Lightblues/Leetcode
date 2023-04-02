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
https://leetcode-cn.com/contest/biweekly-contest-101


Easonsi @2023 """
class Solution:
    """ 6327. 从两个数字数组里生成最小数字 """
    def minNumber(self, nums1: List[int], nums2: List[int]) -> int:
        ss = set(nums1) & set(nums2)
        if ss: return min(ss)
        a,b = min(nums1), min(nums2)
        a,b = sorted([a,b])
        return a*10+b
    
    """ 6328. 找到最大开销的子字符串 等驾驭「最大子数组」 """
    def maximumCostSubstring(self, s: str, chars: str, vals: List[int]) -> int:
        m = dict(zip(chars, vals))
        for i,ch in enumerate(string.ascii_lowercase):
            if ch not in m:
                m[ch] = i+1
        n = len(s)
        # find the max cost of substring
        mx = 0
        acc = 0
        for i in range(n):
            acc += m[s[i]]
            mx = max(mx, acc)
            if acc<0: acc=0
        return mx
    
    """ 6329. 使子数组元素和相等 #medium #题型 循环数组, 要求所有窗口长k的数组之和都相等. 问最少需要执行加减1操作多少次. 限制: n,k 1e5
思路1: #并查集 #中位数
    注意示例中, (n,k) = (4,3) 的情况下, 四个元素都需要相同; 而例如 (6,4), 则 0,2,4 一组, 1,3,5 一组. 组内元素需要相同
    因此, 核心如何确定这些组的关系? 一个暴力的方法是用 #并查集
    一个子问题: 如何最小化代价, 使得组内元素相等? 显然是 #中位数
    """
    def makeSubKSumEqual(self, arr: List[int], k: int) -> int:
        n = len(arr)
        # 并查集
        fa = list(range(n))
        def find(x):
            if fa[x]!=x:
                fa[x] = find(fa[x])
            return fa[x]
        def union(x,y):
            fa[find(x)] = find(y)
        # 根据滑窗确定组的关系
        for i in range(n):
            x = (i+k) % n
            union(i,x)
        # 分组, 每组中的元素应该相同
        ss = defaultdict(list)
        for i,x in enumerate(arr):
            ss[find(i)].append(x)
        ans = 0
        # get det mediums of each group
        for s in ss.values():
            s = sorted(s)
            mid = s[len(s)//2]
            ans += sum(abs(x-mid) for x in s)
        return ans

    """ 6330. 图中的最短环 #hard #题型 #图 对于给定的无向图, 找最小环的大小. 限制: n,m 1e3
思路1: 「删边法」
    枚举每一条边, 计算删去之后两点的最短路径, 再加上原边现在就是最小环
    复杂度: BFS最短路的复杂度为 O(m+n), 乘以边的数量 O(m)
[图论-最小环](https://zhuanlan.zhihu.com/p/342293693)
        """
    def findShortestCycle(self, n: int, edges: List[List[int]]) -> int:
        # 为了方便删边, 采用 set
        g = [set() for _ in range(n)]
        # build the graph
        for u,v in edges:
            g[u].add(v)
            g[v].add(u)
        def shortest_path(u,v):
            # 利用 BFS 求最短路径
            q = deque([u])
            vis = [False]*n
            vis[u] = True
            d = 0
            while q:
                d += 1
                for _ in range(len(q)):
                    x = q.popleft()
                    for y in g[x]:
                        if y==v: return d
                        if vis[y]: continue
                        vis[y] = True
                        q.append(y)
            return -1
        ans = inf
        # 尝试枚举每一条边
        for u,v in edges:
            g[u].remove(v)
            g[v].remove(u)
            ww = shortest_path(u,v)
            if ww!=-1:
                ans = min(ans, ww + 1)
            g[u].add(v)
            g[v].add(u)
        return ans if ans!=inf else -1
    
sol = Solution()
result = [
    # sol.minNumber(nums1 = [4,1,3], nums2 = [5,7]),
    # sol.minNumber(nums1 = [3,5,2,6], nums2 = [3,1,7]),
    # sol.maximumCostSubstring(s = "adaa", chars = "d", vals = [-1000]),
    # sol.maximumCostSubstring(s = "abc", chars = "abc", vals = [-1,-1,-1]),
    # sol.makeSubKSumEqual(arr = [1,4,1,3], k = 2),
    # sol.makeSubKSumEqual(arr = [2,5,5,7], k = 3),
    sol.findShortestCycle(n = 7, edges = [[0,1],[1,2],[2,0],[3,4],[4,5],[5,6],[6,3]]),
    sol.findShortestCycle(n = 4, edges = [[0,1],[0,2]]),
]
for r in result:
    print(r)
