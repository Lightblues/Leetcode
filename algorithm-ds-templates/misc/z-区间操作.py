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



Easonsi @2023 """
class Solution:
    """ 0056. 合并区间 #medium 给定一组数组, 合并其中重叠的部分
思路1: 先按照左端点排序. 然后顺序遍历
    正确性: 注意, 这样不可能出现跨越重叠的情况
"""
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda x: x[0])
        merged = []
        for interval in intervals:
            # 如果列表为空，或者当前区间与上一区间不重合，直接添加
            if not merged or merged[-1][1] < interval[0]:
                merged.append(interval)
            else:
                # 否则的话，我们就可以与上一区间进行合并
                merged[-1][1] = max(merged[-1][1], interval[1])
        return merged
    
    """ 0057. 插入区间 #medium #细节 给定一组不重叠的有序数组, 要求再插入一个区间之后, 合并 (0056. 合并区间)
思路1: 遍历模拟. 
    但需要注意 #细节. 需要标记代插入的数组是否已经插入
"""
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        ans = []
        merged = newInterval[:]; placed = False
        for s,e in intervals:
            if e<newInterval[0]: ans.append([s,e])
            elif s>newInterval[1]:
                if placed==False:
                    ans.append(merged)
                    placed = True
                ans.append([s,e])
            else:
                merged = [min(merged[0],s), max(merged[1],e)]
        if placed==False: ans.append(merged)
        return ans
    
    

    
sol = Solution()
result = [
    sol.insert(intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]),
    sol.insert([[1,5]],[2,3]),
    sol.insert([[2,5],[6,7],[8,9]],[0,1]),
]
for r in result:
    print(r)
