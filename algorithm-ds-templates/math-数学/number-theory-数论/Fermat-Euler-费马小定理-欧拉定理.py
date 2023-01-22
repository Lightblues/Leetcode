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
https://oi-wiki.org/math/number-theory/fermat/


Easonsi @2023 """
class Solution:
    """ 1806. 还原排列的最少操作步数 #medium #题型 #数学
原本的长尾偶数的排列为 perm = 0,1,...n-1. 现每次进行操作: `f(i) = perm[i/2] if i%2==0 else perm[(i-2)/2 + n/2]` 问经过多少次操作后被还原.
限制: 长度 [2, 1000]
思路1: #归纳 #猜想. 
    可知, 在每一步中, 将原数组的前一半扩充到偶数位上, 后一半扩充到奇数位上.
    画出一步中每个位置的变化情况, 可见 0/n-1 位不变, 其他位置发生「轮转」.
    因此 #猜想: 其他位的轮转次数相同, 因此仅考虑其中一个即可. 定义轮转函数 f, 例如当 n=6, idx=1, 这个数字在操作中依次变为 1,2,4,3,1... 因此答案为 4.
思路2: 更为数学的 #证明
    除了0/n-1位置保持不变之外, 其他位置的变换关系可以统一写成 `f(i)≡2i mod(n-1)`, 因此有 `f^k(i) ≡ 2^k i mod(n-1)`
    为了还原, 需要满足 `2^k i mod(n-1) = i mod(n-1)` (可以看到与i无关)
    根据 #欧拉定理, 答案一定 <=n-1, 这样就保证了时间复杂度. 
    因此, 只需要模拟找到第一个满足 2^k=i mod(n-1) 的k即可.
[官答](https://leetcode.cn/problems/minimum-number-of-operations-to-reinitialize-a-permutation/solution/huan-yuan-pai-lie-de-zui-shao-cao-zuo-bu-d9cn/)
"""
    def reinitializePermutation(self, n: int) -> int:
        m = [0] * n
        for i in range(n):
            if i%2 == 0: m[i] = i//2
            else: m[i] = n//2 + (i-1)//2
        cnt = 1
        init = 1; idx = 1
        while m[idx] != init:
            idx = m[idx]
            cnt += 1
        return cnt
    def reinitializePermutation(self, n: int) -> int:
        """ 根据数学推导, 模拟找到第一个满足 2^k=i mod(n-1) 的k """
        if n == 2:
            return 1
        step, pow2 = 1, 2
        while pow2 != 1:
            step += 1
            pow2 = pow2 * 2 % (n - 1)
        return step

    
    
    
    
    
    

    
sol = Solution()
result = [
    # sol.reinitializePermutation(2),
    # sol.reinitializePermutation(4),
    # sol.reinitializePermutation(6),
    # sol.reinitializePermutation(8),
]
for r in result:
    print(r)
