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
https://oi-wiki.org/math/number-theory/gcd/


Easonsi @2023 """
class Solution:
    """  """
    
    
    
    
    
    

    """ 1819. 序列中不同最大公约数的数目 #hard #题型 #gcd #公约数
给定一个数组, 对于其所有的子序列 (不要求连续), 问所有子序列的公约数一共有多少中不同的数字.
约束: 数组长度 1e5; 元素大小 C 2e5
提示: **数组中存在gcd为g的子序列, 等价于, 「数组中所有g的倍数」这一组数的gcd为g**. 
    证明: 否则, 它们的最大公因数一定大于g.
思路1: 因此, 对于每一个可能的公因子 1...C, 从数组中找出其所有倍数, 计算其gcd即可.
    复杂度: 每个g最多的倍数有 `C/1,C/2,...C/C`, 之和渐进为 `ClogC`. 对于gcd, 利用 #辗转相除 法复杂度为 O(logC). 因此整体 `O(C log^2C)`
    事实上, 这个复杂度可以进一步缩紧. 用到的是: **计算m个数字的公约数的复杂度不是 `m logC`, 而是 `m + 2logC`, 也即计算两个数共因子的复杂度logC可以从线性系数中拿出来. 原因在于, 在计算m个数共约数的过程中数字在不断变小. 具体见 [zero](https://leetcode.cn/problems/number-of-different-subsequences-gcds/solution/xu-lie-zhong-bu-tong-zui-da-gong-yue-shu-lrka/) 的评论.
关联: 「AtCoder Beginner Contest 191 F」
思路1.1: 灵神做的两点优化
    1] 子序列长度为1, 数字本身就成立
    2] 子序列长度至少为2. 则对于枚举判断的g (不在原数组中, 排除情况1), 要使其为某一子序列的gcd, 则至少要有 2g,3g 两个元素! 因此, 我们枚举的范围只需要到 C//3 即可!!
    [灵神](https://leetcode.cn/problems/number-of-different-subsequences-gcds/solution/ji-bai-100mei-ju-gcdxun-huan-you-hua-pyt-get7/)
"""
    def countDifferentSubsequenceGCDs(self, nums: List[int]) -> int:
        # 思路1, from [zero](https://leetcode.cn/problems/number-of-different-subsequences-gcds/solution/xu-lie-zhong-bu-tong-zui-da-gong-yue-shu-lrka/)
        nums = set(nums)
        mx = max(nums)
        ans = 0
        # 尝试遍历所有可能的公约数
        for g in range(1, mx+1):
            gnow = None # 当前匹配的nums中g的倍数的 gcd
            # 遍历nums中所有g的倍数
            for y in range(g, mx+1, g):
                if y in nums:
                    if gnow is None: gnow = y
                    else: gnow = math.gcd(gnow, y)
                    # 若当前gcd已经等于g, 说明可以得到这个 g
                    if gnow==g:
                        ans += 1
                        break
        return ans
    def countDifferentSubsequenceGCDs(self, nums: List[int]) -> int:
        ans, mx = 0, max(nums)
        has = [False] * (mx + 1)
        for x in nums:
            if not has[x]:
                has[x] = True
                ans += 1  # 单独一个数也算
        for i in range(1, mx // 3 + 1):  # 优化循环上界
            if has[i]: continue
            g = 0  # 0 和任何数 x 的最大公约数都是 x
            for j in range(i * 2, mx + 1, i):  # 枚举 i 的倍数 j
                if has[j]:  # 如果 j 在 nums 中
                    g = math.gcd(g, j)  # 更新最大公约数
                    if g == i:  # 找到一个答案（g 无法继续减小）
                        ans += 1
                        break  # 提前退出循环
        return ans

    
sol = Solution()
result = [
    # sol.countDifferentSubsequenceGCDs(nums = [6,10,3]),
    # sol.countDifferentSubsequenceGCDs(nums = [5,15,40,5,6]),
]
for r in result:
    print(r)
