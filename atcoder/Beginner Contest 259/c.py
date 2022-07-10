""" 
C - XX to XXX

"""
s = input().strip()
t = input().strip()
def f(s: str):
    ans = ""; 
    last = ""; cnt = 0
    for ch in s+" ":
        if ch!=last:
            last = ch; cnt = 1
        else:
            if cnt>=2: continue
            cnt += 1
        ans += ch
    return ans
print("Yes" if f(s)==f(t) else "No")