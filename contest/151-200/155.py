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
https://leetcode.cn/contest/weekly-contest-155
T2 的二分很精彩, 需要有一定的数学判断. T4 的拓扑排序思路容易想到, 但是需要注意很多的细节, 实现代码比较冗长. 

@2022 """
class Solution:
    """ 1200. 最小绝对差 """
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        arr.sort()
        min_diff = min([arr[i+1]-arr[i] for i in range(len(arr)-1)])
        ans = []
        for i in range(len(arr)-1):
            if arr[i+1]-arr[i] == min_diff:
                ans.append([arr[i], arr[i+1]])
        return ans
    
    """ 1201. 丑数 III #medium 但实际上 #hard #题型 #二分 给定三个数字 a,b,c 定义「丑数」为能够被 a/b/c 之一整除的数字, 问第n个丑数是多少 
限制: n,abc 1e9; 题目保证了结果在 2e9 以内
简化讨论: 考虑两个数字的情况. 比如 2,3. 则能够整除的数字按照 2,3,4,6; 8,9,10,12; 的顺序循环...
    循环大小是多少? m = lcm(a,b,c).
    其中有多少个不同的数字? m//a+m//b+m//c - m//lab-m//lbc-m//lca + m//labc. 可以类比 #集合图
思路0: 尝试用 divmod(n, cnt), 然后用naive的方式计算 m 以下的第 x个丑数. 
    不可行, 例子 n = 1000000000, a = 2, b = 217983653, c = 336916467
思路1: #二分. 实际上, 上面的统计数量的公式可以直接用来作为「小于等于x的丑数的数量」, 我们采用二分搜索即可. 复杂度 O(logE). 
https://leetcode.cn/problems/ugly-number-iii/
"""
    def nthUglyNumber(self, n: int, a: int, b: int, c: int) -> int:
        # Least Common Multiple.
        mab = math.lcm(a,b)
        mbc = math.lcm(b,c)
        mca = math.lcm(c,a)
        mabc = math.lcm(mab,c)
        # cnt = mabc//a + mabc//b + mabc//c - mabc//mab - mabc//mbc - mabc//mca + 1
        # m,r = divmod(n, cnt)
        # def getKth(a,b,c,k):
        #     nums = set(a*i for i in range(1,k+1)) | set(b*i for i in range(1,k+1)) | set(c*i for i in range(1,k+1))
        #     return sorted(nums)[k-1]
        # return m * mabc + getKth(a,b,c, r)
        def cnt(x):
            return x//a+x//b+x//c - x//mab - x//mbc - x//mca + x//mabc
        l=1; r=2*10**9+1
        ans = 0
        while l<r:
            mid = (l+r)//2
            if cnt(mid) >= n:
                r = mid
            else:
                l = mid+1
        return r
    
    """ 1202. 交换字符串中的元素 #medium 见 [并查集] """
    
    """ 1203. 项目管理 #hard #细节 项目之间有前后依赖关系, 要排序. 他们分了几组, 要求在排序中同组的项目相邻. 给出一种可行的安排. 限制: n 3e4
思路1: #拓扑排序 
    分组内部拓扑排序, 分组间拓扑排序, 合并.
    如何处理未分组的项目 (group=-1)? 将它们单独看作一组. 因此需要重新分配组号 #细节
参见 [官答](https://leetcode.cn/problems/sort-items-by-groups-respecting-dependencies/solution/1203-xiang-mu-guan-li-by-leetcode-t63b/)
"""
    def sortItems(self, n: int, m: int, group: List[int], beforeItems: List[List[int]]) -> List[int]:
        def build(group, beforeItems):
            nonlocal m
            # 重新对于组号进行编号
            ungrouped = sum(1 for g in group if g==-1)
            for i,gid in enumerate(group):
                if gid==-1: group[i]=m; m += 1
            # 得到每组所包含的节点
            groups = [[] for _ in range(m)]
            for u,g in enumerate(group):
                groups[g].append(u)
            # 构建每组和组间的拓扑关系, 构图
            group_graphs = [set() for _ in range(m)]
            for gid, gg in enumerate(groups):
                # 尝试用 dict.fromkeys 来些, 但 mutuable 对象会被指向同一个地址
                # group_graphs[gid] = defaultdict.fromkeys(gg, [])
                group_graphs[gid] = {i: [] for i in gg}
            gGroup = {i: [] for i in range(m)}
            # 连边
            for u,gg in enumerate(beforeItems):
                for v in gg:
                    gu,gv = group[u], group[v]
                    if gu!=gv: gGroup[gu].append(gv)
                    else: group_graphs[gu][u].append(v)
            return gGroup, group_graphs
        gGroup, group_graphs = build(group, beforeItems)
        def topo_sort(g):
            # 拓扑排序. 这里的输入 g 采用 defaultdict 的形式, 因为节点可能不连续
            n = len(g)
            rg = defaultdict(list)
            for u,before in g.items():
                for v in before:
                    rg[v].append(u)
            degress = {u:len(before) for u,before in g.items()}
            ans = []
            q = [u for u in g.keys() if degress[u]==0]
            q = deque(q)
            while q:
                u = q.popleft()
                ans.append(u)
                for v in rg[u]:
                    degress[v] -= 1
                    if degress[v]==0: q.append(v)
            return ans if len(ans)==n else []
        # 1) 对组进行 topo_sort
        gtopo = topo_sort(gGroup)
        if not gtopo: return []
        # 2) 对每个组内部进行 topo_sort
        ans = []
        for gid in gtopo:
            g = group_graphs[gid]
            # 有些组可能为空! 要排除
            if len(g)==0: continue
            topo = topo_sort(g)
            if not topo: return []
            ans.extend(topo)
        return ans

    

    
sol = Solution()
result = [
    # sol.minimumAbsDifference(arr = [4,2,1,3]),
    # sol.sortItems(n = 8, m = 2, group = [-1,-1,1,0,0,1,0,-1], beforeItems = [[],[6],[5],[6],[3,6],[],[],[]]),
    # sol.sortItems(n = 8, m = 2, group = [-1,-1,1,0,0,1,0,-1], beforeItems = [[],[6],[5],[6],[3],[],[4],[]]),
    # sol.sortItems(5,5,[2,0,-1,3,0], [[2,1,3],[2,4],[],[],[]]),
    sol.nthUglyNumber(n = 3, a = 2, b = 3, c = 5),
    sol.nthUglyNumber(n = 1000000000, a = 2, b = 217983653, c = 336916467),
]
for r in result:
    print(r)
