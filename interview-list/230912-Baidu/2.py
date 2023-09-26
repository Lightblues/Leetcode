""" 
给个人有 (a,b) 两个属性, 定义两个人的「分数差」为两者差的绝对值之和. 
    对于一个固定的L, 要求差值最多为L的两个人必须在一组. 
    问至少分成k组, 最大可能的L是多少. 
    限制: n 500
思路1: 构建图结构 (并查集), 从小到大连边, 直到小于k组. 
    复杂度: 所有边的路上 O(n^2), 需要对边进行排序
"""
n,k = map(int, input().split())
arrA = list(map(int, input().split()))
arrB = list(map(int, input().split()))
edges = []
for i in range(n):
    for j in range(i,n):
        s = abs(arrA[i]-arrA[j]) + abs(arrB[i]-arrB[j])
        edges.append((s,i,j))
edges.sort(key=lambda x: x[0])

fa = list(range(n))
def find(i):
    if fa[i] != i:
        fa[i] = find(fa[i])
    return fa[i]
def union(i,j):
    fi,fj = find(i),find(j)
    if fi<fj: fi,fj = fj,fi
    fa[fi] = fj
ngroups = n

for s,i,j in edges:
    fi,fj = find(i),find(j)
    if fi!=fj:
        ngroups -= 1
        union(fi,fj)
    if ngroups < k: break
print(s-1)
