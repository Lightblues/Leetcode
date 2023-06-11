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
https://leetcode.cn/contest/weekly-contest-346
https://leetcode.cn/circle/discuss/fwWHZg/
https://www.bilibili.com/video/BV1Qm4y1t7cx/

T1居然没想到栈! T3的回溯忘记了灵神的讲解了😭 T4太难了! 整个状态久很拉~ 

Easonsi @2023 """
class Solution:
    """ 2696. 删除子串后的字符串最小长度 #easy #栈
思路1: #暴力
    太蠢了忘记了 栈!
    """
    def minLength(self, s: str) -> int:
        n = len(s)
        while True:
            s = s.replace('AB', '').replace('CD', '')
            if len(s)==n: break
            n = len(s)
        return n
    
    """ 2697. 字典序最小回文串 """
    def makeSmallestPalindrome(self, s: str) -> str:
        n = len(s)
        pre = []
        for i in range(n//2):
            pre.append(min(s[i], s[n-1-i]))
        pre = ''.join(pre)
        return pre + ("" if n%2==0 else s[n//2]) + pre[::-1]
    
    """ 2698. 求一个整数的惩罚数 #medium #题型 定义「惩罚数」为i, 满足 str(i^2) 可以拆分成一组数字, 其和为i
思路1: 检查每个数字是否合法, 用到 #回溯
    [灵神](https://leetcode.cn/problems/find-the-punishment-number-of-an-integer/solution/yu-chu-li-hui-su-by-endlesscheng-ro3s/)
    """
    def punishmentNumber(self, n: int) -> int:
        def check(x):
            s = str(x**2)
            n = len(s)
            def f(i,j,xx):
                if j>=n: return xx == (int(s[i:]) if i<n else 0)
                if f(i,j+1, xx): return True
                v = int(s[i:j+1])
                if v>xx: return False
                if f(j+1,j+1, xx-v): return True
                return False
            return f(0,0,x)
        ans = 0
        for i in range(1,n+1):
            if check(i): 
                ans += i**2
        return ans
    
    """ 2699. 修改图中的边权 #hard #hardhard 对于一张图部分节点未赋予权重, 问能否对这些边赋值 [1,1e9], 使得 ddist(s,d)=target 
限制: n 100; val 1e7; 所给的图连通
思路1: 两次 #Dijkstra 见灵神视频
    [灵神](https://leetcode.cn/problems/modify-graph-edge-weights/solution/xiang-xi-fen-xi-liang-ci-dijkstrachou-mi-gv1m/)
    详细的证明见 官方
思路2: #二分, 利用题目中的 #贪心 结构
    见 [官方](https://leetcode.cn/problems/modify-graph-edge-weights/solution/xiu-gai-tu-zhong-de-bian-quan-by-leetcod-66bg/)
    """
    def modifiedGraphEdges(self, n: int, edges: List[List[int]], source: int, destination: int, target: int) -> List[List[int]]:
        g = [[] for _ in range(n)]
        for i, (x, y, _) in enumerate(edges):
            g[x].append((y, i))
            g[y].append((x, i))  # 建图，额外保存边的编号

        dis = [[inf, inf] for _ in range(n)]
        dis[source] = [0, 0]

        def dijkstra(k: int) -> None:  # 这里 k 表示第一次/第二次
            vis = [False] * n
            while True:
                # 找到当前最短路，去更新它的邻居的最短路
                # 根据数学归纳法，dis[x][k] 一定是最短路长度
                x = -1
                for y, (b, d) in enumerate(zip(vis, dis)):
                    if not b and (x < 0 or d[k] < dis[x][k]):
                        x = y
                if x == destination:  # 起点 source 到终点 destination 的最短路已确定
                    return
                vis[x] = True  # 标记，在后续的循环中无需反复更新 x 到其余点的最短路长度
                for y, eid in g[x]:
                    wt = edges[eid][2]
                    if wt == -1:
                        wt = 1  # -1 改成 1
                    if k == 1 and edges[eid][2] == -1:
                        # 第二次 Dijkstra，改成 w
                        w = delta + dis[y][0] - dis[x][1]
                        if w > wt:
                            edges[eid][2] = wt = w  # 直接在 edges 上修改
                    # 更新最短路
                    dis[y][k] = min(dis[y][k], dis[x][k] + wt)

        dijkstra(0)
        delta = target - dis[destination][0]
        if delta < 0:  # -1 全改为 1 时，最短路比 target 还大
            return []

        dijkstra(1)
        if dis[destination][1] < target:  # 最短路无法再变大，无法达到 target
            return []

        for e in edges:
            if e[2] == -1:  # 剩余没修改的边全部改成 1
                e[2] = 1
        return edges

sol = Solution()
result = [
    # sol.minLength("ABFCACDB"),
    # sol.minLength("ACBBD"),
    # sol.minLength("CCDAABBDCD"),

    # sol.makeSmallestPalindrome(s = "egcfe"),
    # sol.makeSmallestPalindrome(s = "abcd"),

    sol.punishmentNumber(n = 10),
    sol.punishmentNumber(n = 37),
]
for r in result:
    print(r)
