""" 井字棋
写一个简单的井字棋游戏
需要满足两个主要功能:
1.能实现玩家对战;
2.能实现玩家和电脑对战。而玩家和电脑对战又需要 有两个模式:
    1.对战高级电脑;
    2.对战低级电脑。
设定高级电脑模式不会输给玩家 (玩家只会输给电 脑，或者和电脑平局）,
低级电脑模式电脑随机落子。
游戏的主界面用于根据用户选择，而决定游戏进入 什么模式, 如果玩家不想玩了, 即可通过主界面退 出游戏。
程序需要即时对每一次对战的每一步做出判断：首 先, 落子的位置是否合理, 如果已经有棋子则不能 落子。
其次, 如果成功落子, 则场面上是否有已经获胜的 玩家，如果已经有获胜的玩家则停止落子,
反馈已经胜利的玩家, 同时返回主页面等待用户的 下一次输入。
"""

""" 实现「高级电脑模式」
Agent目标: 后手不会输
开局的前两步策略是固定的:
    先手: 中间
    后手: 角
在后手的情况下, 对方下完棋之后, 检查两种情况
    1) 再下一个变成「三连」的, 例如 `XX.`. checkTree()
    2) 下一个子变成「双活二」. checkDoubleTwo()
        X..
        .X.
    其他情况下, 你可以选择下在任意位置
"""

#%%
# 老师要求用 theBoard 这样的数据格式, 配合 printBoard 函数. 
theBoard = {'top-L': ' ', 'top-M': ' ', 'top-R': ' ',
    'mid-L': ' ', 'mid-M': ' ', 'mid-R': ' ',
    'low-L': ' ', 'low-M': ' ', 'low-R': ' '}
# 下面为了方便判断, 实际上用 board 数组来存储棋盘, 和 theBoard 同步修改
board = [[0]*3 for _ in range(3)]
# 1/2 分别表示先后手

str_indexs = """top-L top-M top-R
mid-L mid-M mid-R
low-L low-M low-R"""
index2xy = {
    "top-L": (0,0),
    "top-M": (0,1),
    "top-R": (0,2),
    "mid-L": (1,0),
    "mid-M": (1,1),
    "mid-R": (1,2),
    "low-L": (2,0),
    "low-M": (2,1),
    "low-R": (2,2),
}
xy2index = {v:k for k,v in index2xy.items()}
val2str = {0: ' ', 1: 'X', 2: 'O'}

def clearBoard():
    """ 清空棋盘 """
    for choice in index2xy:
        theBoard[choice] = ' '
    for i in range(3):
        for j in range(3):
            board[i][j] = 0

#%%
def printBoard(board):
    print(board['top-L'] + '|' + board['top-M'] + '|' + board['top-R']) 
    print('-+-+-')
    print(board['mid-L'] + '|' + board['mid-M'] + '|' + board['mid-R']) 
    print('-+-+-')
    print(board['low-L'] + '|' + board['low-M'] + '|' + board['low-R']) 


#%%
def getInput():
    """ 得到用户输入 """
    while True:
        print(f"{str_indexs}")
        choice = input("请落子：")
        if choice not in index2xy:
            print("输入错误"); continue
        else:
            if checkValid(choice)==False:
                print("当前位置已有棋子, 输入错误"); continue
            else:
                return choice

def checkValid(choice):
    if theBoard[choice] != ' ': return False
    else: True

def putChess(choice, player):
    """ 在位置 choice 放置棋子 """
    x, y = index2xy[choice]
    board[x][y] = player
    theBoard[choice] = val2str[player]

# 处理用户输入...
# player = 1
# choice = getInput()
# putChess(choice, player)

#%%
def checkIsOver():
    """ 检查游戏是否结束, 返回 0/1/2 表示平局/获胜, 或者没有结束 -1 """
    if checkWinner(1): return 1
    if checkWinner(2): return 2
    if all(theBoard[choice] != ' ' for choice in index2xy):
        return 0
    return -1

def checkWinner(player):
    """ 检查盘面上player是否获胜 """
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def printResult(r):
    """ 处理checkIsOver返回结果 """
    if r==0: print("平局")
    elif r==1: print("先手获胜")
    elif r==2: print("后手获胜")

# checkWinner(1)
# board[0] = [1]*3
# print(board)
# checkIsOver()



#%%

def checkThree(player):
    """ 检查身份为 player 的玩家是否可以完成「三连」 """
    for i in range(3):
        row = board[i]
        if row.count(player) == 2 and row.count(0) == 1:
            return (i, row.index(0))
        col = [board[j][i] for j in range(3)]
        if col.count(player) == 2 and col.count(0) == 1:
            return (col.index(0), i)
    diag = [board[i][i] for i in range(3)]
    if diag.count(player) == 2 and diag.count(0) == 1:
        return (diag.index(0), diag.index(0))
    diag = [board[i][2-i] for i in range(3)]
    if diag.count(player) == 2 and diag.count(0) == 1:
        return (diag.index(0), 2-diag.index(0))
    return None

# board = [
#     [1,2,1],
#     [0,1,0],
#     [0,1,2]
# ]
# r = checkThree(1)
# print(r)


#%%
def _checkDoubleTwo(player):
    """ 统计棋盘中player玩家的「活二」数量 """
    cnt = 0
    for i in range(3):
        row = board[i]
        if row.count(player) == 2 and row.count(0) == 1:
            cnt += 1
        col = [board[j][i] for j in range(3)]
        if col.count(player) == 2 and col.count(0) == 1:
            cnt += 1
    diag = [board[i][i] for i in range(3)]
    if diag.count(player) == 2 and diag.count(0) == 1:
        cnt += 1
    diag = [board[i][2-i] for i in range(3)]
    if diag.count(player) == 2 and diag.count(0) == 1:
        cnt += 1
    return cnt>=2
def checkDoubleTwo(player):
    """ 检查身份为 player 的玩家是否可以完成「双活二」 """
    for i in range(3):
        for j in range(3):
            if board[i][j]!=0: continue
            # 模拟下子, 然后删掉
            board[i][j] = player
            res = _checkDoubleTwo(player)
            board[i][j] = 0
            if res: return (i,j)
    return None

# board = [
#     [1,0,0],
#     [0,1,0],
#     [0,0,2]
# ]
# r = checkDoubleTwo(1)
# print(r)
#%%
def agent(step, player):
    """ agent """
    # 前两手
    if step==0:
        return (1,1) if board[1][1]==0 else (0,0)
    oppo = 1 if player==2 else 2
    # 自己可以先获胜
    res = checkThree(player)
    if res: return res
    # 检查需要防住的
    res = checkThree(oppo)
    if res: return res
    res = checkDoubleTwo(oppo)
    if res: return res
    # 自己优先的策略
    res = checkDoubleTwo(player)
    if res: return res
    # 否则随便下
    for i in range(3):
        for j in range(3):
            if board[i][j]==0: return (i,j)
    # 没有空余位置了
    return None

def loopX():
    """ 用户先手 """
    step = 0
    userPlayer, agentPlayer = 1, 2
    while True:
        r = checkIsOver()
        if r!=-1: break
        # 打印棋盘, 处理用户输入
        printBoard(theBoard)
        choice = getInput()
        putChess(choice, userPlayer)
        r = checkIsOver()
        if r!=-1: break
        # 决策
        xy = agent(step, agentPlayer)
        putChess(xy2index[xy], agentPlayer)
        # 累计步数
        step += 1
    return r
def loopO():
    step = 0
    userPlayer, agentPlayer = 2, 1
    while True:
        r = checkIsOver()
        if r!=-1: break
        # 决策
        xy = agent(step, agentPlayer)
        putChess(xy2index[xy], agentPlayer)
        r = checkIsOver()
        if r!=-1: break
        # 打印棋盘, 处理用户输入
        printBoard(theBoard)
        choice = getInput()
        putChess(choice, userPlayer)
        # 累计步数
        step += 1
    return r

# %%
if __name__=="__main__":
    clearBoard()
    mark1 = input('亲爱的玩家,请选择您的棋子(O/X)：')
    # 下面把先后手分开写了, 应该可以写到一起
    if mark1 == 'X':
        r = loopX()
    else: 
        r = loopO()
    printBoard(theBoard)
    printResult(r)


