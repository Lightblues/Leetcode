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
@20220824 """
class Solution:
    """ 给定一个数组, 计算所有长度为奇数的子数组的和. 限制: 长度 100 """
    def sumOddLengthSubarrays(self, arr: List[int]) -> int:
        acc = list(accumulate(arr, initial=0))
        n = len(arr)
        ans = 0
        for i in range(1, n+1, 2):
            for j in range(n-i+1):
                ans += acc[j+i] - acc[j]
        return ans
    
    """ 在图中判断两点是否相连. 限制: 节点, 边 1e5 """
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        visited = [False] * n
        visited[source] = True
        q = deque([source])
        while q:
            u = q.popleft()
            for v in g[u]:
                if not visited[v]:
                    visited[v] = True
                    q.append(v)
        return visited[destination]
    
    """ 目标子串为, 交换顺序后可以变为回文串. 对于给定的字符串求最大目标子串长度. 限制: 字符串长度 1e5
思路0: 尝试二分, 但实际上是错的: 因为例如 `1212` 对于长度为2的子串是没有awesome的.
思路1: 记录回文串要求进行 #状压
    注意到是否为回文串仅有字符串中各个字符的奇偶性决定, 因此, 用一个0/1字符串 mask 表示该子串.
    对于当前mask, 与其编辑距离不超过1的子串相减可构成回文串(满足条件). 而要找到最长的回文串, 用一个哈希表记录每个mask最早出现的位置即可.
    如何找到相邻串? 回文串的要求是, 前缀计数相减, 数量为奇数的字符最多出现一次. 对应到mask表示, 有 `nei(mask) = {mask, mask ^ (1<<i for i in range(10))}`.
    复杂度: `O(n C)` 这里的C的字符数量.
"""
    def longestAwesome(self, s: str) -> int:
        s = list(map(int, s))
        n = len(s)
        def check(l):
            # check whether exist awesome substring of length l
            cnt = Counter(s[:l])
            cntOdds = sum(1 for c in cnt if cnt[c] % 2)
            if cntOdds<=1: return True
            for i in range(l, n):
                if s[i] in cnt and cnt[s[i]] % 2: cntOdds -= 1
                else: cntOdds += 1
                cnt[s[i]] += 1
                cnt[s[i-l]] -= 1
                cntOdds += 1 if cnt[s[i-l]] % 2 else -1
                if cntOdds<=1: return True
            return False
        l,r = 1,n
        ans = 0
        while l<=r:
            mid = (l+r)//2
            if check(mid):
                ans = mid
                l = mid+1
            else:
                r = mid-1
        return ans
    def longestAwesome(self, s: str) -> int:
        # 思路1: 记录回文串要求进行 #状压
        s = list(map(int, s))
        MX = 2<<10
        mask2neighbors = [[] for _ in range(MX)]
        for mask in range(MX):
            mask2neighbors[mask].append(mask)
            for i in range(10):
                mask2neighbors[mask].append(mask ^ (1<<i))
        mask2idx = [None] * MX
        mask2idx[0] = -1
        ans = 0
        mask = 0
        for i,a in enumerate(s):
            mask ^= (1<<a)
            if mask2idx[mask] is None:
                mask2idx[mask] = i
            for nei in mask2neighbors[mask]:
                if mask2idx[nei] is not None:
                    if i-mask2idx[nei] > ans:
                        ans = i-mask2idx[nei]
        return ans
sol = Solution()
result = [
    # sol.sumOddLengthSubarrays(arr = [1,4,2,5,3]),
    sol.longestAwesome("3242415"),
    sol.longestAwesome("12345678"),
    sol.longestAwesome("10120"),
]
for r in result:
    print(r)
