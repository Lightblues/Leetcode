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
https://leetcode.cn/contest/weekly-contest-182

T2有点搞, 官答的思路还是很清楚; T4过分困难了点, 之前灵神的数位DP有讲过...
@2022 """
class Solution:
    """ 1394. 找出数组中的幸运数 """
    
    """ 1395. 统计作战单位数 #medium 给定一个数组, 每个元素的值互不相同. 要求找到 a<b<c 或者 a>b>c 的三元组数量. 限制: n 1000.
思路1: 枚举 mod. 复杂度 O(n^2)
思路2: #离散化 #树状数组
    如何在遍历过程中, 快速得到「小于x的数的数量」? 首先, 我们将数组元素 #离散化 到1...n 范围内.
    在从左往右遍历过程中, 记录出现过程的元素 (相应位置设置为1), 利用 #树状数组, 我们就可以在 O(log n) 时间内计算前缀和, 即得到答案.
[官答](https://leetcode.cn/problems/count-number-of-teams/solution/tong-ji-zuo-zhan-dan-wei-shu-by-leetcode-solution/)
"""
    def numTeams(self, rating: List[int]) -> int:
        n = len(rating)
        ret = 0
        for mid  in range(1, n-1):
            m = rating[mid]
            # 左侧
            cntL, cntG = 0, 0
            for i in range(mid):
                if rating[i] < m: cntL += 1
                else: cntG += 1
            # 右侧
            cntLL, cntGG = 0, 0
            for i in range(mid+1, n):
                if rating[i] < m: cntLL += 1
                else: cntGG += 1
            # 左右匹配
            ret += cntL * cntGG + cntG * cntLL
        return ret
    
    """ 1397. 找到所有好字符串 #hard 见 [digit+数位DP] """
    
""" 1396. 设计地铁系统
"""
class UndergroundSystem:

    def __init__(self):
        self.checkInTime = {}
        self.avgTime = defaultdict(lambda: [0, 0]) # [sum, cnt]

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        # 用户入站
        self.checkInTime[id] = (stationName, t)

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        inStation, inTime = self.checkInTime[id]
        self.avgTime[(inStation, stationName)][0] += t - inTime
        self.avgTime[(inStation, stationName)][1] += 1

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        return self.avgTime[(startStation, endStation)][0] / self.avgTime[(startStation, endStation)][1]
    
    
    
sol = Solution()
result = [
    # sol.numTeams(rating = [2,5,3,4,1]),
    # sol.numTeams(rating = [1,2,3,4]),
    testClass("""["UndergroundSystem","checkIn","checkIn","checkIn","checkOut","checkOut","checkOut","getAverageTime","getAverageTime","checkIn","getAverageTime","checkOut","getAverageTime"]
[[],[45,"Leyton",3],[32,"Paradise",8],[27,"Leyton",10],[45,"Waterloo",15],[27,"Waterloo",20],[32,"Cambridge",22],["Paradise","Cambridge"],["Leyton","Waterloo"],[10,"Leyton",24],["Leyton","Waterloo"],[10,"Waterloo",38],["Leyton","Waterloo"]]"""),
]
for r in result:
    print(r)
