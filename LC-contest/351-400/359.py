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
https://leetcode.cn/contest/weekly-contest-359
https://leetcode.cn/circle/discuss/SIJedb/

Easonsi @2023 """
class Solution:
    """ 2828. 判别首字母缩略词 """
    def isAcronym(self, words: List[str], s: str) -> bool:
        return ''.join(w[0] for w in words) == s
    
    """ 2829. k-avoiding 数组的最小总和 """
    def minimumSum(self, n: int, k: int) -> int:
        used = []
        for i in range(1, 100):
            if k-i in used: continue
            used.append(i)
            if len(used) == n: break
        return sum(used)
    
    """ 2830. 销售利润最大化 #medium 对于 [0,n-1] 的商品, 有一组购买 (s,e,gold) 表示换下这一片段的出价, 问最高收益.
限制: n 1e5; gold 1e3
思路1: 按照 (e,) 排序, #DP
    """
    def maximizeTheProfit(self, n: int, offers: List[List[int]]) -> int:
        offers.sort(key=lambda x: x[1])
        dp = [0] * (n+1)
        idx = 0; m = len(offers)
        for i in range(n):
            dp[i+1] = dp[i]
            while idx<m and offers[idx][1]==i:
                s,e,gold = offers[idx]
                dp[i+1] = max(dp[i+1], dp[s]+gold)
                idx += 1
        return dp[-1]
    
    """ 2831. 找出最长等值子数组 #medium 最多从数组中删掉k个元素, 问相同元素的子数组的最大长度
限制: n 1e5; 
思路1: #二分
    对于一个给定的目标x, 则等价于在 x+k的长度内至少有元素重复x, 可以 #滑动窗口 O(n) 求解
    复杂度: O(n logn)
思路2: #双指针
    用  {v: [idxs]} 来记录相同元素出现的位置! 然后在每个 [idxs] 数组上用双指针! 
    对于 [l,r] 的指针范围内, 需要删除的数量为 arr[r]-arr[l]+1 - (r-l+1)
    复杂度: O(n)
    """
    def longestEqualSubarray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        def check(x):
            l = x + k
            cnt = Counter(nums[:l])
            mx = max(cnt.values())
            if mx >= x: return True
            for i in range(l, n):
                cnt[nums[i-l]] -= 1
                cnt[nums[i]] += 1
                mx = max(mx, cnt[nums[i]])
                if mx >= x: return True
            return False
        ans = 0
        l,r = 1, n
        while l<=r:
            mid = (l+r)//2
            if check(mid):
                ans = mid
                l = mid + 1
            else:
                r = mid-1
        return ans
            


sol = Solution()
result = [
    # sol.minimumSum(n = 5, k = 4),
    # sol.minimumSum(n = 2, k = 6),
    # sol.minimumSum(3,6),
    # sol.maximizeTheProfit(n = 5, offers = [[0,0,1],[0,2,2],[1,3,2]]),
    # sol.maximizeTheProfit(n = 5, offers = [[0,0,1],[0,2,10],[1,3,2]]),
    sol.longestEqualSubarray(nums = [1,1,1,1,1,1,1,1,1,1], k = 0),
    sol.longestEqualSubarray(nums = [1,3,2,3,1,3], k = 3),
    sol.longestEqualSubarray(nums = [1,1,2,2,1,1], k = 2),
    
]
for r in result:
    print(r)
