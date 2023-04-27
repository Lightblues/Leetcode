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
https://leetcode.cn/contest/weekly-contest-324

@2022 """
class Solution:
    """ 6265. 统计相似字符串对的数目 """
    def similarPairs(self, words: List[str]) -> int:
        wordset = defaultdict(int)
        for w in words:
            # wordset[tuple(sorted(set(w)))] += 1
            wordset["".join(sorted(set(w)))] += 1
        ans = 0
        for w,c in wordset.items():
            ans += math.comb(c, 2)
        return ans
    
    """ 6266. 使用质因数之和替换后可以取到的最小值 """
    def smallestValue(self, n: int) -> int:
        def decompose(x):
            # 质因子分解
            ans = []
            for i in range(2, x+1):
                while x % i == 0:
                    ans.append(i)
                    x //= i
                if x == 1:
                    break
            return ans
        while True:
            coms = decompose(n)
            # 边界条件
            if len(coms)==1: return n
            mn = sum(coms)
            # 注意 4分解之后只和还是4, 避免死循环
            if mn==n: return n
            n = mn
    
    """ 6267. 添加边使所有节点度数都为偶数 #hard #细节 给定一张图, 最多添加两条边, 要求使得所有节点的度数都是偶数, 问是否可以 (不允许 重边/自环). 限制: n,m 1e5
思路1: 分类讨论, 注意细节
    显然, 要求图中度数为奇数的节点数量为 0/2/4
    注意, 当奇数节点有2个的时候, 除了在它们之间加一条边 (要求本身没有连边), 还可以连到它们之前都没有连接的一个新节点上!
    奇数节点数量为4, 只能在它们之间添加两条边. 如何检查是否可以添加 (不产生重边)? 枚举所有的组合即可 (见下面的代码)
"""
    def isPossible(self, n: int, edges: List[List[int]]) -> bool:
        g = [[] for _ in range(n)]
        for u,v in edges:
            u,v = u-1,v-1
            g[u].append(v); g[v].append(u)
        singles = []
        for i,nei in enumerate(g):
            if len(nei)%2==1: singles.append(i)
        # 只有当奇数度数节点为 0/2/4 时才可能
        if len(singles)==0: 
            return True
        elif len(singles)==2: 
            u,v = singles
            # 添加一条边
            if u not in g[v]: return True
            # 添加两条边!!
            s = set(range(n)) - set(g[u]) - set(g[v])
            if len(s)>0: return True
        elif len(singles)==4:
            # 枚举可能的两两组合
            # 只需要枚举第一个节点的组合 (u,v), 剩下的两个节点构成另一对. 
            # u, remains = singles[0], singles[1:]
            # for i in range(3):
            #     v = remains[i]
            #     if v not in g[u]:
            #         r = remains[:]
            #         r.pop(i)
            #         if r[0] not in g[r[1]]:
            #             return True
            # 另一种方式
            if singles[0] not in g[singles[1]] and singles[2] not in g[singles[3]]: return True
            if singles[0] not in g[singles[2]] and singles[1] not in g[singles[3]]: return True
            if singles[0] not in g[singles[3]] and singles[1] not in g[singles[2]]: return True
        return False

    """ 6268. 查询树中环的长度 #hard 给定一棵完全二叉树, 跟节点为1, 值为v的节点的两个子节点的值分别为 2v,2v+1. 现在给定一组查询 (a,b), 问在ab之间连一条跳边之后构成的环的长度. 限制: 树高 n 30; 查询数量 q 1e5 
思路1: 也即找两个节点的「最小公共祖先」. 
    在本题场景下, 由于v是有规律的, 可以直接算出每个节点到根节点的路径表示. 例如, 对于节点5, 每次除以二, 得到 5->2->1->0, 每次的余数序列是 [1,0,1] 可以唯一表示该节点.
    对于每个查询 (a,b), 在序列表示的基础上找最小公共祖先.
        例如对于节点 (5,3), 他们的路径表示分别是 [1,0,1], [1,1], 公共路径是 [1], 那么最小公共祖先是1, 那么环的长度就是 1 + 2+1=4
"""
    def cycleLengthQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        # def getLabel(x):
        #     ans = []
        #     while x>0:
        #         ans.append(x%2)
        #         x//=2
        #     return ans
        def getLabel(x):
            ans = [x]
            while x>1:
                x//=2
                ans.append(x)
            return ans
        def cal(x,y):
            # 计算两个节点表示的环长. 这里 x,y 的路径都是反向到根节点的
            if len(y)<len(x):
                x,y = y,x
            # 去除公共路径
            while len(x)>0 and x[-1]==y[-1]:
                x.pop(); y.pop()
            return 1 + len(x)+len(y)
        ans = []
        for x,y in queries:
            lx,ly = getLabel(x), getLabel(y)
            ans.append(cal(lx,ly))
        return ans
    
sol = Solution()
result = [
    # sol.similarPairs(words = ["aba","aabb","abcd","bac","aabc"]),
    # sol.smallestValue(15),
    # sol.smallestValue(3),
    # sol.smallestValue(4),
    sol.isPossible(n = 5, edges = [[1,2],[2,3],[3,4],[4,2],[1,4],[2,5]]),
    sol.isPossible(n = 4, edges = [[1,2],[3,4]]),
    sol.isPossible(n = 4, edges = [[1,2],[1,3],[1,4]]),
    sol.isPossible(11, [[5,9],[8,1],[2,3],[7,10],[3,6],[6,7],[7,8],[5,1],[5,7],[10,11],[3,7],[6,11],[8,11],[3,4],[8,9],[9,1],[2,10],[9,11],[5,11],[2,5],[8,10],[2,7],[4,1],[3,10],[6,1],[4,9],[4,6],[4,5],[2,4],[2,11],[5,8],[6,9],[4,10],[3,11],[4,7],[3,5],[7,1],[2,9],[6,10],[10,1],[5,6],[3,9],[2,6],[7,9],[4,11],[4,8],[6,8],[3,8],[9,10],[5,10],[2,8],[7,11]]),
    sol.isPossible(21, [[2,19],[16,17],[8,14],[2,16],[12,20],[12,14],[16,18],[15,16],[10,21],[3,5],[13,18],[17,20],[14,17],[9,12],[5,15],[5,6],[3,7],[2,21],[10,13],[8,16],[7,18],[4,6],[9,1],[13,21],[18,20],[7,14],[4,19],[5,8],[3,11],[11,1],[7,12],[4,7],[3,16],[13,17],[17,19],[9,13],[7,19],[10,16],[4,13],[4,5],[2,15],[12,19],[11,16],[2,9],[11,17],[17,1],[16,21],[4,10],[10,14],[14,16],[4,1],[13,20],[5,20],[4,14],[4,21],[10,20],[2,14],[8,15],[4,8],[6,19],[15,1],[19,1],[8,19],[15,21],[3,12],[11,18],[9,17],[18,19],[7,21],[3,21],[16,19],[11,15],[5,1],[8,17],[3,15],[8,1],[10,19],[3,8],[6,16],[2,8],[5,18],[11,13],[11,20],[14,21],[6,20],[4,20],[12,13],[5,12],[10,11],[9,15],[3,19],[9,20],[14,18],[21,1],[13,19],[8,21],[2,13],[3,10],[9,18],[19,21],[6,7],[3,18],[2,18],[6,14],[3,17],[5,21],[14,20],[8,9],[16,1],[3,4],[13,1],[5,9],[4,15],[17,21],[20,21],[2,17],[13,14],[11,14],[9,16],[10,18],[6,15],[6,12],[3,13],[5,11],[6,1],[12,17],[8,10],[5,10],[8,18],[4,12],[10,1],[6,13],[4,18],[7,20],[7,16],[2,6],[12,21],[4,17],[15,18],[13,16],[15,20],[7,10],[6,10],[2,20],[7,15],[18,1],[12,1],[3,20],[7,1],[14,15],[4,9],[11,19],[7,9],[5,17],[18,21],[6,21],[8,11],[6,17],[3,14],[7,11],[5,7],[7,13],[6,8],[6,9],[10,12],[5,16],[2,4],[17,18],[9,11],[12,16],[3,6],[12,18],[3,9],[11,12],[14,19],[10,15],[5,13],[8,13],[15,17],[2,10],[11,21],[20,1],[6,18],[2,12],[19,20],[6,11],[8,12],[2,3],[12,15],[2,11],[9,10],[7,17],[9,19],[13,15],[7,8],[4,11],[2,5],[5,19],[16,20],[15,19],[9,14],[14,1],[10,17],[9,21],[2,7],[8,20],[5,14],[4,16]])
    # sol.cycleLengthQueries(n = 3, queries = [[5,3],[4,7],[2,3], [6,7]]),
    # sol.cycleLengthQueries(n = 2, queries = [[1,2]]),
]
for r in result:
    print(r)
