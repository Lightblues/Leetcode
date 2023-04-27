""" 检查是否可以拿到奖学金. 1] 所有成绩不低于60; 
T 10; n 1e3; 

"""
T = int(input())
def f():
    n,X = map(int, input().strip().split())
    A = list(map(int, input().strip().split()))
    B = list(map(int, input().strip().split()))
    if min(B) < 60: return False
    avg = sum(a*b for a,b in zip(A,B)) / sum(A)
    return avg>=X
for _ in range(T):
    ret = f()
    print('Yes' if ret else 'No')