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
单调栈：
    0496. 下一个更大元素 I（单调栈模板题）
    0503. 下一个更大元素 II
    0456. 132 模式
    0739. 每日温度
    0901. 股票价格跨度
    1124. 表现良好的最长时间段
    1475. 商品折扣后的最终价格


0496. 下一个更大元素 I #easy #题型 #单调栈 
    要求 O(n) 时间内计算数组中每个元素的下一个更大元素
0503. 下一个更大元素 II #medium
    相较于 0496, 这里是一个「循环数组」, 也即需要考虑一个环中, 比当前元素更大的下一个元素值.
    思路: 仅需要「循环遍历」两次即可

== 基本题型
0739. 每日温度 #medium 对于一个温度序列, 计算每天的下一个更高温度出现在几天后
1475. 商品折扣后的最终价格 #easy #medium 对于商品i, 它可以得到满足 prices[j] <= prices[i] 的最小下标 j 的折扣, 求打折后的商品价格
0901. 股票价格跨度 #medium 对于流式的股票数据, 计算当天往回小于等于当天股价的天数

== 多种解法, 细看
0456. 132 模式 #medium #题型 #star 在数组中找 满足 i < j < k 和 nums[i] < nums[k] < nums[j] 的三元组
    官答给出了三种方法, 赞

== 两次遍历
1124. 表现良好的最长时间段 #medium 实际上 #hard #题型 给定一个 0/1序列, 问子序列中, 1的数量严格大于0的序列的最大长度 限制: 1e4
    等价于在 1/-1 数组中, 最长的和为正的子数组
    计算 #前缀和; 问题等价于 「0962. 最大宽度坡」
0962. 最大宽度坡 #medium #题型 #star 对于一个数组, 找到相距最大的 (i,j), 满足 A[i] <= A[j]
    两次遍历!! 先用一个 #单调栈 来记录可能的最大左边界; 反向过程中, 匹配成功就出栈!! (因为这是栈顶元素可以匹配的最大宽度)
    
    
    
Easonsi @2023 """
class Solution:
    """ 0496. 下一个更大元素 I #easy #题型 #单调栈
有一个数组 nums2, 满足所有元素都不同. 再给一组查询 nums1, 其每一个元素都是 nums2 中的元素, 要求返回每一次查询的数字之后的 (下一个) 更大元素的值.
思路1: #单调栈. 
    也即, 需要建立一个index, 记为 nextGreater[i] 表示在nums2的第i位置的元素的下一个更大元素 (位置或者值).
    为建立这里index, 可以从后往前遍历, 构建单调递减栈 (从栈底到栈顶).
[here](https://leetcode.cn/problems/next-greater-element-i/solution/xia-yi-ge-geng-da-yuan-su-i-by-leetcode-bfcoj/)

"""
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        # 单调栈
        s = []
        nextGreater = [None] * len(nums2)   # nextGreater[i] 记录 nums2[i] 的下一个更大元素值
        for i in range(len(nums2)-1, -1, -1):
            num = nums2[i]
            while s and s[-1] < num: s.pop()
            nextGreater[i] = s[-1] if s else -1
            s.append(i)
        num2idx = {num: i for i, num in enumerate(nums2)}
        return [nextGreater[num2idx[num]] for num in nums1]
    
    """ 0503. 下一个更大元素 II #medium
相较于 0496, 这里是一个「循环数组」, 也即需要考虑一个环中, 比当前元素更大的下一个元素值.
例子: [1,2,1] 的结果应该是 [2, -1, 2]
思路1: 还是用 #单调栈, 不过需要循环两次
"""
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        s = []
        ans = [-1] * n
        for i,a in enumerate(nums+nums):
            while s and s[-1][0]<a: # 要找的是严格大的元素
                v, idx = s.pop()
                ans[idx%n] = a
            s.append((a,i))
        return ans
    
    
    """ 0456. 132 模式 #medium #题型 在数组中找 满足 i < j < k 和 nums[i] < nums[k] < nums[j] 的三元组
思路1: 枚举3, 利用 #有序数组, 每次在右侧元素中找到次小值. 
    时间复杂度 O(n logn)
思路2: 枚举1, 利用 #单调栈 判断哪些元素可以作为2
    从右往左遍历, 记录可以作为2的最大值 mx2 (也即已经有了一个更大的3), 若当前枚举的元素 nums[i]<mx2, 根据传递性就满足了条件. 
    如何找到 mx2? 用 #单调栈, 从右往左遍历, 构建单调递减栈, 每次遇到比栈顶元素更大的元素, pop 的时候更新 mx2
    复杂度 O(n)
思路3: 枚举2, 用一系列单调结构的 (a,b) 来记录可能的2的范围. 更直观但也更难
    从左往右考虑, 注意到对于可能作为 13组合的下标对 (i,j), 它们定义了区间 (a,b)
        对于一个新的元素x, 假如它 <a, 并不能直接作为1, 还需要找到匹配的3.
        因此, 我们用一系列的 (a,b) 区间来记录! 注意到, 我们可以保证 a,b 都是严格递减的!!
    如何判断x是否可以作为2? 分别在 a,b 序列上 #二分 搜索!
    复杂度: O(n logn) 似乎不太好? 思路3的优势在于是顺序的 (实际上更直觉), 如果是数据流的话, 上面两个方法都不能用了! 
见 [官答](https://leetcode.cn/problems/132-pattern/solution/132mo-shi-by-leetcode-solution-ye89/)
"""
    def find132pattern(self, nums: List[int]) -> bool:
        # 思路1: 枚举3, 利用 #有序数组, 每次在右侧元素中找到次小值. 
        from sortedcontainers import SortedList
        mn = nums[0]
        sl = SortedList(nums[1:])
        for i in range(1, len(nums)-1):
            num = nums[i]
            sl.remove(num)
            # 要满足 132, 必然要求 num>mn, 否则更新 mn. 
            if num>mn:
                # 找到右侧元素中比num小的最大元素
                idx = sl.bisect_left(num)-1
                if idx>=0 and sl[idx]>mn: return True
            else:
                mn = num
        return False
    def find132pattern(self, nums: List[int]) -> bool:
        # 思路2: 枚举1, 利用 #单调栈 判断哪些元素可以作为2
        n = len(nums)
        mx2 = -inf
        s = [nums[-1]]
        for i in range(n-2,-1,-1):
            num = nums[i]
            if num<mx2: return True
            while s and s[-1]<num:
                mx2 = max(s.pop(),mx2)
            s.append(num)
        return False
    def find132pattern(self, nums: List[int]) -> bool:
        # 思路3: 枚举2, 用一系列单调结构的 (a,b) 来记录可能的2的范围. 更直观但也更难
        n = len(nums)
        a = [nums[0]]   # 区间下界, 单调递减
        b = [nums[0]]   # 区间上界, 单调递减
        def check(x):
            """ 检查能否在 a,b 所定义的区间中, 找到包含x的 """
            # 在a中从左到右找到第一个比x小的元素
            idxa = bisect_right(a, -x, key=lambda x:-x)
            if idxa==len(a): return False
            # 在b中从右到左找到第一个比x大的元素
            idxb = bisect_left(b, -x, key=lambda x:-x)
            if idxb==0: return False
            if idxb<len(b) and b[idxb]<=x: idxb-=1
            if idxa<=idxb: 
                return True
            return False
        for i in range(1,n):
            x = nums[i]
            # 检查是否可以作为2
            if check(x): return True
            # 更新区间
            if x>b[-1]: # 作为3
                mn = a.pop(); b.pop()
                while b and x>=b[-1]: 
                    a.pop(); b.pop()
                a.append(mn); b.append(x)
            elif x<a[-1]:   # 作为1
                a.append(x); b.append(x)    # 暂时没有对应的3, 直接填充x
        return False

    """ 0739. 每日温度 #medium 对于一个温度序列, 计算每天的下一个更高温度出现在几天后 """
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        ans = [0]*n
        q = []
        for i,t in enumerate(temperatures):
            while q and q[-1][0]<t:
                _,j = q.pop()
                ans[j] = i-j
            q.append((t,i))
        return ans

    """ 1475. 商品折扣后的最终价格 #easy #medium 对于商品i, 它可以得到满足 prices[j] <= prices[i] 的最小下标 j 的折扣, 求打折后的商品价格
思路1: 从右往左遍历; 维护 #单调递增栈.
"""
    def finalPrices(self, prices: List[int]) -> List[int]:
        n = len(prices)
        ans = prices[:]
        q = []  # 单调递增栈
        for i in range(n-1,-1,-1):
            p = prices[i]
            while q and q[-1]>p:
                q.pop()
            if q: ans[i] -= q[-1]
            q.append(p)
        return ans

    """ 1124. 表现良好的最长时间段 #medium 实际上 #hard #题型 给定一个 0/1序列, 问子序列中, 1的数量严格大于0的序列的最大长度 限制: 1e4
思路1: #转化, 利用 #前缀和 转为 #单调栈 求解
    问题等价于在 1/-1 数组中, 最长的和为正的子数组. 
    再转化: 计算 #前缀和, 这样对于位置j, 它能匹配的就是最左的满足 acc[i]+1<=acc[j] 的位置 i
    要求最大宽度, 问题等价于 「0962. 最大宽度坡」
        要点是两次遍历, 利用单调递减栈维护可能的最大左边界
    复杂度: O(n)
"""
    def longestWPI(self, hours: List[int]) -> int:
        # 转换问题
        hours = [1 if h>8 else -1 for h in hours]
        acc = list(accumulate(hours, initial=0))
        # 下面类似 0962. 最大宽度坡
        n = len(acc)
        q = []
        for i,x in enumerate(acc):
            if not q or q[-1][0]>x: q.append((x,i))
        # 
        ans = 0
        for j in range(n-1,-1,-1):
            while q and q[-1][0]+1<=acc[j]:
                ans = max(ans, j-q.pop()[1])
        return ans

    """ 0962. 最大宽度坡 #medium #题型 #star 对于一个数组, 找到相距最大的 (i,j), 满足 A[i] <= A[j] 限制: n 5e4 
思路1: 很巧妙的两次遍历!! 先用一个 #单调栈 来记录可能的最大左边界; 反向过程中, 匹配成功就出栈!! (因为这是栈顶元素可以匹配的最大宽度)
    第一遍, 先得到从位置0开始的单调递减栈; 
    第二遍, 从右往左, 尝试和栈顶元素匹配; 若匹配成功, 可以将栈顶元素出栈!! (因为这是栈顶元素可以匹配的最大宽度)
    复杂度: O(n)
"""
    def maxWidthRamp(self, nums: List[int]) -> int:
        n = len(nums)
        q = []  # 记录单调递减栈的元素 idx
        for i in range(n):
            if not q or nums[i]<nums[q[-1]]:
                q.append(i)
        ans = 0
        for i in range(n-1,-1,-1):
            while q and nums[i]>=nums[q[-1]]:
                ans = max(ans, i-q.pop())
        return ans




""" 0901. 股票价格跨度 #medium 对于流式的股票数据, 计算当天往回小于等于当天股价的天数 """
class StockSpanner:
    def __init__(self):
        self.q = [] # (price, day)
        self.day = 0

    def next(self, price: int) -> int:
        self.day += 1
        while self.q and self.q[-1][0]<=price:
            self.q.pop()
        ans = self.day-self.q[-1][1] if self.q else self.day
        self.q.append((price, self.day))
        return ans


sol = Solution()
result = [
    # sol.nextGreaterElement(nums1 = [4,1,2], nums2 = [1,3,4,2]),
    # sol.nextGreaterElements(nums = [1,2,1]),
    # sol.nextGreaterElements(nums = [1,2,3,4,3]),
    
    # sol.find132pattern(nums = [3,1,4,2]),
    # sol.find132pattern([1,2,3]),
    # sol.find132pattern([-1,3,2,0]),
    # sol.find132pattern([1,0,1,-4,-3]),
    
    # sol.maxWidthRamp([6,0,8,2,1,5]),
    # sol.maxWidthRamp([9,8,1,0,1,9,4,0,4,1]),
    sol.longestWPI(hours = [9,9,6,0,6,6,9]),
    sol.longestWPI([6,6,6]),
    
]
for r in result:
    print(r)
