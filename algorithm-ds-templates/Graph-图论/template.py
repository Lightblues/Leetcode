from easonsi import utils
from easonsi.util.leetcode import *


""" 
== Floyd 弗洛伊德算法
wiki [Floyd](https://zh.wikipedia.org/zh-cn/Floyd-Warshall%E7%AE%97%E6%B3%95)

"""

class Template:
    
    
    def floyd(n, edges):
        """ Floyd 弗洛伊德算法 """
        d = [[inf] * n for _ in range(n)]
        for i in range(n):
            d[i][i] = 0
        for u, v in edges:
            d[u][v] = d[v][u] = 1
        # 复杂度 O(n^3)
        for k in range(n):      # 中间点
            for i in range(n):
                for j in range(n):
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j])