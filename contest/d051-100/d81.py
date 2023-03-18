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
https://leetcode-cn.com/contest/biweekly-contest-81

哇, 第二次进 30min, 排名83! see [here](https://leetcode.cn/contest/biweekly-contest-81/ranking/).

@2022 """
class Solution:
    """ 6104. 统计星号 """
    def countAsterisks(self, s: str) -> int:
        ans = 0
        isIn = False
        for ch in s:
            if ch == "|":
                isIn = not isIn
            if ch=="*" and not isIn:
                ans += 1
        return ans
    
    """ 6106. 统计无向图中无法互相到达点对数 #medium
给定一张图, 统计不可达的 (u,v) 节点对的数量.
约束: 节点数量 1e5
思路1: 统计所有联通分量的大小. 考虑 #反问题
    提示: 相互不可达的节点对属于不同的联通分量.
    因此, 可以统计所有联通分量, 两个联通分量之间的节点对为 size1*size2. 但这样的复杂度可能是 O(n^2).
    可以考虑反问题: 所有节点对 - 可达的节点对. 所有节点对的数量为 comb(n, 2), 而可达节点对在同一联通分量中, 对数为 comb(size, 2).
"""
    def countPairs(self, n: int, edges: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        # 
        unvisited = set(range(n))
        q = deque()
        cnt = Counter()
        while unvisited:
            u = unvisited.pop()
            q.append(u)
            size = 1
            while q:
                v = q.popleft()
                for w in g[v]:
                    if w in unvisited:
                        unvisited.remove(w)
                        q.append(w)
                        size += 1
            cnt[size] += 1
        # 
        ans = math.comb(n, 2)
        for k,c in cnt.items():
            ans -= math.comb(k, 2) * c
        return ans

    """ 2317. 操作后的最大异或和 """
    def maximumXOR(self, nums: List[int]) -> int:
        ans = 0
        for num in nums:
            ans |= num
        return ans
    
    """ 6107. 不同骰子序列的数目 #hard
投骰子n次, 问满足条件的序列数量. 条件: 相邻数字的最大公约数为1, 两个相同数字之间的间距至少为3.
约束: n的数量级1e4
思路1: #状压 #DP
    可知, 第idx位置的数字可取的值仅由前两个数字决定, 只需要满足上述条件即可.
    考虑状态压缩, 用mask表示相邻两个数字, 采用6进制. 预计算: 所有合法的长度为2的序列, 合法的转移序列.
    用 `f[i][mask]` 表示长度为i, 最后两位为mask的序列数量.
    状态转移: `f[i+1][mask] = sum{ f[i][newmask] }`, 其中 newmask 表示第一位等于mask第二位并且符合条件的所有情况.
"""
    def distinctSequences(self, n: int) -> int:
        MOD = 10**9 + 7
        if n==1: return 6
        def valid(mask):
            a,b = divmod(mask, 6)
            return a!=b and math.gcd(a+1, b+1)==1
        def validTranstion(mask):
            a,b = divmod(mask, 6)
            ans = []
            for c in range(6):
                if c!=a and c!=b and math.gcd(b+1, c+1)==1:
                    ans.append(6*b + c)
            return ans
        validPairs = [i for i in range(6**2) if valid(i)]
        validTrans = {i:validTranstion(i) for i in validPairs}
        # 
        cnt = Counter(validPairs)
        for _ in range(n-2):
            newCnt = Counter()
            for u,vs, in validTrans.items():
                for v in vs:
                    newCnt[v] += cnt[u]
                    newCnt[v] %= MOD
            cnt = newCnt
        return sum(cnt.values()) % MOD
    
sol = Solution()
result = [
    # sol.countAsterisks(s = "yo|uar|e**|b|e***au|tifu|l"),
    # sol.countAsterisks(s = "l|*e*et|c**o|*de|"),
    # sol.countPairs(n = 7, edges = [[0,2],[0,5],[2,4],[1,6],[5,4]]),
    # sol.countPairs(n = 3, edges = [[0,1],[0,2],[1,2]]),
    # sol.maximumXOR(nums = [3,2,4,6]),
    # sol.maximumXOR(nums = [1,2,3,9,2]),
    sol.distinctSequences(n = 1),
    sol.distinctSequences(n = 2),
    sol.distinctSequences(n = 4),
]
for r in result:
    print(r)
