r""" 
使用numpy计算一组数据的皮尔逊相关系数

对于两个变量 ( X ) 和 ( Y )，皮尔逊相关系数计算公式为：
r = \frac{\sum_{i=1}^{N} (X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum_{i=1}^{N} (X_i - \bar{X})^2} \sqrt{\sum_{i=1}^{N} (Y_i - \bar{Y})^2}}
其中，( \bar{X}) 和 ( \bar{Y} ) 分别是 ( X ) 和  Y  的均值。
如果特征与目标值的相关系数为 NaN，则认为相关系数为 0。

5 3
1.0 2.0 3.0 10.0
2.0 3.0 4.0 12.0
3.0 4.0 5.0 14.0
4.0 5.0 6.0 16.0
5.0 6.0 7.0 18.0
> 
0 1.0000
1 1.0000
2 1.0000
"""

import sys
import numpy as np

n,m = map(int, sys.stdin.readline().split())
a = np.array([list(map(float, sys.stdin.readline().split())) for _ in range(n)])
k = int(sys.stdin.readline())

corrs = []
for i in range(m):
    x, y = a[:,i], a[:,m]
    corrs.append((np.corrcoef(x,y)[0][1], -i))
corrs.sort(reverse=True)

# 取前k个? 下面不重要
corr_k = None
for x,i in corrs:
    i = int(-i)
    if i == k: corr_k = k
    if i>k and x != corr_k: break
    print(f"{i} {x:.4f}")
