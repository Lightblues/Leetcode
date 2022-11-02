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
https://leetcode.cn/contest/weekly-contest-211

居然被T2折磨了半天, 事实证明是自己想多了, 直接暴力也可以过 (没想明白状态空间); 
T3之前应该做过类似的 #双指标 排序的题, 结果这次还是疯狂打补丁剑走偏锋, 还是没想明白.

@2022 """
class Solution:
    """ 1624. 两个相同字符之间的最长子字符串 """
    def maxLengthBetweenEqualCharacters(self, s: str) -> int:
        ans = -1
        firstIdx = {}
        for i,ch in enumerate(s):
            if ch in firstIdx: ans = max(ans, i-firstIdx[ch]-1)
            else: firstIdx[ch] = i
        return ans
    
    """ 1625. 执行操作后字典序最小的字符串 #meduim #interest 放在了第二题, 但很有意思.
给定一个长度为偶数字符串s, 每个字符为0...9, 可以进行任意次数的两个操作: 1) 对于所有奇数元素+a (保留个位数); 2) 将s向右 #轮转 b长度. 要求可能得到的最小字典序结果.
限制: 长度 100
提示: 显然可以将原数组元素 按照奇偶性分成两组. 然后操作1仅对于某一组生效.
    另外, 注意数组长度n和可轮转步长b决定了哪些位置的元素可以被放在首位.
    由于字符串长为偶数, 若b也为偶数, 则两个组的奇偶性将永远不变, 操作1仅能对于奇数组操作; 否则, 两数组都可进行操作性.
思路1: 遍历所有可放在首位的元素, 分别对于两组进行取最小值操作.
    具体而言, 可以轮转到首位的元素集合为idxSet, 然后对于所有可能的位置, 可以从该位置分成两组 arr1, arr2 (根据 `[arr[(sidx+i)%n] for i in range(0/1,n,2)]` 划分). 然后分别对两子序列利用操作1取最小值 (注意当b为偶数时, arr1无法进行此操作). 这样就可以得到以sidx开头的最小字典序.
    复杂度: idxSet 大小最大 n, 利用操作1取最小的复杂度为 O(10*n), 因此总的复杂度为 O(10*n^2)
思路2: #暴力 美学, 直接DFS找到所有可能的结果
    实际上, 本题所有可能的结果只有 O(n * 10^2) 种, 第一项为以某元素开始, 第二项为所有可能的序列. 因此直接暴力DFS即可.
"""
    def findLexSmallestString(self, s: str, a: int, b: int) -> str:
        # 思路1: 遍历所有可放在首位的元素, 分别对于两组进行取最小值操作.
        def getMin(arr: List[int]):
            ans = arr[:]
            for _ in range(9):
                arr = [(i+a)%10 for i in arr]
                if arr<ans: ans = arr[:]
            return ans
        def merge(arr1: List[int], arr2: List[int]) -> str:
            arr = itertools.chain(*zip(arr1, arr2))
            return "".join(map(str,arr))
        n = len(s)
        # 所有可能为第一个字符的位置
        idx = 0; idxSet = set()
        while idx not in idxSet:
            idxSet.add(idx)
            idx = (idx+b) % n
        arr = list(map(int, s))
        ans = s
        for sidx in idxSet:
            arr1 = [arr[(sidx+i)%n] for i in range(0,n,2)]
            arr2 = [arr[(sidx+i)%n] for i in range(1,n,2)]
            arr2 = getMin(arr2)
            if b%2==1:
                arr1 = getMin(arr1)
            tmp = merge(arr1, arr2)
            if tmp<ans: ans = tmp
        return ans
    
    def findLexSmallestString(self, s: str, a: int, b: int) -> str:
        # 思路2, 暴力. from https://leetcode.cn/problems/lexicographically-smallest-string-after-applying-operations/solution/yi-li-jie-ban-dfs-by-sunrise-z/
        b = b%len(s)
        def addOpt(s):
            ans = [c for c in s]
            for i in range(1,len(s),2):               
                ans[i]=str((int(s[i])+a))[-1]
            return ''.join(ans)
        def lunOpt(s):
            return s[-b:]+s[:-b]
        alls = {s}  
        def dfs(s):           
            alls.add(s)          
            s1 = addOpt(s)
            s2 = lunOpt(s)          
            if s1 not in alls:                
                dfs(s1)           
            if s2 not in alls:
                dfs(s2)
        dfs(s)
        return min(alls)

    """ 1626. 无矛盾的最佳球队 #medium #题型
有一组球员 (score, age), 若两名球员中, 年龄较小的那个分数较大, 则产生矛盾. 要求在所有球员中组成分数和最大的球队.
限制: n 1e3; age 1e3; score 1e6.
思路1: 将年龄和分数连续化. 然后按照年龄进行排序.
    记 f(a,s) 表示由年龄最大为a的球员, 分数最大为s组成的无冲突球队的最大分数. 
    错误记录: 一开始遍历所有球员, 但这样有问题, 因为有些 f(a,s) 可能为空.
    补丁: 稠密遍历年龄和分数. 则有 `f(a,s) = max(f(a',s') + s*multi)`, 其中multi是分数为s并且年龄为a的球员数量. 这里的遍历对象满足 `a' <= a, s' <= s`, 也即整个矩阵的最大值. 
    下面的实现改成了一维DP进行压缩.
    复杂度: 理论上也是 O(n^2), 但要比下面的慢很多.
思路2: #双指标 排序
    直接对于球员按照 (age,score) 二级排序. #DP 定义为 `f(i)` 表示以第i个球员为终点的最大分数和. 这样, 可以 **保证第i个球员为此组中的分数最大值**. 
    则有更新 `f(i) = max{ f(j) + score[i] }` 这里的j满足 `j<i and score[j] <= score[i]`. 由于相同年龄的球员按照分数排序, 因此不会有少记录的情况.
    复杂度: O(n^2)
"""
    def bestTeamScore(self, scores: List[int], ages: List[int]) -> int:
        # 思路1: 将年龄和分数连续化. 然后按照年龄进行排序.
        s = sorted(set(scores))
        s2cont = {s:i for i,s in enumerate(s)}
        # cnt2s  = {i:s for i,s in enumerate(s)}
        a = sorted(set(ages))
        a2cont = {a:i for i,a in enumerate(a)}
        ages = [a2cont[a] for a in ages]
        # players = sorted(zip(ages, scores))
        age2scores = defaultdict(Counter)
        for age, score in zip(ages, scores):
            age2scores[age][score] += 1
        # f = [[0]*(len(s)+1) for _ in range(len(a)+1)]
        f = [0] * (len(s)+1)
        ans = 0
        for age in range(len(a)):
            mx = 0      # 当前限制下的最大分数
            for score in range(len(s)):
                mx = max(mx, f[score+1], f[score])
                players = age2scores[age][s[score]]
                ss = mx + players*s[score]
                ans = max(ans, ss)
                f[score+1] = ss
        return ans
    def bestTeamScore(self, scores: List[int], ages: List[int]) -> int:
        # 思路2
        players = sorted(zip(ages, scores))
        n = len(players)
        f = [0] * n
        f[0] = players[0][1]
        ans = f[0]
        for i in range(1, n):
            # 注意筛选结果可能为空
            ss = [s for j,s in enumerate(f[:i]) if players[j][1]<=players[i][1]]
            ss = max(ss + [0]) + players[i][1]
            f[i] = ss
            ans = max(ans, ss)
        return ans
    
    """ 1627. 带阈值的图连通性 #hard 
有编号为 1...n 的节点. 两个节点相连的条件为, x,y 的gcd大于阈值. 对于每一个查询, 返回两点是否相连.
思路1: 查询联通性采用 #并查集. 由于节点编号有序, 对于 g in threshold...n, 每次遍历 range(g, n+1, g) 这些节点, 将其相连. 
    这样的复杂度为 #调和级数 `n+n/2+n/3... = O(n logn)`.
"""
    def areConnected(self, n: int, threshold: int, queries: List[List[int]]) -> List[bool]:
        fa = [i for i in range(n+1)]
        def find(x):
            if fa[x] == x:
                return x
            fa[x] = find(fa[x])
            return fa[x]
        def union(x, y):
            x, y = find(x), find(y)
            if x == y:
                return
            fa[x] = y
        for g in range(threshold+1, n+1):
            for i in range(g, n+1, g):
                union(i, g)
        ans = [False] * len(queries)
        for i, (x, y) in enumerate(queries):
            ans[i] = find(x) == find(y)
        return ans
    
sol = Solution()
result = [
    # sol.maxLengthBetweenEqualCharacters(s = "cabbac"),
    # sol.bestTeamScore(scores = [1,3,5,10,15], ages = [1,2,3,4,5]),
    # sol.bestTeamScore(scores = [4,5,6,5], ages = [2,1,2,1]),
    # sol.bestTeamScore([319776,611683,835240,602298,430007,574,142444,858606,734364,896074], [1,1,1,1,1,1,1,1,1,1]),
    # sol.areConnected(n = 5, threshold = 1, queries = [[4,5],[4,5],[3,2],[2,3],[3,4]]),
    # sol.areConnected(n = 6, threshold = 2, queries = [[1,4],[2,5],[3,6]]),
    # sol.findLexSmallestString(s = "74", a = 5, b = 1),
    sol.findLexSmallestString(s = "5525", a = 9, b = 2),
    sol.findLexSmallestString(s = "43987654", a = 7, b = 3),
    
    
]
for r in result:
    print(r)
