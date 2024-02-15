""" @220428 Z 函数（扩展 KMP）
see https://oi-wiki.org/string/z-func/

Z-函数的定义是什么? [区分KMP中的前缀函数是往前!]
    z[i] 表示 s[i...n-1] 和 s 的最长公共前缀长度! (也即从i位置往后匹配s的前缀)
"""

def z_func(s: str):
    """ Z-函数的定义是什么? z[i] 表示 s[i...n-1] 和 s 的最长公共前缀长度! (也即从i位置往后匹配s的前缀) """
    n = len(s)
    z = [0] * n
    l,r = 0,0
    for i in range(1,n):
        if i<=r and z[i-l]<r-i+1:
            z[i] = z[i-l]
        else:
            z[i] = max(0, r-i+1)
            while i+z[i]<n and s[z[i]]==s[i+z[i]]:
                z[i] += 1
        if i+z[i]-1 > r:
            r = i+z[i]-1
            l = i
    return z

res = [
    z_func("aaaaa"),
    z_func("ababab"),
]
for r in res:
    print(r)