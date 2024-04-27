""" 
概率题: 在 (n,m) 的棋盘上, a,b 分别在 (x1,y1), (x2,y2) 的位置, a 先走, 随机左下/下/右下; b 随机左上/上/右上. 问 两者到达同一格子 (获胜) 概率
限制: n,m 3e3
思路1: #模拟 #DP
    可以知道两人相遇的行, 分别求出他们到这一行的概率分布即可.
    复杂度: O(n*m)

3 3 1 2 2 2
# 333333336
"""
MOD = 10**9+7
def f_rev(x):
    """ 求除法逆元 """
    return pow(x, MOD-2, MOD)
inv_3 = f_rev(3)
inv_2 = f_rev(2)

def calc_steps(x1,x2):
    if x1 > x2: return -1, -1
    else:
        a,b = divmod(x2-x1, 2)
        return a+b, a

def calc_prob(y, steps, m):
    probs = [0] * m
    probs[y] = 1
    for _ in range(steps):
        new_probs = [0] * (m)
        # new_probs[0] += probs[0] * inv_3 * 2
        # new_probs[1] += probs[0] * inv_3
        # new_probs[m-1] += probs[m-1] * inv_3 * 2
        # new_probs[m-2] += probs[m-1] * inv_3
        new_probs[0] = (new_probs[0] + probs[0] * inv_2) % MOD
        new_probs[1] = (new_probs[1] + probs[0] * inv_2) % MOD
        new_probs[m-1] = (new_probs[m-1] + probs[m-1] * inv_2) % MOD
        new_probs[m-2] = (new_probs[m-2] + probs[m-1] * inv_2) % MOD
        for i in range(1, m-1):
            new_probs[i-1] = (new_probs[i-1] + probs[i] * inv_3) % MOD
            new_probs[i] = (new_probs[i] + probs[i] * inv_3) % MOD
            new_probs[i+1] = (new_probs[i+1] + probs[i] * inv_3) % MOD
        probs = new_probs
    return probs


n,m,x1,y1,x2,y2 = map(int, input().split())
if m == 1:      # NOTE: 边界情况
    if x1 <= x2: print(1)
    else: print(0)
    exit()
x1,x2,y1,y2 = x1-1, x2-1, y1-1, y2-1
steps_a, steps_b = calc_steps(x1, x2)
if steps_a == -1:
    print(0)
else:
    probs_a = calc_prob(y1, steps_a, m)
    probs_b = calc_prob(y2, steps_b, m)
    ans = sum(p*q for p,q in zip(probs_a, probs_b)) % MOD
    print(ans)

# print(f_rev(3))
# print(calc_prob(1, 1, 3))