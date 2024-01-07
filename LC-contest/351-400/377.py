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
https://leetcode.cn/contest/weekly-contest-377
https://leetcode.cn/circle/discuss/vNHqts/

T3T4 有点意思. T4字符串切片等细抠时间的地方有些懵. 
Easonsi @2023 """
class Solution:
    """ 2974. 最小数字游戏 """
    def numberGame(self, nums: List[int]) -> List[int]:
        nums.sort()
        for i in range(0,len(nums),2):
            nums[i],nums[i+1] = nums[i+1],nums[i]
        return nums
    
    """ 2975. 移除栅栏得到的正方形田地的最大面积 """
    def maximizeSquareArea(self, m: int, n: int, hFences: List[int], vFences: List[int]) -> int:
        def get_lens(arr, n):
            arr = [1] + arr + [n]
            ava = set()
            for i in range(len(arr)):
                for j in range(i+1, len(arr)):
                    ava.add(arr[j]-arr[i])
            return ava
        h = get_lens(sorted(hFences), m)
        v = get_lens(sorted(vFences), n)
        mx = h & v
        if len(mx)==0: return -1
        mod = 10**9+7
        return max(mx)**2 % mod
    
    """ 2976. 转换字符串的最小成本 I #medium 定义了一系列字母 original -> changed 代价为 cost 的变换关系. 问将等长字符串从 source 转换为 target 所需要的最小代价. 
限制: 转换数量 1e2; 字符串长度 1e5
思路1: 计算好字符之间的最小转换代价, 可以通过 bfs 计算
    复杂度: O(Z ^3), 其中 Z 是不同字符串数量
    """
    def minimumCost(self, source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
        nodes = list(string.ascii_lowercase)
        edges = defaultdict(list)
        for u,v,c in zip(original, changed, cost):
            edges[u].append((v,c))
        def bfs(u):
            res = {}
            h = [(0,u)]
            while h:
                c,v = heapq.heappop(h)
                if v in res: continue
                res[v] = c
                for v2,c2 in edges[v]:
                    if v2 not in res or c+c2 < res[v2]:
                        heapq.heappush(h, (c+c2,v2))
            return res
        costs = {u:bfs(u) for u in nodes}
        res = 0
        for u,v in zip(source, target):
            if v not in costs[u]: return -1
            res += costs[u][v]
        return res
    
    """ 2977. 转换字符串的最小成本 II #hard 也是定义了转换规则, 不过包括了相同长度子串之间的一些转换规则. 问最小成本
限制: 转换数量 n 1e2; 字符串长度 L 1e3. 有限制, 若进行了两次交易修改子串[a,b], [c,d], 则两个区间之间要么相同, 要么不相交! 
思路1: 由于「修改区间不相交」的限制条件, 可以考虑 #DP
    
另见 [灵神](https://leetcode.cn/problems/minimum-cost-to-convert-string-ii/solutions/2577877/zi-dian-shu-floyddp-by-endlesscheng-oi2r/)
    """
    def minimumCost(self, source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
        # 仍然计算最短路!
        nodes = list(set(original) | set(changed))
        edges = defaultdict(list)
        for u,v,c in zip(original, changed, cost):
            edges[u].append((v,c))
        def bfs(u):
            res = {}
            h = [(0,u)]
            while h:
                c,v = heapq.heappop(h)
                if v in res: continue
                res[v] = c
                for v2,c2 in edges[v]:
                    if v2 not in res or c+c2 < res[v2]:
                        heapq.heappush(h, (c+c2,v2))
            return res
        dist = {u:bfs(u) for u in nodes}

        # 利用DP计算
        n = len(source)
        dp = [0] + [inf]*n
        for i in range(n):
            # NOTE: 根据字符串长度枚举, 复杂度 O(n L^2), 超时!
            # if source[i]==target[i]: dp[i+1] = dp[i]
            # for j in range(i+1):
            #     if source[j:i+1] in dist and target[j:i+1] in dist[source[j:i+1]]:
            #         dp[i+1] = min(dp[i+1], dp[j]+dist[source[j:i+1]][target[j:i+1]])

            # 思路2: 按照字符串长度枚举! 复杂度有下降~
            if source[i] == target[i]: dp[i+1] = dp[i]
            # vis 记录考虑过的字符串长度，如果考虑过无需再看 —— LC中不加这个刚刚过, 不过加了可以减少时间到 2s
            vis = set()
            for v in dist:
                if i >= len(v) - 1 and len(v) not in vis and source[i-len(v)+1:i+1] in dist and target[i-len(v)+1:i+1] in dist[source[i-len(v)+1:i+1]]:
                    dp[i+1] = min(dp[i+1], dist[source[i-len(v)+1:i+1]][target[i-len(v)+1:i+1]] + dp[i-len(v)+1])
                    vis.add(len(v))
        return dp[-1] if dp[-1]<inf else -1

    
sol = Solution()
result = [
    # sol.numberGame(nums = [5,4,2,3]),
    # sol.maximizeSquareArea(m = 4, n = 3, hFences = [2,3], vFences = [2]),
    # sol.maximizeSquareArea(m = 6, n = 7, hFences = [2], vFences = [4]),
    # sol.maximizeSquareArea(3,9,[2],[8,6,5,4]),

    # sol.minimumCost(source = "abcd", target = "acbe", original = ["a","b","c","c","e","d"], changed = ["b","c","b","e","b","e"], cost = [2,5,5,1,2,20]),
    # sol.minimumCost(source = "aaaa", target = "bbbb", original = ["a","c"], changed = ["c","b"], cost = [1,2]),
    # sol.minimumCost(source = "abcd", target = "abce", original = ["a"], changed = ["e"], cost = [10000]),

    # sol.minimumCost(source = "abcd", target = "acbe", original = ["a","b","c","c","e","d"], changed = ["b","c","b","e","b","e"], cost = [2,5,5,1,2,20]),
    sol.minimumCost(source = "abcdefgh", target = "acdeeghh", original = ["bcd","fgh","thh"], changed = ["cde","thh","ghh"], cost = [1,3,5]),
    sol.minimumCost(source = "abcdefgh", target = "addddddd", original = ["bcd","defgh"], changed = ["ddd","ddddd"], cost = [100,1578])



]
for r in result:
    print(r)
