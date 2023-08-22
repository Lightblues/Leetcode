from easonsi.util.leetcode import *


""" 
https://leetcode.cn/contest/weekly-contest-358
Easonsi @2023 """

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# 限制范围内, 计算每个数字的质因子数量
maxi = 10 ** 5
score = [0] * (maxi + 1)
for i in range(2, maxi + 1):
    if not score[i]:
        for j in range(i, maxi + 1, i):
            score[j] += 1


class Solution:
    """ 6939. 数组中的最大数对和 """
    def maxSum(self, nums: List[int]) -> int:
        mx2numx = defaultdict(list)
        for x in nums:
            mx = max(str(x))
            mx2numx[mx].append(x)
        ans = -1
        for nums in mx2numx.values():
            if len(nums)<2: continue
            ans = max(ans, sum(sorted(nums)[-2:]))
        return ans
    
    """ 6914. 翻倍以链表形式表示的数字 #medium #链表 """
    def doubleIt(self, head: Optional[ListNode]) -> Optional[ListNode]:
        def dfs(head: ListNode):
            if not head: return 0
            carry = dfs(head.next)
            x = 2*head.val + carry
            x, carry = x%10, x//10
            head.val = x
            return carry
        carry = dfs(head)
        if carry:
            head = ListNode(carry, head)
        return head
    
    """ 7022. 限制条件下元素之间的最小绝对差 #medium #题型 在距离至少为x的限制下, 数组中两元素差值最小
限制: N 1e5
思路1: 顺序考虑, 每次 #二分 找到可选的最接近的元素
    对于位置为i的元素, 其可以和 [0,i-k] 的元素计算差值, 二分找到最接近的元素
    那么需要有序队列来维护可匹配项
"""
    def minAbsoluteDifference(self, nums: List[int], x: int) -> int:
        from sortedcontainers import SortedList
        ava = SortedList()
        ans = inf
        for i in range(x,len(nums)):
            ava.add(nums[i-x])
            a = nums[i]
            idx = ava.bisect_left(a)
            if idx>0:
                ans = min(ans, abs(a-ava[idx-1]))
            if idx<len(ava):
                ans = min(ans, abs(a-ava[idx]))
        return ans

    """ 7023. 操作使得分最大 #hard 对于一个数组进行k次操作, 将每次操作的分数累乘计算最大值
每次操作选取不同的区间 [l,r] 计算分数. 分数计算规则为 从这一范围内, 选择「质数分数最高的元素」计算得分; 质数分数即不同质因子的数量, 相同则优先前面的
限制: n 1e5 k 1e9
"""
    def maximumScore(self, nums: List[int], k: int) -> int:
        mod = 10**9+7
        # NOTE: 内部算的复杂度太高了!!
        # @lru_cache(None)
        # def get_primes(x):
        #     # 注意! 1的质因子数量为0
        #     # if x==1: return 0
        #     primes = []
        #     for i in range(2,x+1):
        #         if x%i==0:
        #             primes.append(i)
        #             while x%i==0:
        #                 x //= i
        #     return len(primes)
        # nprimes = [get_primes(x) for x in nums]
        nprimes = [score[x] for x in nums]
        n = len(nums)
        # 计算每个元素作为输出的左右边界 (计算可用区间的数量)
        left = [0] * n
        st = []
        for i,x in enumerate(nprimes):
            while st and st[-1][0]<x:
                st.pop()
            if st: left[i] = st[-1][1]+1
            st.append((x,i))
        right = [n-1] * n
        st = []
        for i in range(n-1,-1,-1):
            x = nprimes[i]
            while st and st[-1][0]<=x:
                st.pop()
            if st: right[i] = st[-1][1]-1
            st.append((x,i))
        # 
        ava = zip(nums, range(n), left, right)
        ava = sorted(ava, key=lambda x: x[0], reverse=True)
        ans = 1; idx = 0
        while k:
            x,i,l,r = ava[idx]
            idx += 1
            mx = (i-l+1)*(r-i+1)
            mx = min(mx, k)
            ans = ans * pow(x, mx, mod) % mod
            k -= mx
        return ans
            
    
sol = Solution()
result = [
    # sol.minAbsoluteDifference(nums = [4,3,2,4], x = 2),
    # sol.minAbsoluteDifference(nums = [1,2,3,4], x = 3),
    # sol.maximumScore(nums = [8,3,9,3,8], k = 2),
    # sol.maximumScore(nums = [19,12,14,6,10,18], k = 3),
    sol.maximumScore([1,7,11,1,5], 14),
]
for r in result:
    print(r)
