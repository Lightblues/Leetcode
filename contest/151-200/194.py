from easonsi import utils
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
https://leetcode.cn/contest/weekly-contest-194
T2 细节较多; T3的复杂度比较玄学, 感觉官答也不太清楚; T4要求最小生成树的「关键边」, 比较高级的内容了.

@2022 """
class Solution:
    """ 1486. 数组异或操作 """
    
    """ 1487. 保证文件名唯一 #medium #细节
顺序来一系列的文件名创建请求. 若文件已经创建过, 则修改为 `name(1)` 这种形式. 要求模拟返回的结果.
注意: 可能会有 `["gta","gta(1)","gta"]` 这样的序列. 因此, 对于新生成的文件名也需要检查是否占用.
"""
    def getFolderNames(self, names: List[str]) -> List[str]:
        cnt = Counter()
        ans = []    # 记录basename下一个括号内待添入的数字.
        for name in names:
            if name not in cnt:
                ans.append(name); cnt[name] = 1
            else: 
                # 尝试添加后缀
                target = f"{name}({cnt[name]})"
                while target in cnt:
                    cnt[name] += 1
                    target = f"{name}({cnt[name]})"
                    # cnt[target] += 1
                ans.append(target); cnt[name] += 1; cnt[target] = 1
        return ans
    
    """ 1488. 避免洪水泛滥 #medium #题型
有无限个湖泊, 给定一个数组表示晴雨, 若值=0说明那天是晴天, 否则第i个湖泊会装满水. 若雨下在装满水的湖泊, 则发生洪水. 你可以在晴天抽干一个湖泊. 目标是不发生洪水, 给出一个抽水的策略. 限制: 数组长度 n 1e5
思路1: 顺序记录晴天的每个日期, 在发生洪水的日期范围内 #二分 搜索晴天.
    注意, 例如 [0,2,2] 虽然前面有一个抽水机会, 但不在两次下雨的日期范围内.
    复杂度: 若使用数组, 可能每次都需要移除第一个元素, 则这样的复杂度为 `O(n^2)`. 若采用有序数组, 则 `O(n logn)`.
"""
    def avoidFlood(self, rains: List[int]) -> List[int]:
        full = {}   # 记录每个湖泊的满水时间
        clouds = []
        ans = [-1] * len(rains)
        for i,pool in enumerate(rains):
            if pool==0: clouds.append(i)
            else:
                if pool in full:
                    # 在上一次被填满的日期之后搜索晴天
                    idx = bisect_right(clouds, full[pool])
                    if idx >= len(clouds): return []        # 无法操作, 返回 []
                    else: ans[clouds[idx]] = pool; clouds.pop(idx)
                # 注意, 只要那天下雨了, 都要更新full
                full[pool] = i
        # 剩余的随便填
        for c in clouds:
            ans[c] = 1
        return ans
    
    
    """ 1489. 找到最小生成树里的关键边和伪关键边 #hard #题型 #kruskal
给定一张带权图, 要求返回「关键边」和「伪关键边」, 也即必须出现在 #最小生成树 上的边, 和存在某一棵最小生成树其中包含的边. 限制: 节点数量 n 100; 边数量 m 200
提示:
    如何最小生成树? 可以采用 #kruskal 算法, 也即从小到大枚举边. 假设已经排好序, 复杂度 `O(m *a)`. 其中a是判断两个节点是否在同一个连通分量的复杂度, 例如用优化的 #并查集 就是 阿克曼函数的反函数.
    如何判断是否为「关键边」? 删去后再运行kruskal, 看是否还能生成最小生成树.
    如何判断是否为「伪关键边」? 首先将该边加入集合, 看是否能生成最小值.
思路1: 先求出不带约束的最小生成树值 mn. 然后便利每一条边, 根据提示判断是否为 (伪)关键边.
    1.1 可以写一个 `kruskal(forbid=set(), pre:int=-1)` 的函数
    1.2 借助通用的并查集实现, 可以方便地对于 kruskal 进行修改, 见官答
    复杂度: O(m^2 *a)
    细节: 如何判断是否全联通? 一种思路是维护每一个分支的大小, 但有一些细节判断 (见1.1); 但这里可以直接用一个数字 setCount 记录当前连通分量的数量.
思路2: 利用 #kruskal 算法的性质 和 #连通性 性质 #hardhard
    提示: 1) **对于kruskal算法, 当遍历完所有权重小于等于x的边之后, 「对应的并查集的连通性是唯一确定的，无论我们在排序时如何规定权值相同的边的顺序」**. 也即联通分量的数量, 每个分量所包含的节点是唯一的.
    因此, 我们可以根据权重大小一层一层往外看. 对于权重都为w的边, 1) 假如两个点在同一个联通分量上, 则为不相关的边; 2) 如何判断 关键/伪关键边? 注意到, **把相关的节点看成一张图, 则关键边对应的是其中的「桥边」**. 可采用 #Tarjan 算法得到.
    复杂度: 最慢的是排序, O(m logm)
[官答](https://leetcode.cn/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/solution/zhao-dao-zui-xiao-sheng-cheng-shu-li-de-gu57q/).
"""
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        # 1.1 可以写一个 `kruskal(forbid=set(), pre:int=-1)` 的函数
        # kruskal 的实现决定了对于 n=2 需要特判.
        if n==2: return [[0], []]
        # 对边排序
        edges = [e+[i] for e,i in zip(edges, range(len(edges)))]
        edges.sort(key=lambda x: x[2])
        def kruskal(forbid=set(), pre:int=-1) -> int:
            # 并查集
            fa = list(range(n))
            sz = [1] * n
            def find(x):
                if fa[x]!=x:
                    fa[x] = find(fa[x])
                return fa[x]
            def merge(x,y):
                fx,fy = find(x),find(y)
                if fx==fy: return
                if fx<fy: fx,fy = fy,fx
                fa[fx] = fy; sz[fy] += sz[fx]
                return sz[fy]
            # 枚举边.
            ans = 0
            if pre!=-1:
                forbid.add(pre)
                e = edges[pre]
                ans += e[2]
                merge(e[0],e[1])
            for i,(u,v,w,idx) in enumerate(edges):
                if i in forbid: continue
                if find(u)==find(v): continue
                else: 
                    ans += w; ss = merge(u,v)
                    if ss==n: return ans
            if sz[find(0)]!=n: return -1
        
        mn = kruskal()
        key, pseudo = [], []
        for i,e in enumerate(edges):
            # 若加入该边不能得到mn, 说明不是(伪)关键边
            if kruskal(pre=i, forbid=set())!=mn: continue
            if kruskal(forbid=set([i]))!=mn: key.append(e[3])
            else: pseudo.append(e[3])
        return [key, pseudo]
    
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        # 将并查集写成类以供复用, 就不用写成上面的复杂 kruskal 了.
        m = len(edges)
        for i, edge in enumerate(edges):
            edge.append(i)
        edges.sort(key=lambda x: x[2])

        # 计算 value
        uf_std = UnionFind(n)
        value = 0
        for i in range(m):
            if uf_std.unite(edges[i][0], edges[i][1]):
                value += edges[i][2]

        ans = [list(), list()]
        
        for i in range(m):
            # 判断是否是关键边
            uf = UnionFind(n)
            v = 0
            for j in range(m):
                if i != j and uf.unite(edges[j][0], edges[j][1]):
                    v += edges[j][2]
            if uf.setCount != 1 or (uf.setCount == 1 and v > value):
                ans[0].append(edges[i][3])
                continue

            # 判断是否是伪关键边
            uf = UnionFind(n)
            uf.unite(edges[i][0], edges[i][1])
            v = edges[i][2]
            for j in range(m):
                if i != j and uf.unite(edges[j][0], edges[j][1]):
                    v += edges[j][2]
            if v == value:
                ans[1].append(edges[i][3])
      
        return ans

    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        # 时间复杂度: 最慢的是排序, O(m logm)
        m = len(edges)
        for i, edge in enumerate(edges):
            edge.append(i)
        edges.sort(key=lambda x: x[2])

        uf = UnionFind(n)
        ans0 = list()
        label = [0] * m     # 记录每个边是否被添加过

        i = 0
        while i < m:
            # 找出所有权值为 w 的边，下标范围为 [i, j)
            w = edges[i][2]
            j = i
            while j < m and edges[j][2] == edges[i][2]:
                j += 1

            # 存储每个连通分量在图 G 中的编号
            compToId = dict()
            # 图 G 的节点数
            gn = 0
            
            for k in range(i, j):
                x = uf.findset(edges[k][0])
                y = uf.findset(edges[k][1])
                if x != y:
                    if x not in compToId:
                        compToId[x] = gn
                        gn += 1
                    if y not in compToId:
                        compToId[y] = gn
                        gn += 1
                else:
                    # 将自环边标记为 -1
                    label[edges[k][3]] = -1
            
            # 图 G 的边
            gm = collections.defaultdict(list)
            gmid = collections.defaultdict(list)
            
            for k in range(i, j):
                x = uf.findset(edges[k][0])
                y = uf.findset(edges[k][1])
                if x != y:
                    idx, idy = compToId[x], compToId[y]
                    gm[idx].append(idy)
                    gmid[idx].append(edges[k][3])
                    gm[idy].append(idx)
                    gmid[idy].append(edges[k][3])

            bridges = TarjanSCC(gn, gm, gmid).getCuttingEdge()
            # 将桥边（关键边）标记为 1
            ans0.extend(bridges)
            for iden in bridges:
                label[iden] = 1

            for k in range(i, j):
                uf.unite(edges[k][0], edges[k][1])
            
            i = j

        # 未标记的边即为非桥边（伪关键边）
        ans1 = [i for i in range(m) if label[i] == 0]

        return [ans0, ans1]


# 并查集模板
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.n = n
        # 当前连通分量数目
        self.setCount = n
    
    def findset(self, x: int) -> int:
        if self.parent[x] == x:
            return x
        self.parent[x] = self.findset(self.parent[x])
        return self.parent[x]
    
    def unite(self, x: int, y: int) -> bool:
        x, y = self.findset(x), self.findset(y)
        if x == y:
            return False
        if self.size[x] < self.size[y]:
            x, y = y, x
        self.parent[y] = x
        self.size[x] += self.size[y]
        self.setCount -= 1
        return True
    
    def connected(self, x: int, y: int) -> bool:
        x, y = self.findset(x), self.findset(y)
        return x == y


# Tarjan 算法求桥边模版
class TarjanSCC:
    def __init__(self, n: int, edges: List[List[int]], edgesId: List[List[int]]):
        self.n = n
        self.edges = edges
        self.edgesId = edgesId
        self.low = [-1] * n
        self.dfn = [-1] * n
        self.ans = list()
        self.ts = -1
    
    def getCuttingEdge(self) -> List[int]:
        # Tarjan 算法
        for i in range(self.n):
            if self.dfn[i] == -1:
                self.pGetCuttingEdge(i, -1)
        return self.ans
    
    def pGetCuttingEdge(self, u: int, parentEdgeId: int):
        self.ts += 1
        self.low[u] = self.dfn[u] = self.ts
        for v, iden in zip(self.edges[u], self.edgesId[u]):
            if self.dfn[v] == -1:
                self.pGetCuttingEdge(v, iden)
                self.low[u] = min(self.low[u], self.low[v])
                if self.low[v] > self.dfn[u]:
                    self.ans.append(iden)
            elif iden != parentEdgeId:
                self.low[u] = min(self.low[u], self.dfn[v])

    
    
sol = Solution()
result = [
    # sol.getFolderNames(["gta","gta(1)","gta","avalon"]),
    # sol.getFolderNames(["wano","wano","wano","wano"]),
    # sol.avoidFlood(rains = [1,2,3,4]),
    # sol.avoidFlood(rains = [1,2,0,0,2,1]),
    # sol.avoidFlood(rains = [0,1,1]),
    # sol.avoidFlood([1,0,2,0,3,0,2,0,0,0,1,2,3]),
    sol.findCriticalAndPseudoCriticalEdges(n = 5, edges = [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]),
    sol.findCriticalAndPseudoCriticalEdges(n = 4, edges = [[0,1,1],[1,2,1],[2,3,1],[0,3,1]]),
    sol.findCriticalAndPseudoCriticalEdges(n=2, edges=[[0,1,1]]),
]
for r in result:
    print(r)
