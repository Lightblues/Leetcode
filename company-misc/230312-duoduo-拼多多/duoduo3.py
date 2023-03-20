""" 
团建: 有三个活动ABC, 分别有人数限制和每个人的费用; 给定每个人的意向 (可以是多个), 问是否可以安排, 若能, 计算最小费用; 若不能, 最多安排的人数
限制: 人数 100
思路0: #贪心, 从费用最小的开始安排起 想来应该是错的
思路1: 大 #模拟 #分类
    何时是合法的? 先去除只有一个偏好的人. 偏好为ABC的人也可以去除. 
        假设人数分别为 ab,bc,ac 则在剩余牌的数量满足 A+B+C < ab+bc+ac+abc; 并且 A+B < ab (加上另外两个) 的条件下可行
    然后怎么样分配? 想不出来, 直接暴力尝试在ab中选择 [0...ab] 个人到A, 剩下的就可以算出来了, 选择代码
    具体见代码
"""

from collections import Counter
n = int(input())
persons = Counter()
for _ in range(n):
    persons[input().strip()] += 1
# remap, 保证 ABC的cost是递增的
events = []
for e in "ABC":
    limit,cost = map(int, input().split())
    events.append([limit,cost,e])
events.sort(key=lambda x: x[1])
eventMap = dict(zip("ABC", [e[2] for e in events]))
def remap(s):
    return "".join(eventMap[c] for c in s)
persons = Counter({remap(p):c for p,c in persons.items()})

# 处理单个偏好的人
flag = True     # 标记是否合法
cnt = 0
cost = 0
for i,e in enumerate('ABC'):
    if events[i][0]<persons[e]: flag = False
    cc = min(events[i][0], persons[e])
    cnt += cc
    events[i][0] -= cc
    cost += cc * events[i][1]

A,B,C = [e[0] for e in events]
ab,bc,ac = persons['AB'], persons['BC'], persons['AC']
abc = persons['ABC']

def checkValid():
    """ 判断是否合法 """
    if A+B+C < ab+bc+ac+abc: return False
    if A+B < ab: return False
    if A+C < ac: return False
    if B+C < bc: return False
    return True

def maxValid():
    mxValid = 0
    for ab_a in range(min(ab,A)+1):
        ab_b = min(ab-ab_a, B)
        ac_a = min(ac, A-ab_a)
        bc_b = min(bc, B-ab_b)
        bc_c = min(bc-bc_b, C)
        ac_c = min(ac, C-bc_c)
        a = ab_a+ac_a
        b = ab_b+bc_b
        c = ac_c+bc_c
        cnt = a+b+c
        remains = abc
        for i,j in enumerate([a,b,c]):
            ava = events[i][0]-j
            cc = min(ava, remains)
            cnt += cc
            remains -= cc
        mxValid = max(mxValid, cnt)
    return mxValid

def minCost():
    mnCost = float('inf')
    for ab_a in range(min(ab, A)+1):
        ab_b = ab - ab_a
        if ab_b > B: continue
        ac_a = min(ac, A-ab_a)
        ac_c = ac - ac_a
        bc_b = min(bc, B-ab_b)
        bc_c = bc - bc_b
        if ac_c+bc_c > C: continue

        a = ab_a+ac_a
        b = ab_b+bc_b
        c = ac_c+bc_c
        cost = a*events[0][1]+b*events[1][1]+c*events[2][1]
        remains = abc
        for i,j in enumerate([a,b,c]):
            ava = events[i][0]-j
            cc = min(ava, remains)
            cost += cc * events[i][1]
            remains -= cc
        mnCost = min(mnCost, cost)
    return mnCost

if flag and checkValid(): 
    print("YES")
    cost += minCost()
    print(cost)
else:
    print('NO')
    cnt += maxValid()
    print(cnt)



