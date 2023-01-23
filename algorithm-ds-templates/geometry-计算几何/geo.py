from easonsi import utils
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
https://oi-wiki.org/geometry/

1515. 服务中心的最佳位置 #hard #题型 #最优化 求 [几何中位数](https://en.wikipedia.org/wiki/Geometric_median)

1453. 圆形靶内的最大飞镖数量 #hard #题型 #几何 二维坐标上有一组点, 飞镖可以覆盖半径为r的区域, 问能否覆盖的最大点数. 
    限制: n 100. r 5000. 二维平面 [+/- 1e4]
    思路1: 这里的点数量较小, 可以考虑 #暴力 枚举.
    提示: 我们肯定可以在两个图上点的半径为r的交点上找到答案. (考虑移动圆找到边界)

@2022 """
class Solution:
    """  """
    
    
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
