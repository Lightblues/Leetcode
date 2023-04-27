from easonsi import utils
from easonsi.util.leetcode import *
""" 
https://leetcode-cn.com/contest/biweekly-contest-49
@2022 """
class Solution:
    """ 1812. 判断国际象棋棋盘中一个格子的颜色 """
    def squareIsWhite(self, coordinates: str) -> bool:
        return ((ord(coordinates[0])-ord('a')) + (ord(coordinates[1])-ord('1'))) % 2 != 0
    
    """ 1813. 句子相似性 III #medium #题型
有两个单词单词序列(句子), 问能否在某一个序列中插入一个任意序列(句子), 使得原本的两个句子相等.
思路1: #两端匹配
    注意到, 由于最多只能插入一个序列, 无非就是左右两端, 或者中间.
    这样, 在上面的任意情况下, 长序列从两端出发, 都可以完全匹配短序列.
    因此, 采用 #两端匹配, 用长序列从两侧匹配短的, 完全覆盖了则说明可以.
思路0: 贪心匹配, 错了!
    原本打算用短序列顺序匹配长序列, 用一个 `flag` 记录是否用过了插入的机会.
    但这样有问题, 例如 "A" 和 "a A b A" 的例子.
"""
    def areSentencesSimilar(self, sentence1: str, sentence2: str) -> bool:
        # 思路1: #两端匹配
        words1, words2, = sentence1.split(), sentence2.split()
        # 令 words1 是长度较长的
        if len(words2) > len(words1):
            words1, words2 = words2, words1
        n = len(words2)
        # 统计所有分别可以匹配多长
        left = 0
        while left<n and words2[left]==words1[left]:
            left += 1
        right = 0
        while right<n and words2[-right-1]==words1[-right-1]:
            right += 1
        return left+right>=n
    
    """ 1814. 统计一个数组中好对子的数目 """
    def countNicePairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        c = Counter()
        for num in nums:
            diff = num - int(str(num)[::-1])
            c[diff] += 1
        ans = 0
        for _, v in c.items():
            if v >= 2:
                ans += v*(v-1)//2
        return ans % MOD
        
    """ 1815. 得到新鲜甜甜圈的最多组数 #hard #hardhard
每次烤 batchSize 个甜甜圈, 然后有一个数组 groups, 表示每次的客人需要购买的数量. 当某次顾客购买的甜甜圈中没有上一次卖剩下的情况下, 该顾客是开心的. 问, 任意调整 groups 顺序的情况下, 最多开心的数量.
    约束: 每组数量 batchSize<=9; 客人组的长度最多为 30.
思路0: 问题等价于, 对于数组进行分组, 使得每组和都是batchSize的倍数, 问最大分组数. 
思路1: #状态压缩+#记忆化搜索 见 [here](https://leetcode.cn/problems/maximum-number-of-groups-getting-fresh-donuts/solution/cji-yi-hua-sou-suo-by-oldyan-658o/)
    显然, 每一组顾客的数量, 重要的是其 %bs 的值, 根据这个值对顾客进行分组. 
        因此, 可以用一个最多长为9的数组对状态进行压缩! 
    记忆化搜索, 记 dfs(r, rest) 表示之前分配剩余的顾客数量为r, 剩余的顾客组的压缩表示为rest情况下的最大分组数量. 
        尝试用每种类型的顾客来组合r: dfs(r, rest) = (r==0) + max_i{ dfs((r+i)%bs, rest\i) }, 其中i为rest中还有的顾客组类型. 
    复杂度分析: 注意状态表示需要一个长bs的数组
        转移方程: O(bs)
        什么情况下状态数最多? 直觉是均匀, 本题中最多30组顾客, 数组长度最多9-1 (因为 %=0的情况不用算), 因此状态数最多情况为 [4,4,4,4,4,4,3,3], 在 (3+1)^2 * (4+1)^6 范围内
思路1.2: 采用 #状态压缩
    对于状态数组rest, 其长度为bs-1, 每个元素的范围在 [0,30], 因此可以用一个整数来表示状态.
    state = sum_i{ rest[i] * (31**i) }
"""
    def maxHappyGroups(self, batchSize: int, groups: List[int]) -> int:
        # 记录顾客组类型的数量
        gtypes = [0] * batchSize
        for i in groups: gtypes[i%batchSize] += 1
        # 特殊: 可以整除的单独处理
        ans = gtypes[0]; gtypes[0] = 0
        # 记忆化搜索
        @lru_cache(None)
        def dfs(r, rest):
            # 注意边界条件!!
            if sum(rest)==0: return 0
            mx = 0
            for i, v in enumerate(rest):
                if v==0: continue
                mx = max(mx, dfs((r+i)%batchSize, rest[:i]+(v-1,)+rest[i+1:]))
            return mx + (r==0)
        return ans + dfs(0, tuple(gtypes))

    def maxHappyGroups(self, batchSize: int, groups: List[int]) -> int:
        # 记录顾客组类型的数量
        gtypes = [0] * batchSize
        for i in groups: gtypes[i%batchSize] += 1
        base = 31
        state = sum([gtypes[i+1] * (base**i) for i in range(batchSize-1)])
        @lru_cache(None)
        def dfs(r, rest: int):
            mx = 0
            # 这样写不需要考虑上面代码中的边界条件
            for i in range(batchSize-1):
                v = rest // (base**i) % base
                if v==0: continue
                mx = max(mx, dfs((r+i+1)%batchSize, rest - (31**i)) + (r==0))
            return mx
        dfs.cache_clear()
        return dfs(0, state) + gtypes[0]

sol = Solution()
result = [
    # sol.squareIsWhite(coordinates = "h3"),
    # sol.areSentencesSimilar(sentence1 = "My name is Haley", sentence2 = "My Haley"),
    # sol.areSentencesSimilar(sentence1 = "of", sentence2 = "A lot of words"),
    # sol.areSentencesSimilar("A", "a A b A")
    # sol.countNicePairs(nums = [42,11,1,97]),
    # sol.countNicePairs(nums = [13,10,35,24,76]),
    # sol.countNicePairs([352171103,442454244,42644624,152727101,413370302,293999243])
    sol.maxHappyGroups(batchSize = 3, groups = [1,2,3,4,5,6]),
    sol.maxHappyGroups(batchSize = 4, groups = [1,3,2,5,2,2,1,6]),
    
    
]
for r in result:
    print(r)
