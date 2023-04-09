from easonsi import utils
from easonsi.util.leetcode import *

""" 
https://oi-wiki.org/graph/shortest-path/

BFS: 等权图上复杂度 O(m+n)

Floyd 算法
    求任意两个结点之间的最短路
    复杂度比较高，但是常数小，容易实现。(三个for)
Bellman-Ford 算法
Dijkstra 算法
    非负权图 上单源最短路径
    复杂度: 根据使用 二叉堆/优先队列 的不同, 有不同的时间复杂度, 
        采用优先队列 PriorityQueue 的复杂度为 O(m logm)

"""


