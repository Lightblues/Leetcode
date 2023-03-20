""" 要求构造一个长n的数组, 满足下面的条件
元素 [-3,3]; 相邻元素符号相反, 不能只和为0; 所有元素只和为0
限制: n 1e5

[1,-2,3,-2] 可以构成长度为4的循环节
    [1,-3,1,-2,3] 处理 %4=1 的情况 (最后5个)
    [1,-2,3,-1,2,-3] 处理 %4=2 的情况 (最后6个)
    [1,-2,1] 处理 %4=3 的情况
 """

n = int(input())

base = [1,-2,3,-2]
def f(x):
    if x==2: return []
    a,b = divmod(x,4)
    if b==0: return base * a
    elif b==1: return base * (a-1) + [1,-3,1,-2,3]
    elif b==2: return base * (a-1) + [1,-2,3,-1,2,-3]
    elif b==3: return base * a + [1,-2,1]

res = f(n)
if res:
    print(*res)
else: print("No Answer")

