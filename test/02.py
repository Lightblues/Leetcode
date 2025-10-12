""" 
2 5
red book game music sigma
mozart 3
book classic music
arcaea 4
red music game hard
"""

import sys
from collections import defaultdict

m,n = map(int, sys.stdin.readline().split())
keywords = set(sys.stdin.readline().split())
res = defaultdict(list)
for _ in range(m):
    name, _ = sys.stdin.readline().split()
    keys = set(sys.stdin.readline().split())
    res[len(keys & keywords)].append(name)
for c in sorted(res.keys(), reverse=True):
    for name in res[c]:
        print(name)
