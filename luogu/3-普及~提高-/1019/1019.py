""" P1019 [NOIP2000 提高组] 单词接龙 #暴力 DFS
给定一组单词, 每个词最多用两次, 接龙要求前后缀匹配但不能包含 (例如 at 后不能接 attention, 事实上这样就没用了, 同样更长的覆盖也是浪费的). 问给定一个起始字符最长的结果.
限制: 单词数量 20, 但长度等限制没说清楚
思路1: #预处理 之后暴力 #DFS
    看到题目说「不保证存在靠谱的做法能通过该数据范围下的所有数据」, 也就不分析复杂度直接暴力DFS了
    具体而言, 计算所有单词之前的匹配长度, 然后用一个全局数组记录使用情况 (因为最多可以用两次)
"""

n = int(input())
words = []
for _ in range(n):
    words.append(input().strip())
startCh = input().strip()
def checkLen(w1, w2):
    # get the min common postfix(w1) and prefix(w2), 不能是包含关系
    for l in range(1, min(len(w1), len(w2))):
        if w1[-l:] == w2[:l]:
            return l
    return -1
common = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        common[i][j] = checkLen(words[i], words[j])
ans = 0
used = [0] * n
def dfs(last:int, cur:int):
    global ans
    flag = False
    for i, u in enumerate(used):
        if u==2: continue
        co = common[last][i]
        if co<=0: continue
        flag = True
        used[i] += 1
        dfs(i, cur+len(words[i])-co)
        used[i] -= 1
    if not flag:
        ans = max(ans, cur)
for i,w in enumerate(words):
    if w[0]==startCh:
        used[i]+=1
        dfs(i, len(w))
        used[i]-=1
print(ans)