""" 
对于一系列 (i,score), 计算分差最小的那些员工对, 输出

限制: n 1e6
"""
n = int(input())
persons = []
for _ in range(n):
    i,score = map(int, input().split())
    persons.append((i,score))
persons.sort(key=lambda x:x[1])
mn = float('inf')
ans = []
for i in range(1,n):
    diff = persons[i][1] - persons[i-1][1]
    if diff < mn:
        mn = diff
        ans = [sorted([persons[i][0], persons[i-1][0]])]
    elif diff == mn:
        ans.append(sorted([persons[i][0], persons[i-1][0]]))
for i,j in sorted(ans):
    print(f"{i} {j}")