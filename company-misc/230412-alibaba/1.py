""" 
要求构造一个01序列, 长n, 包括k个长为3的回文串
边界: n<3!
1 0
"""

n,k = map(int, input().split())
if n<3:
    print(-1 if k>0 else '0'*n)
elif k>n-2: 
    # 注意不可能的情况! 
    print(-1)
else:
    ans = '1' * (k+2)
    r = n-k-2
    ans += ('0011' * (r//4+1))[:r]
    print(ans)