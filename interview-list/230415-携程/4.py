""" 
给定n个数字, 分别表示有多少连续个1/0, 对于这个长序列, 问有多少回文子串? 
限制: n 1e3; 数字 1e9, 对答案取模
思路1: #分类
    对于一组连续数字内部, 若数字数量为k, 则共有 n+(n-1)+...+1 共 k*(k+1)/2 个回文子串
    对于跨组的回文串, 显然要求左右两侧的数量相同时, 才能往外扩散, 采用「中心扩散法」
"""
mod = 10**9+7

n = int(input())
arr = list(map(int, input().split()))
ans = 0
for i in range(n):
    ans = (ans + arr[i]*(arr[i]+1)//2) % mod
for i in range(1,n-1):
    acc = 0
    for j in range(1, n):
        l,r = i-j, i+j
        if l<0 or r>=n: break
        a,b = arr[l], arr[r]
        acc += min(a,b)
        if a!=b: break
    ans = (ans + acc) % mod
print(ans)

