#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
# 计算收益率序列的平均日度收益率(mean)，收益率标准差(std),夏普比率(mean/std),最大回撤(dd),卡玛比率(mean/dd)，结果保留2位小数点,并以list of string格式输出。
# @param arr double浮点型一维数组 
# @return string字符串一维数组
#
""" 对于给定数据, 分别计算 平均日度收益率(mean)，收益率标准差(std),夏普比率(mean/std),最大回撤(dd),卡玛比率(mean/dd)
shrp = mean/std
dd = max(0, sum_{i,j}{-arr[i:j]})
kamma = mean/dd

- 核心是计算DD! 采用DP

[ 0.8, -1.51, -0.46, -0.24, -0.31, -1.23, -0.17,  0.95, -1.52,  1.17]
# ["-0.25","0.94","-0.27","4.49","-0.06"]

 """
import numpy as np
from typing import List
class Solution:
    def calc_stats(self , arr: List[float]) -> List[str]:
        # write code here
        mean_ = np.mean(arr)
        std_ = np.std(arr)
        dd = 0
        tmp = 0
        for x in arr:
            dd = min(tmp+x, dd)
            tmp = min(tmp+x,0)
        dd = max(0, -dd)
        stats = [mean_, std_, mean_/std_, dd, mean_/dd]
        stats = [str(round(x,2)) for x in stats]
        return stats


