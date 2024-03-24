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
https://leetcode-cn.com/contest/biweekly-contest-119
T4有些暴力, 不过回顾了Floyd算法~
Easonsi @2023 """
class Solution:
    """ 2956. 找到两个数组中的公共元素 """
    def findIntersectionValues(self, nums1: List[int], nums2: List[int]) -> List[int]:
        s = set(nums1) & set(nums2)
        return len([i for i in nums1 if i in s]), len([i for i in nums2 if i in s])
    
    """ 2957. 消除相邻近似相等字符 """
    def removeAlmostEqualCharacters(self, word: str) -> int:
        pre = " "
        ans = 0
        for c in word:
            if abs(ord(c) - ord(pre)) <= 1:
                ans += 1
                pre = " "
            else:
                pre = c
        return ans
    
    """ 2958. 最多 K 个重复元素的最长子数组 """
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        l = 0
        cnt = Counter()
        ans = 0
        for r, x in enumerate(nums):
            while cnt[x]+1 > k:
                cnt[nums[l]] -= 1
                l += 1
            cnt[x] += 1
            ans = max(ans, r-l+1)
        return ans

    """ 2959. 关闭分部的可行集合数目 #hard n个分部之间有r条路径, 两两都有路径. 要求关闭一部分, 使得关闭之后, 任意两个分部之间的距离再max限制内. 求可行的方案数
限制: n 10; r 1e3, 一条路的长度 1e3, maxDistance 1e5
思路1: 枚举所有可能的子集, 每个验证!
[ling](https://leetcode.cn/problems/number-of-possible-sets-of-closing-branches/solutions/2560722/er-jin-zhi-mei-ju-floydgao-xiao-xie-fa-f-t7ou/)
Floyd
    2642. 设计可以求最短路径的图类 1811
    1334. 阈值距离内邻居最少的城市 1855
    2101. 引爆最多的炸弹 1880
二进制枚举
    78. 子集
    77. 组合
    1286. 字母组合迭代器 1591
    2397. 被列覆盖的最多行数 1719
    2212. 射箭比赛中的最大得分 1869
    1601. 最多可达成的换楼请求数目 2119
    320. 列举单词的全部缩写（会员题）
    """
    def numberOfSets(self, n: int, maxDistance: int, roads: List[List[int]]) -> int:
        dist = [[inf] * n for _ in range(n)]
        for i,j,w in roads:
            dist[i][j] = min(dist[i][j], w)
            dist[j][i] = min(dist[j][i], w)
        def check(s: int):
            """ 在给定子集为s的情况下, 是否满足条件 (Floyd算法计算所有点的最短路径) """
            f = deepcopy(dist)      # NOTE: Floyd 需要用dist数组开始! 不能初始化为 inf
            # Floyd
            for k in range(n):  # 中间点, 最大限制
                if (s >> k & 1) == 0: continue
                for i in range(n):
                    if (s >> i & 1) == 0: continue
                    for j in range(n):
                        if (s >> j & 1) == 0: continue
                        f[i][j] = min(f[i][j], f[i][k] + f[k][j])
            # check
            for i in range(n):
                if (s >> i & 1) == 0: continue
                for j in range(i):
                    if (s >> j & 1) == 0: continue
                    if f[i][j] > maxDistance: return False
            return True
        return sum(check(s) for s in range(1 << n))

    
sol = Solution()
result = [
    # sol.removeAlmostEqualCharacters(word = "aaaaa"),
    # sol.removeAlmostEqualCharacters("abddez"),
    # sol.maxSubarrayLength(nums = [1,2,3,1,2,3,1,2], k = 2),
    sol.numberOfSets(n = 3, maxDistance = 5, roads = [[0,1,2],[1,2,10],[0,2,10]]),
    sol.numberOfSets(n = 3, maxDistance = 5, roads = [[0,1,20],[0,1,10],[1,2,2],[0,2,2]]),
]
for r in result:
    print(r)
