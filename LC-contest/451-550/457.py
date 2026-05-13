from typing import *
import string
import math
from heapq import heapify, heappop, heappush
from collections import defaultdict
from sortedcontainers import SortedList

"""
https://leetcode.cn/contest/weekly-contest-457
1. 组合考察排序 & 字符串操作
2. 网络分块 + 维护区块最小值
    - 分块: 除了用 1. 并查集; 2. DFS 的好处是天然构建了序号! 更为简单
    - 维护固定区块的 active 集最小值
        1. 通过倒序来不断加入 -- 只需要不断 min
        2. 懒删除堆! 增加的复杂度很低
3. 计算联通分量的变化 -- 标准 并查集
4. 规定行动方式的格点跳转 -- 逆向思维 (本质上就理清条件!)
Easonsi @2026 """


class Solution:
    """ 3606. 优惠券校验器 
https://leetcode.cn/problems/coupon-code-validator/solutions/3716401/mo-ni-pythonjavacgo-by-endlesscheng-xqv4/
"""
    def validateCoupons(self, code: List[str], businessLine: List[str], isActive: List[bool]) -> List[str]:
        s_valid_code = set(string.ascii_letters) | set(string.digits) | set(["_"])
        valid = []
        for c,b,a in zip(code, businessLine, isActive):
            if not a: continue
            if b not in ("electronics", "grocery", "pharmacy", "restaurant"): continue
            if c and set(c).issubset(s_valid_code): valid.append((b, c))
        valid.sort()
        return [v[1] for v in valid]

    """ 3607. 电网维护
对于 c 个节点 n 条边的电网, 执行若干操作: 1. 检查 x 站, 若在线则返回; 否则返回其所在网络中在线的最小那个; 2. 将 x 离线.
限制: c,n 1e5; q 2e5
分解为两部分: 维护电网关系; 检查最小在线设备
- 构建连接关系:
    思路 1: #并查集 Union-Find / Disjoint Set Union
    思路 2: 直接建图 DFS
- 检查最小在线
    思路 1: 暴力 #有序数组 复杂度 O(q logn)
    思路 2: #倒序 维护每个group里面最小的在线设备
        注意: 一台可以被多次下线, 需要先正序求最早在线状态
        复杂度: O(q)
    思路 3: #懒删除堆
        复杂度: O(q logc); 另外 heapify 操作可能是 c 或者 c logc
https://leetcode.cn/problems/power-grid-maintenance/solutions/3716402/dfs-lan-shan-chu-dui-pythonjavacgo-by-en-17gb/
"""
    def processQueries(self, c: int, connections: List[List[int]], queries: List[List[int]]) -> List[int]:
        # 并查集
        fa = list(range(c+1))
        def find(x: int) -> int:
            # find the root
            root = x
            while fa[root] != root:
                root = fa[root]
            # update (路径压缩)
            while fa[x] != x:
                fa[x], x = root, fa[x]
            return root
        def join(x: int, y: int):
            fa[find(x)] = find(y)
        for x,y in connections:
            join(x,y)
        # 暴力 #有序数组
        # x_to_g = {}
        # g_sl = defaultdict(SortedList)
        # for x in range(1, c+1):
        #     g = find(x)
        #     g_sl[g].add(x)
        #     x_to_g[x] = g
        # ans = []
        # offline_s = set()
        # for op, x in queries:
        #     if op==1:
        #         if x not in offline_s: ans.append(x)
        #         elif len(g_sl[x_to_g[x]]): ans.append(g_sl[x_to_g[x]][0])
        #         else: ans.append(-1)
        #     else:
        #         offline_s.add(x)
        #         g_sl[x_to_g[x]].discard(x)
        # return ans

        # 2. 逆序
        x_to_g = [-1] * (c+1)
        for x in range(1, c+1):
            x_to_g[x] = find(x)
        first_offline = [math.inf] * (c+1)  # 记录每个节点的离线时间，初始为无穷大（始终在线
        for i,(op,x) in enumerate(queries):
            if op==2 and first_offline[x] == math.inf: 
                first_offline[x] = i
        ans = []
        g_min = defaultdict(lambda: math.inf)  # 每组中的最小在线号数
        for i in range(1, c+1):
            if first_offline[i] == math.inf:
                g = x_to_g[i]
                g_min[g] = min(g_min[g], i)
        for i in range(len(queries)-1, -1,-1):
            op,x = queries[i]
            g = x_to_g[x]
            if op==2:
                if i==first_offline[x]: g_min[g] = min(g_min[g], x)
            else:
                if i < first_offline[x]: ans.append(x)
                elif g_min[g] != math.inf: ans.append(g_min[g])
                else: ans.append(-1)
        return ans[::-1]

    def processQueries(self, c: int, connections: List[List[int]], queries: List[List[int]]) -> List[int]:
        # 基于 DFS 分组!
        g = [[] for _ in range(c+1)]
        for x,y in connections:
            g[x].append(y)
            g[y].append(x)
        belong = [-1] * (c+1)
        heaps = []  # 记录每个组包含的节点, heap
        def dfs(x: int) -> None:
            belong[x] = len(heaps)  # 记录节点 x 在哪个堆
            h.append(x)  # NOTE: 这里的 h 在外层初始化!
            for y in g[x]:
                if belong[y] == -1:
                    dfs(y)
        for x in range(1, c+1):
            if belong[x] != -1: continue
            h = []
            dfs(x)
            heapify(h)
            heaps.append(h)
        # 3. 懒删除堆
        ans = []
        offline = [False] * (c+1)
        for op,x in queries:
            if op==2: offline[x] = True
            else:
                if not offline[x]: ans.append(x)
                else:
                    h = heaps[belong[x]]
                    while h and offline[h[0]]: heappop(h)  # 
                    ans.append(h[0] if h else -1)  # 简写
        return ans

    """ 3608. 包含 K 个连通分量需要的最小时间 
一个图的每条边会在 t_i 时间消失, 求构成至少 k 个连通分量的最小时间
限制: n 1e5
思路 1: #并查集 逆向考虑
    复杂度: O(n+mlogm+mlogn)
https://leetcode.cn/problems/minimum-time-for-k-connected-components/solutions/3716407/bing-cha-ji-cong-da-dao-xiao-he-bing-pyt-03qz/
    """
    def minTime(self, n: int, edges: List[List[int]], k: int) -> int:
        edges.sort(key=lambda x: -x[2]) # 按照 time 降序排列
        uf = UnionFind(n)
        for u,v,t in edges:
            uf.merge(u,v)
            if uf.cc < k:   # 这条边不能留，即移除所有 time <= t 的边
                return t
        return 0 # 无需移除任何边

    """ 3609. 到达目标点的最小移动次数 
从 (sx, sy) -> (tx, ty). 对于 (x,y), 记 m = max(x,y) 每次移动可以是 (x+m, y) or (x,y+m). 求最小移动步数
限制: v 1e9 >0
思路 1: #逆向思维 + 分类讨论
    反向, 考虑从 (x,y) 走到 (sx, sy)
    - 不失一般性, 假设 x>=y 且 x>0 (对于 x=y=0 的情况无需考虑; 结论有对称性)
    分类考虑上一步的操作:
        (x/2, y). 则要求 x/2>=y, x>=2y 且为偶数
        (x-y, y). 则要求 x-y<=y, y<=x<=2y
        (x,y/2). 则要求 x<=y/2 和假设矛盾
        (x,y-x). 由于不考虑负数, 因此假设了 y-x>=0, 也即 x=y>0, 倒推操作后一个变为 0
    边界:
        x=sx & y=sy -> 返回
        x<sx or y<sy -> -1
    现在考虑倒推的过程:
        若 x>=2y: 奇数不可能; 偶数 //2
        若 x>y: x -= y
        若 x==y: 此时两种操作
    复杂度: O(log(tx+ty))
https://leetcode.cn/problems/minimum-moves-to-reach-target-in-grid/solutions/3716440/ni-xiang-si-wei-fen-lei-tao-lun-yan-ge-z-m5cc/
    """
    def minMoves(self, sx: int, sy: int, tx: int, ty: int) -> int:
        x,y = tx,ty
        cnt = 0
        while x!=sx or y!=sy:  # NOTE: 注意终止条件!
            if x<sx or y<sy:  # 失败
                return -1
            cnt += 1
            # 下面直接枚举了所有可能情况; 可以参考 ling 的讨论, 通过调换 sx,sy 来维护 x>=y 的条件
            if x>=2*y:
                if x%2: return -1
                x //= 2
            elif y>= 2*x:
                if y%2: return -1
                y //= 2
            elif x > y:
                x -= y
            elif y > x:
                y -= x
            else:
                if sx==0: x=0
                else: y=0
        return cnt

class UnionFind:
    def __init__(self, n: int):
        self.fa = list(range(n))
        self.cc = n
    # 返回 x 所在集合的代表元
    # 同时做路径压缩，也就是把 x 所在集合中的所有元素的 fa 都改成代表元
    def find(self, x: int) -> int:
        if self.fa[x] != x:
            self.fa[x] = self.find(self.fa[x])
        return self.fa[x]
    # 把 from 所在集合合并到 to 所在集合中
    def merge(self, x: int, y: int) -> None:
        x, y = self.find(x), self.find(y)
        if x==y: return
        self.fa[x] = y
        self.cc -= 1

sol = Solution()
result = [
    # sol.validateCoupons(code = ["SAVE20","","PHARMA5","SAVE@20"], businessLine = ["restaurant","grocery","pharmacy","restaurant"], isActive = [True,True,True,True]),
    # sol.processQueries(c = 5, connections = [[1,2],[2,3],[3,4],[4,5]], queries = [[1,3],[2,1],[1,1],[2,2],[1,2]]),
    # sol.processQueries(c = 3, connections = [], queries = [[1,1],[2,1],[1,1]]),
    # sol.minTime(n = 2, edges = [[0,1,3]], k = 2),
    # sol.minTime(3, [[2,0,4242],[2,1,7212]], 2),
    sol.minMoves(sx = 1, sy = 2, tx = 5, ty = 4),
    sol.minMoves(sx = 0, sy = 1, tx = 2, ty = 3),
    sol.minMoves(sx = 1, sy = 1, tx = 2, ty = 2),
]
for r in result:
    print(r)