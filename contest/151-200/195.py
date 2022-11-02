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
https://leetcode.cn/contest/weekly-contest-195
@2022 """
class Solution:
    """ 1496. 判断路径是否相交 """
    def isPathCrossing(self, path: str) -> bool:
        x, y = 0, 0
        visited = set()
        visited.add((x, y))
        for p in path:
            if p == 'N':
                y += 1
            elif p == 'S':
                y -= 1
            elif p == 'E':
                x += 1
            elif p == 'W':
                x -= 1
            if (x, y) in visited:
                return True
            visited.add((x, y))
        return False
    
    """ 1497. 检查数组对是否可以被 k 整除 """
    def canArrange(self, arr: List[int], k: int) -> bool:
        # Python 对于负数取mod的结果总是正的
        # 对于 C++和Java，负数的结果是负的，此时可以 xk = (x % k + k) % k 得到。
        arr = map(lambda x: x % k, arr)
        cnt = Counter(arr)
        for i in range(1, k//2+1):
            if cnt[i] != cnt[k-i]: return False
        # 特殊情况是可以整除
        if cnt[0]%2: return False
        return True
    
    """ 1498. 满足条件的子序列数目 #medium
给定一个数组， 问其子序列中， 满足最大元素和最小元素之和不大于 target 的数量。 限制： 数量 n 1e5
思路1: 对于每一个元素, 二分查找可以匹配的最大元素.
    我们枚举最小元素为第i位置的, 通过二分找到它可以匹配的最大元素位置j (实际上bisect是其下一个位置). 第i个元素必选, 其他元素可选有 `2^(j-i-1)` 种方案.))`
    复杂度: O(nlog(n))
"""
    def numSubseq(self, nums: List[int], target: int) -> int:
        mod = 10**9 + 7
        nums.sort()
        res = 0
        for i,v in enumerate(nums):
            j = bisect_right(nums, target-v)
            if j<=i: break
            res = (res + 2**(j-i-1)) % mod
        return res
    
    """ 1499. 满足不等式的最大值 #hard #题型
给定一组点， 要求在 xi,xj 在k范围内的， yi+yj+|xi-xj| 最大值。 限制: 点数量 1e5
思路1： #优先队列
    在枚举第j个元素， 与其匹配的前面的第j个元素， 分数为 `yi+yj+xj-xi`, 因此i的分数为 si = yi-xi. 
    因此, 用一个最小堆来记录 (si,xi) 信息; 在遍历j的时候, 通过 xj-xi 判断是否过期.
    复杂度: O(n logn)
"""
    def findMaxValueOfEquation(self, points: List[List[int]], k: int) -> int:
        # (-si, xi)
        q = []
        ans = -inf
        for x,y in points:
            while q and x-q[0][1] > k:
                heappop(q)
            if q:
                ans = max(ans, x+y-q[0][0])
            heappush(q, (-(y-x),x))
        return ans
    
    
sol = Solution()
result = [
    # sol.isPathCrossing(path = "NESWW"),
    # sol.canArrange(arr = [1,2,3,4,5,6], k = 7),
    # sol.canArrange([1,2,3,4,5,10,6,7,8,9], 5),
    # sol.numSubseq(nums = [3,5,6,7], target = 9),
    # sol.numSubseq(nums = [2,3,3,4,6,7], target  12),
    sol.findMaxValueOfEquation(points = [[1,3],[2,0],[5,10],[6,-10]], k = 1),
    sol.findMaxValueOfEquation(points = [[0,0],[3,0],[9,2]], k = 3)
]
for r in result:
    print(r)
