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
https://leetcode.cn/contest/weekly-contest-428
T2 题目很炫, 有点意思

T4 的 DP 条件搞了好久, 逻辑上需要加强! 
Easonsi @2024 """
class Solution:
    """ 3386. 按下时间最长的按钮 """
    def buttonWithLongestTime(self, events: List[List[int]]) -> int:
        mx = 0; idx = 0; pre = 0
        for i,t in events:
            if t - pre > mx:
                mx = t - pre
                idx = i
            elif t - pre == mx:
                idx = min(idx, i)
            pre = t
        return idx
    
    """ 3387. 两天自由外汇交易后的最大货币数 #medium 给定两天的汇率转换图, 求第一天的一单位 x 货币到第二天结束最多可以是多少. (一天可以进行任意次转换)
限制: 边数量 10
思路1: 只需要计算两天 x -> y -> x 的汇率情况, 取最大即可! 
    """
    def maxAmount(self, initialCurrency: str, pairs1: List[List[str]], rates1: List[float], pairs2: List[List[str]], rates2: List[float]) -> float:
        def build_ratio(pairs, rates):
            g = defaultdict(list)
            for (u,v), r in zip(pairs, rates):
                g[u].append((v, r))
                g[v].append((u, 1/r))
            radios = {initialCurrency: 1.0}
            def dfs(u, fa, vv=1):
                for v, r in g[u]:
                    if v == fa: continue
                    radios[v] = vv * r
                    dfs(v, u, vv * r)
            dfs(initialCurrency, None)
            return radios
        ratios1 = build_ratio(pairs1, rates1)
        ratios2 = build_ratio(pairs2, rates2)
        mx = 1
        for x in ratios1.keys() & ratios2.keys():
            mx = max(mx, ratios1[x] / ratios2[x])
        return mx
    
    """ 3388. 统计数组中的美丽分割 #medium 定义一个美丽分割: 将数组分为 num1, num2, num3 三个子数组, 要求 nums1 是 nums2 的 前缀, 或者 nums2 是 nums3 的前缀. 求分割数量. 
限制: n 5e3; val 50
思路1: 计算 LCP 数组
    定义 lcp(i,j) 表示 nums[i:], nums[j:] 的最长公共前缀, i<=j
    递推:
        若 nums[i]==nums[j]: lcp[i,j] = lcp[i+1,j+1] + 1
        else: lcp[i,j] = 0
    边界: lcp[x, n] = 0
    枚举分割:
        条件1: i <= j-i and lcp[0,i] >= i
        条件2: n-j+1 >= j-i and lcp[i,j] >= j-i
ling: https://leetcode.cn/problems/count-beautiful-splits-in-an-array/solutions/3020939/liang-chong-fang-fa-lcp-shu-zu-z-shu-zu-dwbrd/
    """
    def beautifulSplits(self, nums: List[int]) -> int:
        n = len(nums)
        lcp = [[0]*(n+1) for _ in range(n+1)]
        for i in range(n-1,-1,-1): # NOTE 需要从后往前
            for j in range(n-1,i-1,-1):
                if nums[i]==nums[j]: lcp[i][j] = lcp[i+1][j+1] + 1
        ans = 0
        for i in range(1, n-1):
            for j in range(i+1, n):
                if (i<=j-i and lcp[0][i]>=i) or (n-j+1>=j-i and lcp[i][j] >= j-i): ans += 1
        return ans

    """ 3389. 使字符频率相等的最少操作次数 #hard 定义3种操作: 1) 删除一个; 2) 添加一个; 3) 将一个字符变为字母表下一个 (z不能变为a). 问将s变为 "所有字母出现次数相同" 所需最少操作数.
限制: n 2e4
思路1: #DP + 枚举
    假设知道了 target, 如何计算操作数? -- DP!
    注意, 分析可知, 对于一个位置, 没有必要先加后减! (也即把 a 变为 c)
    对于每个未知, 维护变为 0/target 的最小代价, #DP, 参考: https://leetcode.cn/problems/minimum-operations-to-make-character-frequencies-equal/solutions/3020622/mei-ju-dp-by-tsreaper-trnh/
    复杂度: O(A * n) 其中A未字母数量. 
拓展: ling https://leetcode.cn/problems/minimum-operations-to-make-character-frequencies-equal/solutions/3020630/mei-ju-dpfen-lei-tao-lun-pythonjavacgo-b-ahfn/
    """
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - ord('a')] += 1
        def check(target: int) -> int:
            dp = [[0,0] for _ in range(27)] # 前i个满足条件, 并且第i个变为 0/target 的最小操作数. 
            dp[1] = [cnt[0], abs(target-cnt[0])]
            for i in range(1, 26):
                dp[i+1][0] = min(dp[i]) + cnt[i]
                op0 = dp[i][0]
                if cnt[i] > target:
                    op0 += cnt[i] - target
                else:
                    op0 += max((target-cnt[i])-cnt[i-1], 0)
                op1 = dp[i][1]
                if cnt[i] > target:
                    op1 += cnt[i] - target
                else:
                    op1 += max((target-cnt[i])-max(cnt[i-1]-target, 0), 0)
                dp[i+1][1] = min(op0, op1)
            return min(dp[-1])
        return min(check(t) for t in range(max(cnt)+1))




sol = Solution()
result = [
    # sol.buttonWithLongestTime( events = [[1,2],[2,5],[3,9],[1,15]]),
    # sol.maxAmount(initialCurrency = "EUR", pairs1 = [["EUR","USD"],["USD","JPY"]], rates1 = [2.0,3.0], pairs2 = [["JPY","USD"],["USD","CHF"],["CHF","EUR"]], rates2 = [4.0,5.0,6.0]),

    sol.beautifulSplits(nums = [1,1,2,1]),
    sol.beautifulSplits([2,2,0,0,0,0,0,1,2,2,0,0,0,1,0]),

    # sol.makeStringGood(s = "acab"),
    # sol.makeStringGood("aaabbc"),
    # sol.makeStringGood("gigigjjggjjgg"),
    # sol.makeStringGood("ympylhyyyhmyhlypylyphylhpyyynyhplymyyylyppyypnhllympymnnyylmh")
]
for r in result:
    print(r)
