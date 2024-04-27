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
https://leetcode.cn/contest/weekly-contest-389

Easonsi @2023 """
class Solution:
    """ 3083. 字符串及其反转中是否存在同一子字符串 """
    def isSubstringPresent(self, s: str) -> bool:
        pairs = set([s[i:i+2] for i in range(len(s)-1)])
        s_rev = s[::-1]
        pairs_rev = set([s_rev[i:i+2] for i in range(len(s)-1)])
        return len(pairs & pairs_rev) > 0
    
    """ 3084. 统计以给定字符开头和结尾的子字符串总数 """
    def countSubstrings(self, s: str, c: str) -> int:
        n = s.count(c)
        return n*(n+1)//2
    
    """ 3085. 成为 K 特殊字符串需要删除的最少字符数 #medium 对于一个字符串, 可以删除其中的某些字符, 要求 |freq[i] - freq[j]| <= k, 问最少删除多少字符
限制: n 1e5
思路1: #前缀和
    唯一重要的是字符出现的次数. 
    滑窗维护当前的边界, cost包括两部分, 一块是对于更大的数字要减去, 另一部份是删除出现较小的数字. 
"""
    def minimumDeletions(self, word: str, k: int) -> int:
        cnt = list(Counter(word).values())
        cnt.sort(reverse=True)
        acc = list(accumulate(cnt, initial=0))
        ans = inf
        l = 0
        for i,v in enumerate(cnt):      # 
            while cnt[l]-v > k:
                l += 1
            cost = (acc[l] - (v+k)*l) + (acc[-1]-acc[i+1])
            ans = min(ans, cost)
        return ans
    
    """ 3086. 拾起 K 个 1 需要的最少行动次数 #hard 对于一个 0/1 数组, 选择在一开始选择一个坐标idx, 目标是在idx位置上收集到 k 个 1. 有两个操作:
1] 选择任意位置j将其 0 -> 1. 最后进行 maxChanges 次. 2] 选择相邻元素, 交换 (01 -> 10), 若结果是idx位置变成了1, 则收集一个. (一开始的idx位置若有1直接收集不算步骤)
限制: n,k 1e5. 
思路1: #中位数贪心
    注意: 除了idx原本就有1, 以及邻居有1的情况, 从其他地方转移过来的成本是要高于操作1+操作2两次的!
    因此, 优先用掉 maxChanges 次的组合操作, 剩下的 `k-maxChanges` 个 1 需要从原数组中转移
        NOTE: 也即在 maxChanges=0 的情况下, 问题转化为, 从原数组中找到一个位置 idx, 使其和相邻 k-maxChanges 个 1 的位置和 (成本) 最低 —— #中位数贪心
        对于这一问题, 「标准答案」是这些数组的中位数位置!!!
    边界: 什么情况下不能这样化简? 
        直接通过连续 (不大于3) 的1 + 加上组合操作直接达成! 例如对于 k=5, 有三个连续的1, 再加上2次组合操作直接完成! 
        因此, 边界条件是 c + maxChanges >= k, 其中c是连续1的个数 (不大于3)
    转化的问题: 对于处在 pos的若干位置, 选择一个位置idx, 使其和最相邻的x个元素的距离和最小
        思路: 枚举中位数, 然后用 #前缀和 来计算距离! 
    复杂度: O(n)
[ling](https://leetcode.cn/problems/minimum-moves-to-pick-k-ones/solutions/2692009/zhong-wei-shu-tan-xin-by-endlesscheng-h972/)

题单：中位数贪心

462. 最小操作次数使数组元素相等 II
2033. 获取单值网格的最小操作数 1672
2448. 使数组相等的最小开销 2005
2607. 使子数组元素和相等 2071
2967. 使数组成为等数数组的最小代价 2116
1478. 安排邮筒 2190
2968. 执行操作使频率分数最大 2444
1703. 得到连续 K 个 1 的最少相邻交换次数 2467
LCP 24. 数字游戏
296. 最佳的碰头地点 二维的情况（会员题）
    """
    def minimumMoves(self, nums: List[int], k: int, maxChanges: int) -> int:
        pos = []
        c = 0
        for i,x in enumerate(nums):
            if x==1:
                pos.append(i)
                c = max(c, 1)
                if i>0 and nums[i-1]==1:
                    c = max(c, 2)
                    if i>1 and nums[i-2]==1:
                        c = 3
        # boundary
        if c + maxChanges >= k:
            if c>=k:
                return k-1
            elif c>0:
                return (c-1) + 2*(k-c)
            else:
                return 2*k
        # greedy
        target_len = k - maxChanges
        acc = list(accumulate(pos, initial=0))
        n = len(pos)
        ans = inf
        for l in range(0, n-target_len+1):
            r = l + target_len - 1
            mid = (l+r)//2
            # 分割为 [l...mid], [mid..r] 两段
            cost = (mid-l+1)*pos[mid] - (acc[mid+1]-acc[l]) + \
                (acc[r+1]-acc[mid+1]) - (r-mid)*pos[mid]
            ans = min(ans, cost)
        return ans + 2*maxChanges

sol = Solution()
result = [
    # sol.minimumDeletions(word = "dabdcbdcdcd", k = 2),
    sol.minimumMoves(nums = [1,1,0,0,0,1,1,0,0,1], k = 3, maxChanges = 1),
    sol.minimumMoves(nums = [0,0,0,0], k = 2, maxChanges = 3),
    sol.minimumMoves([1,1], 2, 4),
    sol.minimumMoves([1,1], 1, 2),
]
for r in result:
    print(r)
