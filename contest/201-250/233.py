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
https://leetcode.cn/contest/weekly-contest-233
@2022 """
class Solution:
    """ 1800. 最大升序子数组和 """
    def maxAscendingSum(self, nums: List[int]) -> int:
        ans = 0
        sidx = 0; s = 0
        for i,num in enumerate(nums+[-1]):
            if i==0 or num>nums[i-1]:
                s += num
            else:
                sidx = i
                ans = max(ans, s); s = num
        return max(ans, s)
    
    """ 1801. 积压订单中的订单总数 #medium #题型 #模拟
按照时间顺序有一批订单. 每个时间包含了一组订单 (price, amount, type=0/1) 订单类型 0/1表示买/卖, amount个订单可以分开来处理. 订单有「积压」也即等待处理的情况. 在每一个时间, 若新来的订单为采购, 并且积压的销售订单中有小于该价格的, 则按照价格从小到大购买; 反之亦然. 问最后积压的订单数量.
限制: 数组长度 1e5; price, amount 1e9; 对结果取模.
思路1: 利用两个 #有序数组 分别记录「积压」的销售/购买订单. 然后按照顺序匹配订单即可. (当然, 也可以用 #堆 来处理)
总结: 本题其实模拟了按照时间顺序的一个「市场」, buyer想要最低价格, seller想要最高价格. 然后按照时序依次匹配的过程.
"""
    def getNumberOfBacklogOrders(self, orders: List[List[int]]) -> int:
        from sortedcontainers import SortedList
        buySD = SortedList(); sellSD = SortedList()
        for p,a,t in orders:
            if t==0:    # buy
                while a and len(sellSD) and sellSD[0][0]<=p:
                    if sellSD[0][1] >= a:
                        sellSD[0][1] -= a
                        if sellSD[0][1]==0: sellSD.pop(0)
                        a = 0
                        break
                    else:
                        a -= sellSD[0][1]
                        sellSD.pop(0)
                if a: buySD.add([p,a])
            else:
                while a and len(buySD) and buySD[-1][0]>=p:
                    if buySD[-1][1] >= a:
                        buySD[-1][1] -= a
                        if buySD[-1][1]==0: buySD.pop()
                        a = 0; break
                    else:
                        a -= buySD[-1][1]
                        buySD.pop()
                if a: sellSD.add([p,a])
        mod = 10**9+7
        acc = 0
        for p,a in buySD:
            acc = (acc+a)%mod
        for p,a in sellSD:
            acc = (acc+a)%mod
        return acc
        
    
    """ 1802. 有界数组中指定下标处的最大值 #medium
要求构造一个符合条件的数组 nums: 1) 长度为n, 所有元素为正数; 2) 相邻元素差值最多为1; 3) 所有元素之和不超过 maxSum; 4) 在 index 的位置的元素最大. 要求返回合法的数组中, index 位置元素的最大值.
限制: n, maxSum [1, 1e9]; 
思路1: #二分
    显然, 构造的数组是一个在index处有一个「山峰」的结构.
    在给定index位置高度的情况, 容易计算整个数组最小和为多少. 因此可以用二分来搜索.
思路2: #数学 实际上可以直接归纳出公式
[官答](https://leetcode.cn/problems/maximum-value-at-a-given-index-in-a-bounded-array/solution/you-jie-shu-zu-zhong-zhi-ding-xia-biao-c-aav4/)
"""
    def maxValue(self, n: int, index: int, maxSum: int) -> int:
        def calc(h, d):
            # 计算 sum{h-1, h-d}
            return (2*h-d-1)*d/2
        def check(h):
            # 分成四个部分: index 处的柱子; 左右的三角形; (可能)剩余的高度为1的地方
            d1 = min(h-1, index)
            d2 = min(h-1, n-index-1)
            s = h + calc(h, d1) + calc(h, d2) + (n-1-d1-d2)
            return s<=maxSum
        l,r = 1, maxSum
        ans = 1
        while l<=r:
            mid = (l+r)//2
            if check(mid):
                ans = mid
                l = mid+1
            else:
                r = mid-1
        return ans
        
    """ 1803. 统计异或值在范围内的数对有多少 #hard #字典树 #题型 给定一个长n的数组, 要求对于所有 (i,j) 的数对, 其XOR值在 `[low, high]` 范围内的数量.
限制: 数组长度n, 元素大小, low,high 2e4; 
思路1: 采用 #字典树 see [trie]
思路2: 相较于字典树, 直接用哈希表+优化
    对于 [low,high] 范围内的每个元素t, 统计数组中两个元素 xor结果为t的数量. 
        为此, 先用cnt记录数组中元素出现次数. 枚举所有元素x, 利用异或的性质, 匹配元素应该是 y=t ^ x. 因此数量为 cnt[x] * cnt[y].
        但这样复杂度为 O(n^2) 需要优化. 
    考虑对「一组t」同时计数, 也即「划分 [0,high] 为不同的区间」 (问题转化为 `query([0,high])-query([0,low-1])` )
        例如, 对于 t in [0,10100], 可以划分为 [00000,01111], [10000,10011], [10100,10100] 这些区间
            对于第一个区间, 只要 x^y 的前1个比特符合要求, 就能从这一区间内找到一个t满足 x^y=t. 
        具体而言, 如何实现? 在每一次迭代中, 需要对cnt进行合并; 丢掉后面不相关的位!
    实际上, 这里虽然没有用 #字典树, 但是思路和字典树是一致的, 高位表达的信息更多些.
    见 [灵神](https://leetcode.cn/problems/count-pairs-with-xor-in-a-range/solution/bu-hui-zi-dian-shu-zhi-yong-ha-xi-biao-y-p2pu/)

思路9.1: 利用numpy 进行暴力搜索. see [here](https://leetcode.com/problems/count-pairs-with-xor-in-a-range/discuss/1119721/Python-NumPy-bruteforce-O(N2)/)
思路9.2: 神仙思路, 用了 #快速沃尔什变换 [here](https://leetcode.cn/problems/count-pairs-with-xor-in-a-range/solution/kuai-su-wo-er-shi-bian-huan-onlognqiu-xi-fidb/)
    但其实复杂度也是 O(n log(n))
"""
    def countPairs(self, nums: List[int], low: int, high: int) -> int:
        # 利用 numpy 暴力. https://leetcode.com/problems/count-pairs-with-xor-in-a-range/discuss/1119721/Python-NumPy-bruteforce-O(N2)/
        import numpy as np
        numBits = max(max(x.bit_length() for x in nums), low.bit_length(), high.bit_length())
        freq = np.bincount(nums, minlength=(1 << numBits))
        targets = np.arange(low, high + 1)
        return int(sum(freq[targets ^ x].sum() for x in nums) // 2)
    def countPairs(self, nums: List[int], low: int, high: int) -> int:
        # 思路2: 相较于字典树, 直接用哈希表+优化
        # cnt 记录当前位的元素分布情况
        ans, cnt = 0, Counter(nums)
        high += 1   # +1
        while high:
            nxt = Counter()
            for x, c in cnt.items():
                # 注意这里的逻辑: 若当前最低位为1, 减掉这个1再统计!
                if high & 1: ans += c * cnt[x ^ (high - 1)]
                if low & 1:  ans -= c * cnt[x ^ (low - 1)]
                nxt[x >> 1] += c
            cnt = nxt       # 更新cnt. 注意其中的元素bit长度都减少了1
            low >>= 1
            high >>= 1
        return ans // 2

    
sol = Solution()
result = [
    # sol.maxAscendingSum(nums = [10,20,30,5,10,50]),
    # sol.maxValue(n = 4, index = 2,  maxSum = 6),
    # sol.maxValue(n = 6, index = 1,  maxSum = 10),
    # sol.getNumberOfBacklogOrders(orders = [[10,5,0],[15,2,1],[25,1,1],[30,4,0]]),
    # sol.getNumberOfBacklogOrders(orders = [[7,1000000000,1],[15,3,0],[5,999999995,0],[5,1,1]]),
    sol.countPairs(nums = [1,4,2,7], low = 2, high = 6),
    sol.countPairs(nums = [9,8,4,2,1], low = 5, high = 14),
]
for r in result:
    print(r)
