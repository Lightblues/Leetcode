""" B. Almost Ternary Matrix
给定两个整数 m,n <=50, 要求构造一个该大小的 0/1 grid, 使得其中的每个元素, 相邻点中与其值不同的数量都是2个.
限制: m,n 都是偶数, 保证了一定有解.
例子: 
1 0 0 1 1 0 0 1
0 1 1 0 0 1 1 0
0 1 1 0 0 1 1 0
1 0 0 1 1 0 0 1
思路1: #构造
    人工尝试几种特殊情况. 容易发现, 可以控制每一行的基本元为 `1001` or `0101` 然后每隔两行交替填入.
https://codeforces.com/contest/1699/problem/B
"""
t = int(input())
pattern1 = [1,0,0,1] * 20
pattern2 = [0,1,1,0] * 20
def f(m,n):
    for i in range(m):
        l = pattern1[:n] if i%4 in [0,3] else pattern2[:n]
        print(" ".join(map(str, l)))
for _ in range(t):
    m,n = map(int, input().split())
    f(m,n)
