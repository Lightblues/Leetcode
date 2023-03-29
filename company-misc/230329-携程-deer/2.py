""" 构造一个排列
对于位置i的元素x, 若其为左侧的最大值; 不相邻
贪心构造: 就是取最后的k个元素放在最前面! 为了避免相邻, 交替放置这些vals即可~
"""
n, k = map(int, input().split())
arr = list(range(1,n+1))
vals, other = arr[-k:], arr[:-k]
ans = []
for i in range(k):
    ans += [vals[i], other[i]]
ans += other[k:]
ans = list(map(str, ans))
print(" ".join(ans))