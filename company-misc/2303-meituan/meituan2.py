""" 坦克大战
在一个16*16的网格上, D,W初始位置为 (0,0,R), (15,15,L), 两人分别发出长度为256的指令. 指令包括: 
    F表示开火, 先于移动指令, 若摧毁对方则获胜;
    R,L,U,D表示移动; 执行都掉转方向; 若前面的格子没有被对方占领, 则往前一格否则在原地
若同时到达相同格子; 或者同时Fire对方, 则平局P
若没有因为上面的情况提前结束, 最后统计占据的格子数量
返回: (结束的轮次, 结果 D/W/P)

思路1: 大 #模拟
    但是好像只有 64% 的通过率? 不太懂哪里错了
 """

seqD = input()
seqW = input()
N = 16

def checkFire(s1,s2):
    """ s1 位置开火, 检查是否可以摧毁 s2 """
    if s1[2]=='R' and s1[0]==s2[0] and s1[1]<s2[1]: return True
    if s1[2]=='L' and s1[0]==s2[0] and s1[1]>s2[1]: return True
    if s1[2]=='U' and s1[1]==s2[1] and s1[0]>s2[0]: return True
    if s1[2]=='D' and s1[1]==s2[1] and s1[0]<s2[0]: return True
    return False

def moveDir(d, dir):
    if d=='R': dir[1] += 1
    elif d=='L': dir[1] -= 1
    elif d=='U': dir[0] -= 1
    elif d=='D': dir[0] += 1
    
def checkCollide(d,w):
    """ 检查是否会发生碰撞平局 """
    if d=='F' or w=='F': return False
    dD = D[:2]
    moveDir(d, dD)
    wD = W[:2]
    moveDir(w, wD)
    if dD==wD: return True
    return False

def move(s,cmd, role='D'):
    if cmd=='F': return
    s[2] = cmd      # 调整坦克的方向
    if cmd=='R':
        if s[1]<N-1 and grid[s[0]][s[1]+1] in ('.', role):
            s[1] += 1
            grid[s[0]][s[1]] = role
    elif cmd=='L':
        if s[1]>0 and grid[s[0]][s[1]-1] in ('.', role):
            s[1] -= 1
            grid[s[0]][s[1]] = role
    elif cmd=='U':
        if s[0]>0 and grid[s[0]-1][s[1]] in ('.', role):
            s[0] -= 1
            grid[s[0]][s[1]] = role
    elif cmd=='D':
        if s[0]<N-1 and grid[s[0]+1][s[1]] in ('.', role):
            s[0] += 1
            grid[s[0]][s[1]] = role

grid = [['.'] * N for _ in range(N)]
grid[0][0] = 'D'
grid[15][15] = 'W'
# cntD = cntW = 0

D = [0,0,'R']
W = [15,15,'L']
for i,(d,w) in enumerate(zip(seqD,seqW), start=1):
    # check fire. 先开火, 后移动
    f1,f2 = (d=='F' and checkFire(D,W)), (w=='F' and checkFire(W,D))
    if f1 and f2: print(f"{i}\nP"); exit()
    elif f1: print(f"{i}\nD"); exit()
    elif f2: print(f"{i}\nW"); exit()

    # check collide
    if checkCollide(d,w): print(f"{i}\nP"); exit()

    # move
    move(D,d,'D')
    move(W,w,'W')
    
cntD = sum([1 for i in range(N) for j in range(N) if grid[i][j]=='D'])
cntW = sum([1 for i in range(N) for j in range(N) if grid[i][j]=='W'])
# i 已经更新到了256
if cntD>cntW: print(f"{i}\nD")
elif cntD<cntW: print(f"{i}\nW")
else: print(f"{i}\nP")
