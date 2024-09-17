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
https://oi-wiki.org/graph/euler/
一些概念
    通过图中所有边恰好一次且行遍所有顶点的通路称为欧拉通路；
    通过图中所有边恰好一次且行遍所有顶点的回路称为欧拉回路；
    具有欧拉回路的无向图称为欧拉图；
    具有欧拉通路但不具有欧拉回路的无向图称为半欧拉图。
判断欧拉图
    无向图: 
        欧拉图的充要条件是图中所有顶点的度数都是偶数。
        半欧拉图的充要条件是图中有且仅有两个顶点的度数是奇数，其余顶点的度数都是偶数。
    有向图: 
        欧拉图的充要条件是图中所有顶点都是强联通的, 并且所有顶点的入度等于出度。
        半欧拉图的充要条件是 1] 退化为无向图是连通的; 2] din-dout 数量至多为1; 3] dout-din 数量至多为1; 4] 其余节点的din=dout.
如何求解欧拉通路? #Hierholzer 算法
    核心是, 从当前节点u出发进行DFS, 和一般的区别在于
        对于半欧拉图, 从节点u出发的分支中, **最多只能有一个「死胡同」**, 也即回不到节点u的路径. 
        为了检查是否「死胡同」, 在DFS过程中需要「拆边」, 也即修改图结构. 
        在DFS中, 我们最后再加入节点u, 最后对于访问序列逆序输出即可. 
        复杂度: O(m), m为边的数量
    算法:
        从起点出发进行DFS
        每次沿着某条边拓展 (u,v) 的时候, 都需要删除这条边 (避免重复访问)
        在无法进行拓展的时候 (采用while循环), 才将节点u加入访问序列
        注意: 逆序输出访问序列
    修改为按照字典序最小: 这样需要对于节点所连的邻居进行排序, 例如可以用 #堆, 因此时间复杂度为 O(m logm)

Easonsi @2023 """
class Solution:

    """ 0332. 重新安排行程 #hard #欧拉通路 机票行程重排列, 要求首尾相连 (连成一条通路). 要求从JFK出发, 按字典序返回最小的行程组合.
限制: 边数量 M 300
见 [官答](https://leetcode-cn.com/problems/reconstruct-itinerary/solution/zhong-xin-an-pai-xing-cheng-by-leetcode-solution/)
提示: 问题转化为, 对于一个有向图, 已知是一个半欧拉图, 要求找到从JFK开始的一条欧拉通路
思路1: #Hierholzer 算法. 见上面的说明
"""
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        # Hierholzer 算法 求解欧拉通路 -- 建议看下面栈的写法! 
        def dfs(curr: str):
            # 重点是这里的wihle!! 尽量尝试 DFS
            while vec[curr]:
                # 尽量去排序较小的机场
                tmp = heapq.heappop(vec[curr])
                dfs(tmp)
            record.append(curr)      # 最后再加入当前节点; 也可以按照 0753 的, 写在 while 里面!!. 区别在于 record 是否记录了起始节点. 
        # 记录图, 用最小堆保存数据 (字典序)
        vec = defaultdict(list)
        for depart, arrive in tickets:
            vec[depart].append(arrive)
        for key in vec:
            heapq.heapify(vec[key])     # 利用最小堆保存数据
        record = list()
        dfs('JFK')
        return record[::-1]
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        g = defaultdict(list)
        for s,e in tickets:
            g[s].append(e)
        for k,v in g.items():
            heapq.heapify(v)
        # 也可以写成 stack 的形式, 更优雅! 
        h = ['JFK']
        ans = []
        while h:
            while g[h[-1]]:     # 尽量去寻找环, 那条支链必然在最后被加入
                tmp = heapq.heappop(g[h[-1]])       # 先入栈的最后出栈, 从而 [::-1] 之后保证了是最小的! 
                h.append(tmp)
            ans.append(h.pop())
        return ans[::-1]

    """ 0753. 破解保险箱 #hard #欧拉通路
密码是 n 位数, 密码的每一位是 k 位序列 0, 1, ..., k-1 中的一个。返回一个最短字符串, 其子字符串包括所有可能的密码. 
限制: n [1,4]; k [1,10]; k^n 最大为 4096
[官答](https://leetcode-cn.com/problems/cracking-the-safe/solution/po-jie-bao-xian-xiang-by-leetcode-solution/)
思路1: 关键在于将其转化为一个规范的欧拉通路问题
    建图: 要求的是 n 长序列, 都可将其看成 n-1长序列加上 0~k-1 的数字. 因此, 可以构建一个图, 节点为所有的 n-1长序列, 其第i个出边就是在最后加上数字i并去除第一位数字, 跳到相应的节点上. 
        用数字表示: 例如, 节点u的第v的出边就跳转到数值为 u*k % (k**(n-1)) + v 的节点上. (用k进制来表示节点)
        可知, 这样构造的图, 每个节点都有 k条出边和入边, 共可代表 $k^{n-1} * k$ 个不同的数字, 正好对应了所有可能的密码.
        显然, 这张图是欧拉图, 一个欧拉回路就对应一个题目所要求的一个字符串. 
 """
    def crackSafe(self, n: int, k: int) -> str:
        # 神奇地兼容了 n=1 的情况. 
        # if n == 1: return ''.join(map(str, range(k)))
        # 建图. 实际上边/转移是在下面的 dfs中创建的. 
        edges = defaultdict(list)
        MX = k**(n-1)
        for i in range(MX):   # 节点为 [0...k**(n-1)-1]
            # 这里的边直接记录最后添加的那个字符!
            edges[i] = list(range(k))
        # Hierholzer 算法 求解欧拉通路
        record = []
        def dfs(u):
            while edges[u]:
                v = edges[u].pop()
                dfs((u*k % MX) + v)
                record.append(str(v))       # 这里在 while中加入record, 没有记录起始节点 (区别于 0332)
        dfs(0)
        # 注意在答案中加入开始节点
        return "0"*(n-1) + ''.join(record[::-1])
    
    def crackSafe(self, n: int, k: int) -> str:
        # 自己写的, 更加直观一点. 
        # 边界!! 上面的写法神奇地兼容了 n=1 的情况. 
        if n == 1: return ''.join(map(str, range(k)))
        MN = k**(n-1)
        g = [[] for _ in range(MN)]
        for u in range(MN):
            for new in range(k):
                v = (u*k + new) % MN
                g[u].append(v)
        # Hierholzer
        record = []
        def dfs(u):
            while g[u]:
                v = g[u].pop()
                dfs(v)
                record.append(str(v % k))
        dfs(0)
        return "0"*(n-1) + ''.join(record[::-1])

    def crackSafe(self, n: int, k: int) -> str:
        # from 官答, 更有技巧性的写法
        seen = set()    # 出现过的长为n的密码
        ans = list()
        highest = 10 ** (n - 1)
        # Hierholzer
        def dfs(node: int):
            for x in range(k):
                nei = node * 10 + x
                if nei not in seen:
                    seen.add(nei)
                    dfs(nei % highest)
                    ans.append(str(x))
        dfs(0)
        return "".join(ans) + "0" * (n - 1)

sol = Solution()
result = [
    sol.findItinerary([["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]),
    sol.findItinerary([["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]),
    # sol.crackSafe(1,2),
    # sol.crackSafe(2,2),
    # sol.crackSafe(3,2),
]
for r in result:
    print(r)
