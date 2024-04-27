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
https://leetcode.cn/contest/weekly-contest-386
https://leetcode.cn/circle/discuss/aznKZM/
难度挺大

Easonsi @2023 """
class Solution:
    """ 3046. 分割数组 """
    def isPossibleToSplit(self, nums: List[int]) -> bool:
        return max(Counter(nums).values()) <= 2
    
    """ 3047. 求交集区域内的最大正方形面积 #medium 有一组矩形, 求交叉部分可以放入的最大正方形
限制: N 1e3
思路1: 两两枚举
    复杂度: O(n^2)
可以不分类讨论, 因为若有交集的话, 
    左下角横坐标：两个矩形左下角横坐标的最大值。
    左下角纵坐标：两个矩形左下角纵坐标的最大值。
    ... 然后看这两个点是否合法即可! 
[ling](https://leetcode.cn/problems/find-the-largest-area-of-square-inside-two-rectangles/solutions/2653554/jian-ji-xie-fa-wu-xu-fen-lei-tao-lun-pyt-b7yq/)
    """
    def largestSquareArea(self, bottomLeft: List[List[int]], topRight: List[List[int]]) -> int:
        n = len(bottomLeft)
        def f(x1,x2,x3,x4):
            if x4 < x2:
                x1,x2,x3,x4 = x3,x4,x1,x2
            if x3>x2: return 0
            elif x1<=x3<=x2: return x2-x3
            else: return x2-x1

        mx = 0
        for i,j in combinations(range(n),2):
            x1,y1 = bottomLeft[i]; x2,y2 = topRight[i]
            x3,y3 = bottomLeft[j]; x4,y4 = topRight[j]
            a = f(x1,x2,x3,x4)
            b = f(y1,y2,y3,y4)
            mx = max(min(a,b),mx)
        return mx**2

    
    """ 3048. 标记所有下标的最早秒数 I #medium 有一个数组nums, 另外有一个长m的数组 changeIndices, 
对于时间 s = 1...m, 每次可以执行一个操作: 1] 将nums的某一位置-1; 2] nums[changeIndices[s]]=0 的话, 可以mark这一位置. 问最早可以mark左右位置的时间, 不行的话返回 -1
限制: n,m 2e3
思路1: #二分 + 从后往前尝试
    注意, 由于不知道应该先mark哪个, 无法直接找到最优解
    在给定限制的情况下 c, 可以先先从右往左看 changeIndices[:c], 对于每个index找到最晚一次位置, 然后看在此之前是否可以满足消除条件! 
    消除条件是, 假设只 s=[i1,i2,...ii] 个坐标要消除, 则 c >= ii + sum(nums[ss] in s)
    """
    def earliestSecondToMarkIndices(self, nums: List[int], changeIndices: List[int]) -> int:
        n,m = len(nums), len(changeIndices)

    
sol = Solution()
result = [
    sol.largestSquareArea(bottomLeft = [[1,1],[2,2],[3,1]], topRight = [[3,3],[4,4],[6,6]]),
    sol.largestSquareArea(bottomLeft = [[1,1],[2,2],[1,2]], topRight = [[3,3],[4,4],[3,4]]),
    sol.largestSquareArea([[2,2],[3,1]], [[5,5],[5,5]]),
]
for r in result:
    print(r)
