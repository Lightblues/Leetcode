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
https://leetcode.cn/contest/weekly-contest-186

T3 对角线遍历 版本2 有启发性. T4用到了新学的「单调队列」有意思.

@2022 """
class Solution:
    """ 1422. 分割字符串的最大得分 """
    def maxScore(self, s: str) -> int:
        ans = score = (s[0] == '0') + s[1:].count('1')
        for c in s[1:-1]:
            score += 1 if c == '0' else -1
            ans = max(ans, score)
        return ans
    """ 1423. 可获得的最大点数 """
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        acc1 = list(accumulate(cardPoints[:k], initial=0))
        acc2 = list(accumulate(cardPoints[-k:][::-1], initial=0))
        return max(acc1[i] + acc2[k-i] for i in range(k+1))
    
    """ 1424. 对角线遍历 II #medium #题型 给定一组数组从上往下排列 (可能不是矩阵), 要求按照从左下到右上的方向一条一条对角线便利.
限制: 所有数字的数量 n 1e5.
思路1: 直接计算每个坐标在全矩阵下的idx. 然后排序. 复杂度 O(nlogn)
    例如, 对于一个矩阵, 按照遍历顺序定义每个位置的idx为
    0 2 5 9
    1 4 8
    3 7
    6
    由于所给的数组并不是规则的, 我们只根据 (i,j) 算到idx, 然后排序即可.
    如何计算? 假设 i+j=k 表示第k条对角线, 则其idx从 k(k+1)/2 开始, 再加上 j 即可.
"""
    def findDiagonalOrder(self, nums: List[List[int]]) -> List[int]:
        t = []
        for i, row in enumerate(nums):
            for j, num in enumerate(row):
                idx = i + j
                start = idx*(idx+1) // 2
                t.append((start + j, num))
        return [i[1] for i in sorted(t)]
    
    """ 1425. 带限制的子序列和 #hard #题型. 要求数组的字序列的最大和. 不过有限制: 所取的相邻元素在原数组中的位置距离不能超过k.
限制: 数组长度 n, k 1e5. 数组元素 -1e4~1e4.
思路1: 单调队列
    基本的 #DP 是记 `f[i]` 表示以 `nums[i]` 结尾的最大和. 那么有 `f[i] = max(f[i-k ... i-1], 0) + nums[i]`.
    但在本题下会超时. 于是考虑用一个 #单调队列 来记录合法范围内的最大值.
"""
    def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        dp = [-inf] * n
        q = deque() # (val, idx)
        for i,num in enumerate(nums):
            # idx 限制.
            while q and q[0][1] < i-k:
                q.popleft()
            dp[i] = num + max(0, q[0][0] if q else -inf)
            # 维护单调递减队列
            while q and q[-1][0] <= dp[i]:
                q.pop()
            q.append((dp[i], i))
        return max(dp)


    
sol = Solution()
result = [
    # sol.maxScore(cardPoints = [1,2,3,4,5,6,1], k = 3),
    # sol.maxScore(cardPoints = [2,2,2], k = 2),
    # sol.maxScore([96,90,41,82,39,74,64,50,30], 8),
    # sol.findDiagonalOrder(nums = [[1,2,3,4,5],[6,7],[8],[9,10,11],[12,13,14,15,16]]),
    sol.constrainedSubsetSum(nums = [10,2,-10,5,20], k = 2),
    sol.constrainedSubsetSum([-1,-2,-3], 1),
]
for r in result:
    print(r)
