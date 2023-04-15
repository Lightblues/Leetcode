""" 删除字符串中字典序最小的k个字符
s = "abcd", k = 3
"d"
s = "xxaaabyycdzz", k = 4
"xxyyzz"
a: 3
b: 1

应用: 谣言检测; RE/KG


游戏场景下的对话. KG的应用? 
如何根据语境查到知识? 
说话的风格语调? 
安全性? 模拟游戏角色

对实习生的期望? 有自己的想法; 主动找一些问题和方案. 
"""


# from string import ascii_lowercase
from collections import Counter, defaultdict
def f(s, k):
    cnt = Counter(s)
    toDelete = defaultdict(int)
    for ch,c in sorted(cnt.items()):
        t = min(k, c)
        toDelete[ch] = t
        k -= t
        if k==0: break
    ans = []
    for c in s:
        if toDelete[c]>0:
            toDelete[c] -= 1
        else: ans.append(c)
    return "".join(ans)

for ans in (
    f(s = "xxaaabyycdzz", k = 4),
    f("dcbab", 2),
    f("dcbab", 3),
):
    print(ans)
