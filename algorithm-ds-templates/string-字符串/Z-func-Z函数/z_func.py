""" @220428 Z 函数（扩展 KMP）
see https://oi-wiki.org/string/z-func/
"""

def z_func(s: str):
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