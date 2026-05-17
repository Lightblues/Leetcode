from typing import *
from math import comb, inf
from bisect import bisect_left
from itertools import accumulate, pairwise


"""
https://leetcode.cn/contest/weekly-contest-461
1. 三段式数组, 简单模拟
2. 平衡装运的最大数量, 简单贪心
3. 变为活跃状态的最小时间 - 对于一个随时间变化的序列, 计算最早满足条件的时间
    思路 1: 二分
    思路 2: 逆向思维
    NOTE: 可以用两个数组模拟双向链表!
3640. 三段式数组 II - 定义为严格上升-下降-上升的子数组, 要求最大和
    方法 1: 分组循环的方式 (双指针/滑窗) 找到三个区间, 代码比较细碎!
    方法 2: 状态机 DP, 删繁就简, 极为精彩!
Easonsi @2026 """


class Solution:
    """ 3637. 三段式数组 I """
    def isTrionic(self, nums: List[int]) -> bool:
        n = len(nums)
        # first
        p = 1
        while p<n and nums[p] > nums[p-1]:
            p += 1
        if p==1: return False
        # second
        q = p
        while q<n and nums[q] < nums[q-1]:
            q += 1
        if q==p or q==n: return False
        # last
        i = q
        while i<n and nums[i]>nums[i-1]:
            i += 1
        return i==n

    """ 3638. 平衡装运的最大数量 #5
"平衡装运" 定义为一个子数组, 其最后一个重量 < 最大重量. 给定一个数组, 问最多能够成多少个 "平衡装运"
限制: n 1e5
思路 1: 贪心
    """
    def maxBalancedShipments(self, weight: List[int]) -> int:
        pre_max = -1
        ans = 0
        for w in weight:
            if w<pre_max:
                ans += 1
                pre_max = -1
            else: pre_max = w
        return ans

    """ 3639. 变为活跃状态的最小时间 #5
对于一个字符串, 有一个 range(0,n-1) 的排列, 表示在 t 将 order[t] 位置变为 *; 若包含*的子串数量超过 k, 则表示激活. 问最小激活时间
限制: n 1e5
思路 1: 二分
    复杂度: O(n logn), 其中计算 check 的复杂度为 O(n) -- 如果用遍历的方法的话; 下面写的还要考虑 sort
思路 2: 逆向思维+双向链表
    NOTE: 注意正向 "加入 *" 的过程, 其实也是可以统计的; 不过要引入有序数组
    逆向: 一开始全为 * -- 共有 cnt = n(n+1)/2 个合法子串
    考虑将 i 还原为字母, 则需要直到左侧星号 l 和右侧星号 r
    - 减小的数量: 左侧 [l+1...i], 右侧 [i...r-1], 共计 (i-l) * (r-i)
    答案: 不断减去星号, 第一次 cnt<m 的时刻即为答案
    NOTE: 这里需要知道左侧/右侧最近邻, 可以 #数组模拟双向链表 来快速!
https://leetcode.cn/problems/minimum-time-to-activate-string/solutions/3741028/er-fen-da-an-pythonjavacgo-by-endlessche-6s8n/
"""
    def minTime(self, s: str, order: List[int], k: int) -> int:
        n = len(s)
        if n*(n+1)//2 < k: return -1
        mn_unvalid = n*(n+1)//2 - k + 1
        def check(m: int) -> bool:
            acc = 0
            pre = -1
            # NOTE: 下面方便起见用了 sort (逆向思维); 实际上可以通过记录 "上一个*位置" 遍历一遍来统计, 参见 link
            for i in sorted(order[:m+1]):
                acc += comb(i-pre, 2)
                if acc >= mn_unvalid: return False
                pre = i
            acc += comb(n-pre, 2)
            return acc < mn_unvalid
        return bisect_left(list(range(n)), True, key=check)

    def minTime(self, s: str, order: List[int], k: int) -> int:
        n = len(s)
        cnt = (n+1)*n//2
        if cnt < k: return -1

        # 数组模拟双向链表
        pre = list(range(-1, n))
        nxt = list(range(1, n+2))
        for t in range(n-1,-1,-1):  # 倒序
            i = order[t]
            l,r = pre[i],nxt[i]
            cnt -= (i-l)*(r-i)
            if cnt < k: return t
            # 删除链表中的 i
            pre[r] = l
            nxt[l] = r

    """ 3640. 三段式数组 II #6
三段式数组定义: l<p<q<r, 使得三段分别严格递增/递减/递增. 最所有三段子数组中, 和最大.
限制: n 1e5. 保证至少存在一个三段式子数组
思路 1: 枚举所有的递减完全区间. 要求最大:
    - 第一段, 从右往左求最大, 显然可以通过元素是否 >0 来终止
    - 第二段, 一定要包含
    - 第三段, 从左往右求最大, 可以维护一个 mx
    NOTE: 如何获取 "所有递减区间"? -- 本质上还是 "分组循环"
思路 2: #分组循环
    参见 ling, 比较长, 但核心对于 i 的维护同下面思路 1
思路 3: #状态机 DP
    寻找子问题:
        - 假设 i 为第三段最后一个元素, 则 i-1:
            - 第三段倒数第二个 -> 变为 i-1 作为第三段最后一个元素
            - bottom, -> i-1 作为第二段最后一个元素
        - 假设 i 为第二段最后一个元素, 考虑 i-1
            - 第二段倒数第二 -> 递归
            - top, -> i-1 作为第一段最后一个元素
        - 假设 i 为第一段最后一个元素, 考虑 i-1
            - 第一段倒数第二 -> 递归
            - 第一段第一个数!
    状态设计与状态转移方程
        定义 f[i,j] 表示位置i 作为 j \in {1,2,3} 段最后一个元素时候的最大和, 则有
        f(i,3) = max{ f(i-1,3), f(i-1,2) } + nums[i] | nums[i] > nums[i-1]
        f(i,2) = max{ f(i-1,2), f(i-1,2) } + nums[i], | nums[i] < nums[i-1]
        f(i,1) = max{ f(i-1,1), nums[i-1] } + nums[i]  | nums[i] > nums[i-1]
        以上转移非法时, 赋值 -inf
        初始值：f(0,j) = -inf
        答案: f(i,3) 最大值
https://leetcode.cn/problems/trionic-array-ii/solutions/3741020/fen-zu-xun-huan-on-shi-jian-o1-kong-jian-ewr5/
    """
    def maxSumTrionic(self, nums: List[int]) -> int:
        acc = list(accumulate(nums, initial=0))
        n = len(nums)
        def exp_l(i: int) -> int:
            # expend from i (asume nums[i-1] < nums[i])
            l = i-1
            while l>0 and 0<nums[l-1]<nums[l]: l-= 1
            return l
        def exp_r(j: int) -> int:
            r = j+1
            mx = s = nums[r]; mx_r = r
            while r<n-1 and nums[r+1]>nums[r]:
                r += 1
                s += nums[r]
                if s > mx:
                    mx = s
                    mx_r = r
            return mx_r
        ans = -inf
        i = 0
        while i<n:
            # 下面的 #分组循环, 本质上是在找 [top, bottom]
            start = i
            i += 1
            while i<n and nums[i]>nums[i-1]: i+= 1
            if i == start+1: continue  # 至少要有上升段
            peak = i - 1
            while i<n and nums[i]<nums[i-1]: i += 1
            if i == peak+1 or i==n or nums[i]==nums[i-1]: continue  # 第二段, 第三段都存在!
            bottom = i - 1
            # 
            l = exp_l(peak)
            r = exp_r(bottom)
            ans = max(ans, acc[r+1]-acc[l])
            i = bottom
        return ans if ans != -inf else -1

    def maxSumTrionic(self, nums: List[int]) -> int:
        ans = f1=f2=f3 = -inf
        for x,y in pairwise(nums):
            f3 = max(f3, f2) + y if y>x else -inf
            f2 = max(f2, f1) + y if y<x else -inf
            f1 = max(f1, x) + y if y>x else -inf
            ans = max(ans, f3)
        return ans


sol = Solution()
result = [
    # sol.minTime(s = "abc", order = [1,0,2], k = 2),
    # sol.minTime(s = "cat", order = [0,2,1], k = 6),
    # sol.minTime("itk", [2,0,1], 4),
    # sol.maxSumTrionic(nums = [0,-2,-1,-3,0,2,-1]),
    # sol.maxSumTrionic(nums = [1,4,2,7]),
    sol.maxSumTrionic([2,993,-791,-635,-569]),
]
for r in result:
    print(r)
