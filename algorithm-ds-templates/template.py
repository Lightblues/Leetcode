from easonsi import utils
from easonsi.util.leetcode import *
from functools import lru_cache as cache
import pytest
""" 
run test: pytest template.py
"""


""" 
== Floyd 弗洛伊德算法
wiki [Floyd](https://zh.wikipedia.org/zh-cn/Floyd-Warshall%E7%AE%97%E6%B3%95)

"""

""" 
w[i]: 第i个物品的体积
v[i]: 第i个物品的价值
返回: 不超过capacity的前提下, 能够获得的最大价值
"""
def zero_one_knapsack(capacity, w, v):
    n = len(w)
    @cache
    def dfs(i,c):
        if i<0: return 0
        if c<w[i]: return dfs(i-1,c)
        return max(dfs(i-1,c), dfs(i-1,c-w[i])+v[i])
    return dfs(n-1, capacity)


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


""" BIT: Binary Indexed Tree 树状数组
"""
# 树状数组模板（维护前缀最大值）
class BIT:
    def __init__(self, n):
        self.tree = [-inf] * n

    def update(self, i: int, val: int) -> None:
        while i < len(self.tree):
            self.tree[i] = max(self.tree[i], val)
            i += i & -i

    def pre_max(self, i: int) -> int:
        mx = -inf
        while i > 0:
            mx = max(mx, self.tree[i])
            i &= i - 1
        return mx

def test_BIT():
    bit = BIT(10)       # 注意：树状数组的下标从 1 开始
    bit.update(1, 10)
    bit.update(2, 20)
    bit.update(3, 30)
    assert bit.pre_max(1) == 10
    assert bit.pre_max(2) == 20
    assert bit.pre_max(3) == 30
    bit.update(1, 40)
    assert bit.pre_max(1) == 40
    assert bit.pre_max(2) == 40
    assert bit.pre_max(3) == 40
    assert bit.pre_max(9) == 40


""" SegTree: Segment Tree 分段树/线段树
"""
class SegTree:
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        self.tree = [0] * (2 * self.n)

        # 构建分段树
        self._build_tree(0, 0, self.n - 1)

    def _build_tree(self, node, start, end):
        if start == end:
            # 叶节点，存储原始数组元素值
            self.tree[node] = self.arr[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2

            # 递归构建左右子树
            self._build_tree(left_child, start, mid)
            self._build_tree(right_child, mid + 1, end)

            # 合并左右子树的值
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def query(self, query_start, query_end):
        # 查询区间和
        return self._query(0, 0, self.n - 1, query_start, query_end)

    def _query(self, node, start, end, query_start, query_end):
        if query_end < start or query_start > end:
            # 查询区间与当前区间没有交集
            return 0
        elif query_start <= start and query_end >= end:
            # 查询区间包含当前区间
            return self.tree[node]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2

            # 递归查询左右子树
            left_sum = self._query(left_child, start, mid, query_start, query_end)
            right_sum = self._query(right_child, mid + 1, end, query_start, query_end)

            # 返回左右子树查询结果的合并
            return left_sum + right_sum

    def update(self, index, new_value):
        # 更新指定索引处的值
        self._update(0, 0, self.n - 1, index, new_value)

    def _update(self, node, start, end, index, new_value):
        if start == end == index:
            # 到达叶节点，更新值
            self.tree[node] = new_value
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2

            # 根据索引位置更新左右子树
            if index <= mid:
                self._update(left_child, start, mid, index, new_value)
            else:
                self._update(right_child, mid + 1, end, index, new_value)

            # 更新当前节点的值
            self.tree[node] = self.tree[left_child] + self.tree[right_child]


# 示例用法
arr = [1, 3, 5, 7, 9, 11]
seg_tree = SegTree(arr)

# 查询区间和
query_start = 1
query_end = 4
result = seg_tree.query(query_start, query_end)
print(f"Sum in range [{query_start}, {query_end}]: {result}")

# 更新指定索引处的值
index_to_update = 2
new_value = 8
seg_tree.update(index_to_update, new_value)

# 再次查询更新后的区间和
result_after_update = seg_tree.query(query_start, query_end)
print(f"Sum in range [{query_start}, {query_end}] after update: {result_after_update}")
