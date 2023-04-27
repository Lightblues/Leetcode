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
https://leetcode.cn/contest/weekly-contest-305
@2022 """
class Solution:
    """ 6136. 算术三元组的数目 """
    def arithmeticTriplets(self, nums: List[int], diff: int) -> int:
        s = set(nums)
        ans = 0
        for a in nums:
            if a-diff in s and a+diff in s: ans += 1
        return ans
    
    """ 6139. 受限条件下可到达节点的数目 """
    def reachableNodes(self, n: int, edges: List[List[int]], restricted: List[int]) -> int:
        restricted = set(restricted)
        q = [0]
        g = collections.defaultdict(list)
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        visited = set()
        while q:
            node = q.pop()
            visited.add(node)
            for nei in g[node]:
                if nei not in visited and nei not in restricted:
                    q.append(nei)
        return len(visited)
    
    """ 2369. 检查数组是否存在有效划分 #medium #题型 其实不难, 但一开始想歪了结果WA了四发😭
对一个数组进行拆分, 合法的子数组为: 1) 两相同元素; 2) 三相同元素; 3) 三个连续递增数字, 例如 [1,2,3]. 问能否进行拆分.
思路0: 尝试对于情况3进行筛选, 一旦出现递增就标记为已使用. 但实际上是 #WA 的, 因为可能有 [1,1,2,3,4] 这种情况.
思路1: #DP
    对应三种情况, 递归 `f[i] = (nums[i]==nums[i-1]==nums[i-2] and f[i-3]) or (nums[i]==nums[i-1] and f[i-2]) or nums[i-2]+2==nums[i-1]+1==nums[i]`. 注意边界.
    1.1 写成 #记忆化 形式更加简单
[灵神](https://leetcode.cn/problems/check-if-there-is-a-valid-partition-for-the-array/solution/by-endlesscheng-8y73/)
"""
    def validPartition(self, nums: List[int]) -> bool:
        # 灵神优雅的代码
        n = len(nums)
        f = [True] + [False] * n
        for i, x in enumerate(nums):
            if i > 0 and f[i - 1] and x == nums[i - 1] or \
               i > 1 and f[i - 2] and (x == nums[i - 1] == nums[i - 2] or
                                       x == nums[i - 1] + 1 == nums[i - 2] + 2):
               f[i + 1] = True
        return f[n]
    def validPartition(self, nums: List[int]) -> bool:
        # 1.1 写成 #记忆化 形式更加简单
        def check3(a,b,c):
            # 检查三个数
            if a==b-1 and c==b+1: return True
            if a==b==c: return True
            return False
        @lru_cache(None)
        def f(i):
            if i<1: return False
            elif i==1: return nums[1]==nums[0]
            elif i==2: return check3(nums[0], nums[1], nums[2])
            else:
                if nums[i]==nums[i-1] and f(i-2): return True
                if check3(nums[i-2], nums[i-1], nums[i]) and f(i-3): return True
            return False
        return f(len(nums)-1)

    """ 2370. 最长理想子序列 #hard #DP 给定一个小写字母字符串, 要求最长的子序列, 使得相邻元素的差值都不超过k. 
思路1: 用一个哈希表lastIdx记录每个字母最近出现的位置. 
    遍历过程中对每个i,ch进行查找: f[i] = max{ f[lastIdx[ch-k...ch+k]] +1 }.
    复杂度: O(n C) 其中C为字符集大小
思路1.1: 直接 f[i] 记录以i字符结尾的最大长度即可
    见 [灵神](https://leetcode.cn/problems/longest-ideal-subsequence/solution/by-endlesscheng-t7zf/)
"""
    def longestIdealString(self, s: str, k: int) -> int:
        base = ord('a')
        s = [ord(c)-base for c in s]
        n = len(s)
        lastIdx = [-1] * 26
        f = [1] * n
        for i,ch in enumerate(s):
            for c in range(max(0, ch-k), min(26, ch+k+1)):
                if lastIdx[c] >= 0:
                    f[i] = max(f[i], f[lastIdx[c]]+1)
            lastIdx[ch] = i
        return max(f)
    def longestIdealString(self, s: str, k: int) -> int:
        # 灵神
        f = [0] * 26
        for c in s:
            c = ord(c) - ord('a')
            # Python 的简洁写法
            f[c] = 1 + max(f[max(c - k, 0): c + k + 1])
        return max(f)

sol = Solution()
result = [
    # sol.arithmeticTriplets(nums = [4,5,6,7,8,9], diff = 2),
    # sol.reachableNodes(n = 7, edges = [[0,1],[0,2],[0,5],[0,4],[3,2],[6,5]], restricted = [4,2,1]),
    # sol.longestIdealString(s = "acfgbd", k = 2),
    # sol.longestIdealString(s = "abcd", k = 3),
    sol.validPartition(nums = [4,4,4,5,6]),
    sol.validPartition(nums = [1,1,1,2]),
    sol.validPartition([579611,579611,579611,731172,731172,496074,496074,496074,151416,151416,151416]),
    sol.validPartition([730480,730481,730482,730483,730484,730485]),
    sol.validPartition([676575,676575,676575,533985,533985,40495,40495,40495,40495,40495,40495,40495,782020,782021,782022,782023,782024,782025,782026,782027,782028,782029,782030,782031,782032,782033,782034,782035,782036,782037,782038,782039,782040,378070,378070,378070,378071,378072,378073,378074,378075,378076,378077,378078,378079,378080,378081,378082,378083,378084,378085,378086,378087,378088,378089,378090,378091,378092,378093,129959,129959,129959,129959,129959,129959]),
    sol.validPartition([803201,803201,803201,803201,803202,803203]),
]
for r in result:
    print(r)
