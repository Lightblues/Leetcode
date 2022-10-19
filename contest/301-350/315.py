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
https://leetcode.cn/contest/weekly-contest-315

前三题划水, 5min做出来, 结果T4想了一个小时做不出Orz... 想了个 O(n^2) 的算法
看了题解, 没想到思路异常的简单, 但当时真的想不到...

@2022 """
class Solution:
    """ 6204. 与对应负数同时存在的最大正整数 """
    def findMaxK(self, nums: List[int]) -> int:
        ans = -1
        s = set(nums)
        for a in nums:
            if a>0 and -a in s: ans = max(ans, a)
            # s.add(a)
        return ans
    
    """ 6205. 反转之后不同整数的数目 """
    def countDistinctIntegers(self, nums: List[int]) -> int:
        s = set(nums)
        for a in nums:
            s.add(int(str(a)[::-1]))
        return len(s)
    
    """ 6219. 反转之后的数字和 """
    def sumOfNumberAndReverse(self, num: int) -> bool:
        for a in range(num+1):
            if a + int(str(a)[::-1]) == num: return True
        return False
    
    """ 6207. 统计定界子数组的数目 #hard #题型 #review 给定一个数组. 通过给定 mn, mx 问所有子数组中, 其最小最大值分别是这两个数字的数量.
限制: n 1e5;
思路0: #TLE 尝试对于 mn, mx 两个数字, 计算其作为最小/最大值成立的区域. 然后两两匹配, 统计数量.
    关联: 2281. 巫师的总力量和
    花了将近一个小时才写好. 结果意识到复杂度是 O(n^2), 果然超时...
思路1: 顺序遍历, 考察以 idx为右端点的合法区间的数量.
    怎样才合法? 先不考虑超过 [mn,mx] 范围的数字, 则匹配的左端点数量取决于 `min(mn_i, mx_i)` 的位置, 这里的两个指标是最近的 mn, mx 的位置.
    在遍历过程中, 更新 mn,mx 作为最小/最大值的区域 (可能的左端点).
    见 [灵神](https://leetcode.cn/problems/count-subarrays-with-fixed-bounds/solution/jian-ji-xie-fa-pythonjavacgo-by-endlessc-gag2/)
思路2: #双指针 根据数据范围进行分割, 求解子问题.
    显然, 子数组不会跨越 [mn, mx] 范围之外的数字, 因此可以根据这些进行分割, 转化 **问题要求**「子数组中同时出现 mn,mx」
    该问题可以用一个经典的 双指针 求解: 遍历作为右端点的位置 i, 维护左端点使得 [j...i] 是同时包含两个数字的最小区间.
        具体而言, 遍历过程中记录 [i,j] 区间的两个数字的计数 cntMn, cntMx, 维护j使得区间最小.
    [here](https://leetcode.cn/problems/count-subarrays-with-fixed-bounds/solution/by-tsreaper-czkz/)
"""
    def countSubarrays(self, nums: List[int], minK: int, maxK: int) -> int:
        # 思路0: #TLE 尝试对于 mn, mx 两个数字, 计算其作为最小/最大值成立的区域. 然后两两匹配, 统计数量.
        n = len(nums)
        
        # 求左右边界, 注意这里的边界都是开区间
        rMin = [n] * n
        stack = []
        for i in range(n-1, -1, -1):
            while stack and stack[-1][0] >= nums[i]:
                stack.pop()
            rMin[i] = stack[-1][1] if stack else n
            stack.append((nums[i], i))
        lMin = [-1] * n
        stack = []
        for i in range(n):
            while stack and stack[-1][0] > nums[i]:
                stack.pop()
            lMin[i] = stack[-1][1] if stack else -1
            stack.append((nums[i], i))
        # print(f"lMin={lMin}, rMin={rMin}")
        rMax = [n] * n
        stack = []
        for i in range(n-1, -1, -1):
            while stack and stack[-1][0] < nums[i]:
                stack.pop()
            rMax[i] = stack[-1][1] if stack else n
            stack.append((nums[i], i))
        lMax = [-1] * n
        stack = []
        for i in range(n):
            while stack and stack[-1][0] <= nums[i]:
                stack.pop()
            lMax[i] = stack[-1][1] if stack else -1
            stack.append((nums[i], i))
        # print(f"lMax={lMax}, rMax={rMax}")
        
        idxMin = [i for i in range(n) if nums[i]==minK]
        minRange = {}
        for i in idxMin: minRange[i] = (lMin[i]+1, rMin[i]-1)
        idxMax = [i for i in range(n) if nums[i]==maxK]
        maxRange = {}
        for i in idxMax: maxRange[i] = (lMax[i]+1, rMax[i]-1)
        
        ans = 0
        for mn, (mnl, mnr) in minRange.items():
            for mx, (mxl, mxr) in maxRange.items():
                if not (mxl<=mn<=mxr and mnl<=mx<=mnr): continue
                l,r = max(mnl, mxl), min(mnr, mxr)
                il, ir = sorted([mn,mx])
                ans += (il-l+1) * (r-ir+1)
        return ans
        
    def countSubarrays(self, nums: List[int], minK: int, maxK: int) -> int:
        # 思路1: 顺序遍历, 考察以 idx为右端点的合法区间的数量.
        ans = 0
        # 最近的一个 mn, mx 的位置
        minL = maxL = -1
        # 最近的一个不合法位置的边界.
        valL = -1
        for i, x in enumerate(nums):
            if x==minK: minL = i
            if x==maxK: maxL = i
            if x<minK or x>maxK: valL = i
            l = min(minL, maxL) # [l...i] 范围内的数字进行满足了 mn,mx 边界
            # 注意, 需要与 valL 边界比较!!
            if l>valL: ans += l-valL
        return ans

    def countSubarrays(self, nums: List[int], minK: int, maxK: int) -> int:
        # 思路2: #双指针 根据数据范围进行分割, 求解子问题.
        def f(arr, mn,mx):
            ans = 0
            cntMn = cntMx = 0
            j = 0
            for i,x in enumerate(arr):
                if x==mn: cntMn += 1
                if x==mx: cntMx += 1
                while cntMn>0 and cntMx>0:
                    # 找到第一个不符合条件的位置.
                    if arr[j]==mn: cntMn -= 1
                    if arr[j]==mx: cntMx -= 1
                    j += 1
                ans += j
            return ans
        ans = 0
        l = 0
        for r,x in enumerate(nums + [maxK+1]):
            if x<minK or x>maxK: 
                if l<r: ans += f(nums[l:r], minK, maxK)
                l = r+1
        return ans
        
sol = Solution()
result = [
    sol.countSubarrays(nums = [1,1,1,1], minK = 1, maxK = 1),
    sol.countSubarrays(nums = [1,3,5,2,7,5], minK = 1, maxK = 5),
]
for r in result:
    print(r)
