""" 
C - XX to XXX
给定两个字符串s,t. 若s中有连续两个相同的字符, 则可在它们之间插入一个相同的字符. 问s能够经过一定的操作变为t.
"""
s = input().strip()
t = input().strip()
def f(s: str):
    # 尝试将 s,t 都缩减. 但有问题, 因为 s 只能加字符不能减
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
# print("Yes" if f(s)==f(t) else "No")
def getCounts(s: str):
    ans = []
    last = ""; cnt = 0
    for ch in s +" ":
        if ch!=last:
            if last!="":
                ans.append((last,cnt))
            cnt = 1; last = ch
        else:
            cnt += 1
    return ans

sc, tc = getCounts(s), getCounts(t)
# 注意在zip之前不要漏掉这里的判断!!!
if len(sc)!=len(tc):
    print("No")
    exit()
for (chs,cs), (cht,ct) in zip(sc,tc):
    if chs!=cht or cs>ct or (cs==1 and ct>1):
        print("No")
        exit()
print("Yes")