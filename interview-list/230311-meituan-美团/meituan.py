""" 流星
input: n个流星, 给定 (start,end) 时间区间, 求最多同时出现的流星数, 以及最长的时间段
限制: n 1e6, 时间范围 1e9
output: (maxCnt, maxTime)

思路1: #差分 记录区间; 然后 #前缀和 计算累计数量; 由于数字范围较大需要利用dict
 """

from collections import defaultdict
# 处理输入
n = int(input())
start = list(map(int, input().split()))
end = list(map(int, input().split()))

# 差分统计区间. 由于时间范围很大, 所以用前缀和来统计
t2cnt = defaultdict(int)
for s,e in zip(start, end):
    t2cnt[s] += 1
    t2cnt[e+1] -= 1

t2cnt = sorted(t2cnt.items(), key=lambda x: x[0])
mxCnt = 0       # 最多同时出现的流星数
mxTime = 0
flag = False    # flag 标记当前区间是否在最大时间段
acc = 0         # 统计前缀和
for i,(t,cnt) in enumerate(t2cnt):
    acc += cnt
    if flag==True:
        # 上一个区间是最大数量
        mxTime += t-t2cnt[i-1][0]
    if acc > mxCnt:
        # 出现了新的最大数量
        flag = True
        mxTime = 0
        mxCnt = acc
    elif acc == mxCnt:
        flag = True
    else:
        flag = False

print(f"{mxCnt} {mxTime}")

