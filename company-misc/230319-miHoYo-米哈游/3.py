
""" 对于形如下面的字符串, 对于每一个query(l,r), 判断在 s[l,r] 范围内的逗号, 分号数量. 限制: q 1e4; l,r 1e12
1,2,3;4,5,6;7,8,9;10,11,12;...;97,98,99;100,101,102;

1~9: 3/6 编码; 共 9*2 = 18 个字符
    符号出现的位置: 2,4,6; 
10~99: 3/9 编码; 共 90*3 = 270 个字符
    符号出现的位置: 3,6,9; (相对)
100~999: 3/12 编码; 共 900*4 = 3600 个字符
    符号出现的位置: 4,8,12; (相对)
1000~9999: 3/15 编码; 共 9000*5 = 45000 个字符
10000~99999: 3/18 编码; 共 90000*6 = 540000 个字符
 """

q = int(input())

M = 12
a,b = 2,9
acc = []
for _ in range(M):
    # (多少个字符一个符号, 数字数量)
    acc.append((a,b))
    a += 1
    b *= 10

def cntL(x):
    ans = 0
    for m,c in acc:
        if x<=0: break
        if x >= m*c:
            ans += c
            x -= m*c
        else:
            ans += x//m
            x = 0
    return ans

def cntB(x):
    ans = 0
    for m,c in acc:
        if x<=0: break
        if x >= m*c:
            ans += c//3
            x -= m*c
        else:
            ans += x//(m*3)
            x = 0
    return ans


def f(l,r):
    n_all = cntL(r) - cntL(l-1)
    n_b = cntB(r) - cntB(l-1)
    return n_all-n_b, n_b

for _ in range(q):
    l,r = map(int, input().split())
    a,b = f(l,r)
    print(f"{a} {b}")
