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
https://leetcode-cn.com/contest/biweekly-contest-98
灵神: https://www.bilibili.com/video/BV15D4y1G7ms/
Easonsi @2023 """
class Solution:
    """ 6359. 替换一个数字后的最大差值 """
    def minMaxDifference(self, num: int) -> int:
        s = str(num)
        mn = int(s.replace(s[0], '0'))
        mx = num
        for c in s:
            if c!='9':
                mx = int(s.replace(c, '9'))
                break
        return mx-mn
    
    """ 6361. 修改两个元素的最小分数  """
    def minimizeSum(self, nums: List[int]) -> int:
        nums.sort()
        return min(
            nums[-1]-nums[2],
            nums[-2]-nums[1],
            nums[-3]-nums[0],
        )
    
    """ 6360. 最小无法得到的或值 #medium 数组中的一组数字的或可以构成很多数字, 求arr中最小的无法构成的 最小非零整数. 限制: n 1e5
思路1: 有用的只有 bit_count()==1 的幂
    因为是或运算, 对于 0..010..0, 只有它本身才能得到! 可知, 若有哪一位无法得到, 那么一定是最小的那个无法得到的数字
    因此, 问题转为, 求arr中最小不存在的幂
    1.1 采用 #哈希表 复杂度 O(n + logU)
思路1.2 脑筋急转弯 + #lowbit 优化
    可以进一步优化到 O(n) 时间, 利用 #位运算
    用一个 mask 记录所有的幂, 例如得到 110011
        如何判断是否为幂? (x & (x - 1)) == 0
    那么答案就是第一个0的位置. 
        我们知道第一个非零位可以用 x&-x 得到. 我们对mask取反之后用该操作即可!
关联: 「2154. 将找到的值乘以 2」
[灵神](https://leetcode.cn/problems/minimum-impossible-or/solution/nao-jin-ji-zhuan-wan-pythonjavacgo-by-en-7j89/)
"""
    def minImpossibleOR(self, nums: List[int]) -> int:
        s = set(nums)
        i = 1
        while True:
            if i not in s:
                return i
            i <<=1
    def minImpossibleOR(self, nums: List[int]) -> int:
        # 思路1.2 可以进一步优化到 O(n) 时间, 利用 #位运算
        mask = 0
        for x in nums:
            if (x & (x - 1)) == 0:  # x 是 2 的幂次
                mask |= x
        mask = ~mask
        return mask & -mask  # lowbit

    """ 2154. 将找到的值乘以 2 对于一个数字ori, 若能够在arr中找到它, 就不断*2
思路1: #哈希表. 复杂度 O(n + logU)
思路2: 类似「最小无法得到的或值」 #位运算 
    记录ori的所有幂级别的倍数; 然后找到最小的不存在的幂
"""
    def findFinalValue(self, nums: List[int], original: int) -> int:
        s = set(nums)
        while original in s:
            original *= 2
        return original
    def findFinalValue(self, nums: List[int], original: int) -> int:
        # 思路2: 类似「最小无法得到的或值」 #位运算 
        mask = 0
        for x in nums:
            if x%original==0:
                p = x//original
                if (p & (p-1)) == 0:  # 倍数是 2 的幂次
                    mask |= p
        mask = ~mask    # 取反后，找最低位的 1（lowbit = mask & -mask）
        return original * (mask & -mask)  # lowbit

    """ 6358. 更新数组后处理求和查询 #hard 题目比较复杂, 总结就是, 对于一个0/1序列, 需要实现一个函数完成 [l,r] 范围的反转操作, 并实现求和操作
限制: n 1e5; 操作次数 q 1e5
思路1: Python 直接暴力转为二进制数可以过?! 
    是一个非常大的数字
思路2: #线段树 #模版题 #题型 见 [segment-tree]
    复杂度: O(n + q logn)
[灵神](https://leetcode.cn/problems/handling-sum-queries-after-update/solution/xian-duan-shu-by-endlesscheng-vx80/)
"""
    def handleQuery(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        # 思路1: Python 直接暴力转为二进制数可以过?! 
        s = sum(nums2)
        x = int(''.join(map(str, nums1[::-1])), 2)
        ans = []
        for op,l,r in queries:
            if op==1:
                y = (1<<(r-l+1)) - 1
                y <<= l
                x ^= y
            elif op==2:
                s += l * x.bit_count()
            else:
                ans.append(s)
        return ans


sol = Solution()
result = [
    # sol.minMaxDifference(11891),
    # sol.minimizeSum(nums = [1,4,7,8,5]),
    sol.minImpossibleOR([2,1]),
]
for r in result:
    print(r)
