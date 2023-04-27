from easonsi import utils
from easonsi.util.leetcode import * 
from tqdm import tqdm

import random
n = 2002
anss = []
for _ in tqdm(range(10000)):
    arr = list(range(n))
    random.shuffle(arr)
    ans = 0
    for i,x in enumerate(arr):
        if x>i:
            if arr[x]==i: ans += 1
    anss.append(ans)
print(sum(anss)/len(anss))
