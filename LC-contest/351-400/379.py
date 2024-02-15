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
https://leetcode.cn/contest/weekly-contest-379
https://leetcode.cn/circle/discuss/dvN3g7/

有水平的一次, T4 有点难, 复杂度分析有意思!
Easonsi @2023 """
class Solution:
    """ 3000. 对角线最长的矩形的面积 """
    def areaOfMaxDiagonal(self, dimensions: List[List[int]]) -> int:
        mx, ans = 0,0
        for w,h in dimensions:
            ds = w**2 + h**2
            if ds > mx:
                mx = ds
                ans = w*h
            elif ds == mx:
                ans = max(ans, w*h)
        return ans
    
    """ 3001. 捕获黑皇后需要的最少移动次数 #medium 在8*8的棋盘上, 有一个车和象, 检查需要几步可以捕获黑皇后
注意: 不能跳过另一个棋子!
[ling](https://leetcode.cn/problems/minimum-moves-to-capture-the-queen/solutions/2594432/fen-lei-tao-lun-jian-ji-xie-fa-pythonjav-aoa8/) 完全一样
    """
    def minMovesToCaptureTheQueen(self, a: int, b: int, c: int, d: int, e: int, f: int) -> int:
        # if a==e or b==f or (c+d)==(e+f) or (c-d)==(e-f):
        #     return 1
        if a==e:
            if c!=a or (d-b)*(d-f)>0: return 1
        if b==f:
            if d!=b or (c-a)*(c-e)>0: return 1
        if c+d==e+f:
            if a+b!=c+d or (a-c)*(a-e)>0: return 1
        if c-d==e-f:
            if a-b!=c-d or (a-c)*(a-e)>0: return 1
        return 2
    
    """ 3002. 移除后集合的最多元素数 #medium 分别从两个大小为n的数组中移除 n/2 个元素, 问最终两个合起来得到的集合的最大元素数
限制: n 2e4
思路1: 分析两个集合的关系
    记交集数量、两个集合各自独有的元素数量为 i, a, b, 元素限制 tt = n//2
    则两个元素分别可以取 min(tt, a/b) 个, 然后再看 i个元素是否可以再加进去
思路2: 两种思考问题的角度：移除元素/添加元素
[ling](https://leetcode.cn/problems/maximum-size-of-a-set-after-removals/solutions/2594380/tan-xin-pythonjavacgo-by-endlesscheng-ymuh/)
    """
    def maximumSetSize(self, nums1: List[int], nums2: List[int]) -> int:
        tt = len(nums1) // 2
        s1, s2 = set(nums1), set(nums2)
        num_intersection = len(s1 & s2)
        a, b = len(s1)-num_intersection, len(s2)-num_intersection
        a_limit, b_limit = min(tt, a), min(tt, b)
        ans = a_limit
        if a_limit < tt:
            num_intersection -= (tt-a_limit)
            ans = tt
        ans += min(b_limit+num_intersection, tt)
        return ans
    
    """ 3003. 执行操作后的最大分割数量 #hard 对于一个字符串, 定义其「分割数量」为反复执行「选择最长前缀进行分割, 前缀最多包含 k 个 不同 字符」操作得到的数量. 
最多修改原始 s的一个字符, 问可以得到的最大分割数量
限制: n 1e4; k 26
思路1: 记忆化搜索+记录字符集合
    定义 dfs(i, mask, changed) 表示遍历到位置i, 当前字符串的字符集合为mask (二进制表示) 的情况下, 后续可以构造的最大分割数. 其中 changed 表示是否修改过
    返回 dfs(0, 0, False)
    重点是复杂度分析! 对于DP来看状态空间数量. (i, mask) 不同的数量有多少?
        由于最多修改一次, 对于每个位置, 其前缀mask最多有 Z^2 种可能, 其中 Z=26
思路2: 前后缀分解
    首先证明「对于 s 的任意后缀，从左往右分割出的段数，等于从右往左分割出的段数」
    复杂度: O(n)
[ling](https://leetcode.cn/problems/maximize-the-number-of-partitions-after-operations/solutions/2595072/ji-yi-hua-sou-suo-jian-ji-xie-fa-pythonj-6g5z/)
    """
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        n = len(s)

        @lru_cache(None)
        def dfs(i, mask, changed):
            if i == n: return 1     # frontair
            c = ord(s[i]) - ord('a')

            # 1. 不修改
            new_mask = mask | (1 << c)
            if new_mask.bit_count() <= k:
                res = dfs(i+1, new_mask, changed)
            else:
                # 分割出一个子串，这个子串的最后一个字母在 i-1
                res = dfs(i+1, 1<<c, changed) + 1
            if changed: return res
            
            # 2. 修改
            # 枚举把 s[i] 改成 a,b,c,...,z
            for j in range(26):
                new_mask = mask | (1 << j)
                if new_mask.bit_count() <= k:
                    # res2 = dfs(i+1, new_mask, True)       # 注意! 这里没有更新 res! 是错的!
                    res = max(res, dfs(i + 1, new_mask, True))
                else:
                    res = max(res, dfs(i + 1, 1 << j, True) + 1)
            return res
        return dfs(0, 0, False)

    
sol = Solution()
result = [
    sol.maxPartitionsAfterOperations(s = "accca", k = 2),
    sol.maxPartitionsAfterOperations(s = "aabaab", k = 3),
    sol.maxPartitionsAfterOperations("ghorzzjwaqhcaeibwxwedecgs", 1),
]
for r in result:
    print(r)
