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
https://leetcode.cn/contest/weekly-contest-419
T3 不知道为啥 TLE 了
T4 感觉用 SortedList 有些作弊, 感觉重点是复杂度分析!

Easonsi @2023 """
class Solution:
    """ 3318. 计算子数组的 x-sum I """
    def findXSum(self, nums: List[int], k: int, x: int) -> List[int]:
        ans = []
        n = len(nums)
        for i in range(n-k+1):
            sub = nums[i:i+k]
            cnt = Counter(sub)
            vals = [(v,k) for k,v in cnt.items()]
            vals.sort(reverse=True)
            ks = [k for v,k in vals[:x]]
            ans.append(sum((k for k in sub if k in ks)))
        return ans
    
    """ 3319. 第 K 大的完美二叉子树的大小 """
    def kthLargestPerfectSubtree(self, root: Optional[TreeNode], k: int) -> int:
        vals = []
        def dfs(root: TreeNode) -> int:
            nonlocal vals
            if root is None: return 0
            nleft, nright = dfs(root.left), dfs(root.right)
            if nleft!=-inf and nleft == nright:
                vals.append(2*nleft+1)
                return 2*nleft+1
            return -inf
        dfs(root)
        vals.sort(reverse=True)
        return vals[k-1] if k <= len(vals) else -1

    """ 3320. 统计能获胜的出招序列数 #hard 三种字符之间 E > F > W > E 之间的循环胜利关系. 已知A的序列的情况下, 问B能获胜的出招序列数
限制: n 1e3
思路1: #DP 记 f(i,c,s) 表示位置i出c, 分数为s的出招序列数. 
    答案 sum{ f(n-1, ., s>0) }
[ling](https://leetcode.cn/problems/count-the-number-of-winning-sequences/solutions/2949448/jiao-ni-yi-bu-bu-si-kao-dpcong-ji-yi-hua-5tsk/)
    """
    def countWinningSequences(self, s: str) -> int:
        # TLE
        MOD = 10**9 + 7
        win = {
            'F': 'W',
            'W': 'E',
            'E': 'F',
        }
        chars = "FWE"
        n = len(s)
        @lru_cache(None)
        def f(i, c, score):
            # #wins for B in index=i, current state=c, accelerate score=score
            if i==0:
                if score==0 and c==s[0]: return 1
                elif score==1 and c==win[s[0]]: return 1
                elif score==-1 and win[c]==s[0]: return 1
                return 0
            if score + (n-i) <= 0: return 0
            acc = 0
            if c==s[i]: pre = score
            elif c==win[s[i]]: pre = score-1
            else: pre = score+1
            for ch in chars:
                if ch != c: acc += f(i-1, ch, pre)
            return acc % MOD
        ans = 0
        for ch in chars:
            ans += sum(f(n-1, ch, i) for i in range(1,n+1))
        return ans % MOD
    
    """ 3321. 计算子数组的 x-sum II #hard 对于一个长n的数组, 计算每个长为k的子数组的x-sum
x-sum 的定义: 统计子数组中元素出现次数, 仅保留出现次数前x个的元素 (相同的话保留数字大的), 统计这些元素的和
限制: n 1e5;  x 1e9
思路1: #有序数组
    [ling](https://leetcode.cn/problems/find-x-sum-of-all-k-long-subarrays-ii/solutions/2948867/liang-ge-you-xu-ji-he-wei-hu-qian-x-da-p-2rcz/)
思路2: #对顶堆
    什么是对顶堆? 为了 "支持插入和删除操作, 维护序列中的第k大的元素", 具体的实现方式可以用一个大顶堆和一个小顶堆来实现, 增加延迟删除性质! 
    参见 [oi-wiki](https://oi-wiki.org/ds/binary-heap/)
    """

sol = Solution()
result = [
    # sol.findXSum(nums = [1,1,2,2,3,4,2,3], k = 6, x = 2),
    sol.countWinningSequences( s = "FFF"),
    sol.countWinningSequences( s = "FWEFW"),
]
for r in result:
    print(r)
