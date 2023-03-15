""" Queue using Two Stacks 
思路1: 采样两个栈 s1,s2, 后者「逆序」; 前者作为输入的「缓冲」
    例如, 要求出栈时, 假设 s2 空, 则弹出 s1中所有元素逆序加入s2; 否则直接弹出 s2
"""

# Enter your code here. Read input from STDIN. Print output to STDOUT

s1, s2 = [], []
def enqueue(x):
    s1.append(x)
def dequeue():
    if not s2:
        while s1:
            s2.append(s1.pop())
    return s2.pop()
def front():
    if not s2:
        while s1:
            s2.append(s1.pop())
    return s2[-1]

n = int(input())
for i in range(n):
    cmd = input().strip()
    if ' ' in cmd:
        x = int(cmd.split()[1])
        enqueue(x)
    elif int(cmd)==2:
        dequeue()
    else:
        print(front())
