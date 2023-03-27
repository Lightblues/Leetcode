""" 选择题
思路1; #模拟

"""
n = int(input())
pre = input().split()
ans = input().split()

acc = 0
for p,a in zip(pre, ans):
    if p==a: acc += 3
    elif all(i in a for i in p): acc += 1
print(acc)



