""" 有一些tags; 从n个tags中挑选k个特征. 不放回采样. 
@230420

tags =  [('a', 0.1), ('b', 0.4), ('c', 0.1), ('d', 0.4)]

"""

import numpy as np
def select_k(tags, k):
    # 直接调包
    n = len(tags)
    ps = [t[1] for t in tags]
    idxs = np.random.choice(n, size=k, p=ps, replace=False)
    return [tags[i] for i in idxs]

k = 2
import random
def select_k(tags, k):
    # 这样在分布差异很大的时候可能效率太低
    probabilities = [t[1] for t in tags]

    # 根据概率分布随机选择k个元素
    chosen_idxs = set()
    for i in range(k):
        flag = False
        while True:
            r = random.random()
            cumulative_prob = 0
            for j, prob in enumerate(probabilities):
                cumulative_prob += prob
                if r <= cumulative_prob:
                    if j not in chosen_idxs:
                        chosen_idxs.add(j)
                        flag = True
                    break
            if flag: break

    return [tags[i] for i in chosen_idxs]

def select_k(tags, k):
    n = len(tags)
    probs = [t[1] for t in tags]
    idxs = list(range(n))
    chosen_idxs = set()

    # 这样写可能只采样到一个点? 换成while循环
    # for _ in range(k):
    while len(chosen_idxs)<k:
        s_prob = sum(probs)
        r = random.random() * s_prob
        cumulative_prob = 0
        for j, prob in enumerate(probs):
            cumulative_prob += prob
            if r <= cumulative_prob:
                chosen_idxs.add(j)
                probs.pop(j)
                idxs.pop(j)
                break

    return [tags[i] for i in chosen_idxs]

tags = [('a', 0.1), ('b', 0.4), ('c', 0.1), ('d', 0.4)]
tags = [('a', 0.1), ('b', 0.4), ('c', 0.1), ('d', 400)]
print(select_k(tags, k=2))