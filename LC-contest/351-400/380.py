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
https://leetcode.cn/contest/weekly-contest-380

Easonsi @2023 """
class Solution:
    """ 3005. 最大频率元素计数 """
    def maxFrequencyElements(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        fcnt = Counter(cnt.values())
        max_freq, ans = 0, 0
        for k,v in fcnt.items():
            if k > max_freq:
                max_freq = k
                ans = k * v
        return ans
    
    """ 3006. 找出数组中的美丽下标 I #medium 给定字符串 s, a,b 和整数k, 找到所有的「美丽下标 i」, 满足从i位置出发的子串为a, 从j位置出发的子串为b, 并且 |j-i| <=k 
限制: n 1e5; a,b 长度 10
思路1: KMP + 二分
    复杂度: KMP的复杂度位 O(n); 引入如果用二分来遍历pos的话复杂度位 O(n logn), 也可以优化为双指针, 则复杂度 O(n)
    [ling](https://leetcode.cn/problems/find-beautiful-indices-in-the-given-array-i/solutions/2603716/fei-bao-li-zuo-fa-kmper-fen-cha-zhao-pyt-0o8y/)
    """
    def beautifulIndices(self, s: str, a: str, b: str, k: int) -> List[int]:
        pos_a = self.kmp(s, a)
        pos_b = self.kmp(s, b)

        ans = []
        for pos in pos_a:
            idx = bisect_left(pos_b, pos)
            if (idx < len(pos_b) and pos_b[idx] - pos <= k) or (idx > 0 and pos - pos_b[idx - 1] <= k):
                ans.append(pos)
        return ans
    
    def kmp(self, text: str, pattern: str) -> List[int]:
        m = len(pattern)
        pi = [0] * m
        c = 0
        for i in range(1, m):
            v = pattern[i]
            while c and pattern[c] != v:
                c = pi[c - 1]
            if pattern[c] == v:
                c += 1
            pi[i] = c

        res = []
        c = 0
        for i, v in enumerate(text):
            v = text[i]
            while c and pattern[c] != v:
                c = pi[c - 1]
            if pattern[c] == v:
                c += 1
            if c == len(pattern):
                res.append(i - m + 1)
                c = pi[c - 1]
        return res

    """ 3007. 价值和小于等于 K 的最大数字 #medium 对于一个整数num, 假设其二进制是s, 记其「价值」为所有在整数x的整数倍的位置上为1的个数. 
现在给定 1...xx 各个数字的「价值和」, 问在价值和限制最大k的条件下, 最大的数字xx是多少? 
限制: k 1e15; x 8
思路1: 二分
    如何对于给定的xx来计算其下数字的价值和? 
        例如对于 x=2, 则 [00,01] 没有价值, [10,11] 的价值为1 —— 也即, 对于每 2^x 个数字, 其后 2^{x-1} 个数字在该位的价值为 1
        此外, 我们对所有数字都 / 2^x, 则可以计算下一个 2x 位的价值累计
    二分的上界是多少? 
参见 [ling](https://leetcode.cn/problems/maximum-number-that-sum-of-the-prices-is-less-than-or-equal-to-k/) 
给了三种解析! 
    """
    def findMaximumNumber(self, k: int, x: int) -> int:
        def f(m, x):
            ans = 0
            tmp = 2**(x-1)
            while m >= tmp:
                a,b = divmod(m, 2*tmp)
                ans += (a * tmp) + max(0, b-(tmp-1))  # 注意数字包括了 [1...xx]
                tmp *= 2**x
            return ans
        
        l,r = 0, k<<(x)
        ans = 0
        while l <= r:
            mid = (l+r)//2
            if f(mid, x) <= k: 
                l = mid+1
                ans = mid
            else: r = mid-1
        return ans


    """ 3008. 找出数组中的美丽下标 II #hard 给定字符串 s, a,b 和整数k, 找到所有的「美丽下标 i」, 满足从i位置出发的子串为a, 从j位置出发的子串为b, 并且 |j-i| <=k 
限制: n 5e5; a,b 长度 5e5
    """
    
sol = Solution()
result = [
    # sol.maxFrequencyElements(nums = [1,2,2,3,1,4]),
    # sol.findMaximumNumber(k = 9, x = 1),
    # sol.findMaximumNumber(k = 7, x = 2),
    sol.findMaximumNumber(57, 4),

    # sol.beautifulIndices(s = "isawsquirrelnearmysquirrelhouseohmy", a = "my", b = "squirrel", k = 15),
]
for r in result:
    print(r)
