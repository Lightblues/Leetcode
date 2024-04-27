""" 
从n个笔记中选择k个构建合集, 分数为 sum(star) * min(comments), 要求最大分数
限制: n,a,b 1e5
思路1: 针对comments从大到小排序, 维护当前分数最大和. 

4 2
1 2 3 4
3 4 2 1
# 10
"""
import heapq
n,k = map(int, input().split())
stars = list(map(int, input().split()))
comments = list(map(int, input().split()))
notes = list(zip(stars, comments))
notes.sort(key=lambda x: -x[1])

q = [i[0] for i in notes[:k]]
heapq.heapify(q)
mn_comments = notes[k-1][1]
s = sum(q)
ans = mn_comments * s
for i in range(k,n):
    star,c = notes[i]
    mn_comments = c
    s_out = heapq.heappushpop(q, star)
    s += star - s_out
    ans = max(ans, s * mn_comments)
print(ans)
