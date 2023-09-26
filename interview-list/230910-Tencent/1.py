""" 
计算矩阵的谱半径, 题目见md

按照题目所给算法计算即可，不过需要注意的是在更新v的过程中需要及时归一化，否则在矩阵幂次的过程中容易数值溢出(容易分析归一化对最终结果没有影响)
"""

n = int(input())
mat = [None for _ in range(n)]
for i in range(n):
    mat[i] = list(map(float, input().split()))
v = list(map(float, input().split()))

def normalize(v):
    s = sum(v)
    return [i/s for i in v]

EPSILON = 1e-4
pre = 1e5
# 可以先进行归一化, 为了数值稳定性
v = normalize(v)
for _ in range(1000):
    nv = [0]*n
    for i in range(n):
        nv[i] = sum([mat[i][j]*v[j] for j in range(n)])
    if abs(nv[0]/v[0] - pre) < EPSILON:
        break
    pre = nv[0]/v[0]
    # print(pre)
    # XXX: 归一化要放在这里! 
    nv = normalize(nv)
    v = nv

print(f"{pre:.2f}")


