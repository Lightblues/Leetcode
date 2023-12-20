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
https://leetcode-cn.com/contest/biweekly-contest-115
https://leetcode.cn/circle/discuss/maICM3/

T3挺有意思, T4有些高级. 

Easonsi @2023 """
class Solution:
    """ 2899. 上一个遍历的整数 """
    def lastVisitedIntegers(self, words: List[str]) -> List[int]:
        ans = []
        s = []; before = []
        for w in words:
            if w=='prev':
                if s:
                    ans.append(s[-1])
                    before.append(s.pop())
                else:
                    ans.append(-1)
            else:
                while before:
                    s.append(before.pop())
                s.append(int(w))
        return ans
    
    """ 2900. 最长相邻不相等子序列 I 从arr中找到一个子序列, 要求对于groups中定义的0/1组, 答案中的相邻元素所属组别不同 
思路1: #贪心 可知, 一定可以选择一个个元素
    """
    def getWordsInLongestSubsequence(self, n: int, words: List[str], groups: List[int]) -> List[str]:
        ans = []
        pre = -1
        for w, g in zip(words, groups):
            if g!=pre:
                ans.append(w)
                pre = g
        return ans
    
    """ 2901. 最长相邻不相等子序列 II #medium #DP #题型 从arr中找到一个子序列, 要求所选相邻元素 1] 有不同group, 2] 长度相等且汉明距离为1. 注意字符串长度可能不同
限制: n 1e3 字符串长度 10
思路1: 
    根据可否相邻, 可以构建0/1矩阵, 问题等价于找到最长的路径. (单向边)
    给定图, 如何找到最长路径? #DP 
    如何返回答案? 
    """
    def getWordsInLongestSubsequence(self, n: int, words: List[str], groups: List[int]) -> List[str]:
        def dist(s,t):
            if len(s)!=len(t):
                return -1
            return sum(i!=j for i,j in zip(s,t))
        g = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i+1,n):
                if groups[i]==groups[j]: continue
                d = dist(words[i], words[j])
                if d==1:
                    g[i].append(j)
        dp = [1] * n
        pre = [None] * n    # 保留DP路径, 用于重构
        for i in range(n):
            for j in g[i]:
                if dp[j]<dp[i]+1:
                    pre[j] = i
                    dp[j] = dp[i]+1
        mx = max(dp)
        idx = dp.index(mx)
        ans = []
        while idx is not None:
            ans.append(words[idx])
            idx = pre[idx]
        return ans[::-1]
    
    """ 2902. 和带限制的子多重集合的数目 #hard 对于一个arr, 找到满足和在[l,r]范围内的「子多重集合」的数量, 「子多重集合」的定义即要求 sorted(a) != sorted(b)
限制: n 2e4; arr之和 2e4; l,r 2e4; 对答案取模. 
思路1: 「多重背包方案数」问题, 进行优化
    注意到, 我们先对于元素进行cnt操作. 定义 f[i][j] 表示从前i种数字中得到j的方案数. 
        则 f[i][j] = f[i-1][j] + f[i-1][j-x] + f[i-1][j-2x] + ... + f[i-1][j-cx], 其中x,c分别是第i种数字的值和个数.
        而 f[i][j-x] = f[i-1][j-x] + f[i-1][j-2x] + f[i-1][j-3x] + ... + f[i-1][j-(c+1)x]
        汇总简化: f[i][j] = f[i][j-x] + f[i-1][j] - f[i-1][j-(c+1)x] 注意最后一项若 j-(c+1)x < 0 则为0
        这样, 我们就能在 O(1) 时间内进行更新
    整体而言, 外层对于cnt循环, 内层对于可以得到的数字j循环
    边界: 注意可能有数字0, 因此边界为 f[0][0] = cnt[0]+1 表示根据0的个数, 有多少种方案
    复杂度: 注意这里 S=sum(arr) <= 2e4, 因此arr中不同元素的个数载 sqrt{S} 级别!
        整体复杂度 O(S min(sqrt{S},n))
见 [灵神](https://leetcode.cn/problems/count-of-sub-multisets-with-bounded-sum/solutions/2482876/duo-zhong-bei-bao-fang-an-shu-cong-po-su-f5ay/)
    """
    def countSubMultisets(self, nums: List[int], l: int, r: int) -> int:
        MOD = 10 ** 9 + 7
        total = sum(nums)
        if l > total:
            return 0

        r = min(r, total)
        cnt = Counter(nums)
        f = [cnt[0] + 1] + [0] * r
        del cnt[0]

        s = 0
        for x, c in cnt.items():
            new_f = f.copy()
            s = min(s + x * c, r)  # 到目前为止，能选的元素和至多为 s
            for j in range(x, s + 1):  # 把循环上界从 r 改成 s，能快一倍
                new_f[j] += new_f[j - x]
                if j >= (c + 1) * x:
                    new_f[j] -= f[j - (c + 1) * x]
                new_f[j] %= MOD
            f = new_f
        return sum(f[l:]) % MOD

    
    
sol = Solution()
result = [
    # sol.lastVisitedIntegers(words = ["1","2","prev","prev","prev"]),
    
    # sol.getWordsInLongestSubsequence(n = 3, words = ["bab","dab","cab"], groups = [1,2,2]),
    # sol.getWordsInLongestSubsequence(n = 4, words = ["a","b","c","d"], groups = [1,2,3,4]),
    
    sol.countSubMultisets(nums = [1,2,2,3], l = 6, r = 6),
    sol.countSubMultisets(nums = [2,1,4,2,7], l = 1, r = 5),
    
]
for r in result:
    print(r)
