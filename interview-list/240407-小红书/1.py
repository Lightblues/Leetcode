""" 
有n个粉丝, (x,y) 的权重分别为 (1,2), 根据 (score, y, -id) 的顺序逆序排列, 返回前k个

4 2
1 2
2 1
3 0
1 3
# 1 4

"""
n,k = map(int, input().split())
fans = []
for i in range(1,n+1):
    x,y = map(int, input().split())
    s = x + 2*y
    fans.append((s,y,-i))
fans.sort(reverse=True)
ans = [-i[2] for i in fans[:k]]
ans.sort()
print(" ".join(map(str, ans)))