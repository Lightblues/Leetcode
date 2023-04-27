""" 简单 """
from collections import Counter
def getUniqueCharacter(s):
    cnt = Counter(s)
    for i,x in enumerate(s):
        if cnt[x]==1: return i+1
    return -1

for s in ["hackthegame", "falafal"]:
    print(getUniqueCharacter(s))
