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
https://leetcode.cn/contest/weekly-contest-153
T3是「子数组最大和」的变种. T4是经典的DP, 用了暴力的递归方式. 

@2022 """
class Solution:
    """ 1184. 公交站间的距离 """
    
    """ 1185. 一周中的第几天 #题型 #日期 给定一个 (y,m,d), 返回是周几. 限制: 日期 1971~2100
关联: 1360. 日期之间隔几天 #easy #题型
"""
    def dayOfTheWeek(self, day: int, month: int, year: int) -> str:
        days = [31,28,31,30,31,30,31,31,30,31,30,31]
        def leap_year(year):
            return (year % 400 == 0) or (year % 100 != 0 and year % 4 == 0)
        def getDays(year,month,day):
            # 返回从 1971 开始第几天
            acc = 0
            for y in range(1971,year):
                acc += 366 if leap_year(y) else 365
            for m in range(month-1):
                acc += days[m]
            if month > 2 and leap_year(year):
                acc += 1
            acc += day
            return acc
        weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        # print(getDays(1971,1,1))
        # 1970 年 1212 月 3131 日是星期四
        bias = 4
        idx = getDays(year,month,day)
        return weekdays[(idx+bias)%7]
    def dayOfTheWeek(self, day: int, month: int, year: int) -> str:
        import datetime
        idx = datetime.datetime(year, month, day).weekday() # 0~6 从Monday开始
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return weekdays[idx]
    
    """ 1186. 删除一次得到子数组最大和 #medium #题型 相较于「子数组最大和」, 可以删除所选子数组中的一个元素. 要求 **所选子数组不能为空**! 限制: n 1e5
相较于经典的「子数组最大和」, 区别在于可删除一个. 考虑dp的时候记录两个数字 a,b 分别表示在不删除/删除一个条件下的最大和
递推: 对于当前元素 x
    对于a, 有 a = max(a+x, x). 注意由于不能为空, 第二项不是0
    对于b, 有 b = max{ a, b+x }. 
    边界: 注意b初始化为 max(arr[0], arr[1])
"""
    def maximumSum(self, arr: List[int]) -> int:
        n = len(arr)
        if n==1: return arr[0]
        a = max(arr[1], arr[0]+arr[1])
        b = max(arr[0], arr[1])
        ans = max(a,b)
        for i in range(2, n):
            a,b = max(a+arr[i], arr[i]), max(a, b+arr[i])
            ans = max(ans,a,b)
        return ans
    
    """ 1187. 使数组严格递增 #hard #题型 给定两个数组, 每次操作可以赋值 arr1[i] = arr2[j]. 问要使得 arr1 严格递增所需的最少步数, 不行的话返回-1. 限制: n 2e3. 
思路1: #DP
    记 `f[i,x]` 表示在x的操作步骤内, arr[:i] 可以得到最小末尾. 
    递推: 是一组数字的min操作: 
        少一个操作: f[i,x-1] (保证 f[i,0...x-1] 是递减的)
        针对arr1当前元素: 若 arr1[i] > f[i-1,x], 则可取 arr1[i]
        从arr2中选择: 在 arr2 中选择比 f[i-1,x-1]  大的最小元素
    复杂度: O(n^2)
"""
    def makeArrayIncreasing(self, arr1: List[int], arr2: List[int]) -> int:
        arr2.sort()
        n = k = len(arr1)
        f = [[float('inf')] * (n+1) for _ in range(n)]
        # 边界: 一个元素
        f[0][0] = arr1[0]
        for i in range(1,n):
            f[0][i] = min(arr1[0], arr2[0])
        # DP
        for i in range(1, n):
            if f[i-1][0]!=inf and arr1[i]>arr1[i-1]: 
                f[i][0] = arr1[i]
            for x in range(1,n+1):
                mn = f[i][x-1]
                if arr1[i] > f[i-1][x]: mn = min(mn, arr1[i])
                idx = bisect_right(arr2, f[i-1][x-1])
                if idx<len(arr2): mn = min(mn, arr2[idx])
                f[i][x] = mn
        for x,v in enumerate(f[-1]):
            if v!=inf: return x
        return -1
    
sol = Solution()
result = [
    # sol.makeArrayIncreasing(arr1 = [1,5,3,6,7], arr2 = [1,3,2,4]),
    # sol.makeArrayIncreasing(arr1 = [1,5,3,6,7], arr2 = [4,3,1]),
    # sol.makeArrayIncreasing(arr1 = [1,5,3,6,7], arr2 = [1,6,3,3]),
    # sol.makeArrayIncreasing([5,16,19,2,1,12,7,14,5,16], [6,17,4,3,6,13,4,3,18,17,16,7,14,1,16]), 
    # sol.maximumSum(arr = [1,-2,0,3]),
    # sol.maximumSum([-1,-1,-1]),
    # sol.maximumSum([2,1,-2,-5,-2]),
    sol.dayOfTheWeek(day = 31, month = 8, year = 2019),
]
for r in result:
    print(r)
