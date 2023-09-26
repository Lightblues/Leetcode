#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
# 
# @param x double浮点型二维数组 
# @param y double浮点型一维数组 
# @return int整型一维数组
#

""" 
对于 x,y 做线性回归, 以 mse 衡量好坏. 给定一组变量, 挑选两个对y进行回归, 要求mse最小. 

[[70, 95, 34, 46, 10], [65, 88, 45, 24, 32], [87, 91, 23, 35, 10], [67, 101,34, 55, 15]],[50,51,78,88]
# [0,1]

"""
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
from typing import List
class Solution:
    def fit(self , x: List[List[float]], y: List[float]) -> List[int]:
        # write code here
        x = np.array(x)
        n = len(x[0])
        mn = np.inf; ans = None
        for i in range(n):
            for j in range(i+1, n):
                x_ = x[:, [i, j]]
                model = LinearRegression()
                model.fit(x_, y)
                mse = mean_squared_error(y, model.predict(x_))
                # print(i, j, mse)
                if mse<mn:
                    mn = mse
                    ans = [i, j]
        return ans


x = [[70, 95, 34, 46, 10], [65, 88, 45, 24, 32], [87, 91, 23, 35, 10], [67, 101,34, 55, 15]]
y = [50,51,78,88]
sol = Solution()
sol.fit(x,y)