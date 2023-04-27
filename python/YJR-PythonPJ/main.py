import random
import sys

AGENT = 1   # 劳拉 ID
PLAYER = 2  # 玩家 ID
COLUMN = 8  # 列数
ROW = 6     # 行数
WIN = 4     # 获胜条件

# 存储棋盘信息，直接用行来存储
board = [[0 for i in range(COLUMN)] for j in range(ROW)]
ID_TO_SYMBOL = {  # 转换玩家 ID 和输出形式
    0: " ",
    1: "O",
    2: "X"
}


# 重定向标准输出，参考 https://www.jianshu.com/p/9c5c9d36eb31
class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass



def print_hello():
    """打印欢迎页面"""
    txt = ("\n"
           "Hi，我是劳拉，我们来玩一局四连环。我用 O 型棋子，你用 X 型棋子。\n"
           "游戏规则：双方轮流选择棋盘的列好放进自己的棋子，\n"
           "        若棋盘上有四颗相同型号的棋子在一行、一列或一条斜线上连接起来,\n"
           "        则使用该型号棋子的玩家就赢了！\n"
           "    ")
    print(txt)
    print("开始了！这是棋盘的初始状态：")
    print_board()


def print_board():
    """打印棋盘"""
    print(" " + " ".join("12345678"))
    for i in range(ROW - 1, -1, -1):
        line = board[i]
        line = "|" + "|".join([ID_TO_SYMBOL[i] for i in line]) + "|"
        print(line)
    print("-" * 17)
    print()


def get_available_col():
    """返回可下的列"""
    return [i for i, x in enumerate(board[-1]) if x == 0]


def put_piece(col, player):
    """将对应 player 的棋子放在指定列，然后打印棋盘"""
    col_list = [board[r][col] == 0 for r in range(0, ROW)]
    row = col_list.index(True)  # 找到第一个空的行
    board[row][col] = player
    print_board()


def agent_put_piece():
    """随机选择某一列下棋"""
    available_col = get_available_col()
    col_chosen = random.choice(available_col)
    print(">>>轮到我了，我把 O 棋子放在第 {} 列...".format(col_chosen + 1))

    return col_chosen


def player_put_piece():
    """请玩家输入所下的列"""
    col = input(">>>轮到你了，你放 X 棋子，请选择列号（1-8）：")
    # sys.stdout.write(str(col) + "\n")     # 这样会直接输出
    available_col = get_available_col()
    try:
        if not col.isdigit():
            print('请输入一个整数')
            return player_put_piece()
        col = int(col) - 1
        if col < 0 or col >= COLUMN:
            print("数字不在范围内，请重新输入")
            return player_put_piece()
        elif col not in available_col:
            print("第 {} 列已满，可选的列 {}".format(col, available_col))
            return player_put_piece()
        return col
    except Exception as e:
        print(e)


def check_board_full():
    """检查棋盘是否已满"""
    ava_col = get_available_col()
    return len(ava_col) == 0


def check_coordinate_win(col, row, player):
    """给定坐标，检查是否包含获胜条件"""
    test_player = ID_TO_SYMBOL[player]
    test_row = "".join(ID_TO_SYMBOL[x] for x in board[row])
    test_col = "".join(ID_TO_SYMBOL[x] for x in [board[r][col] for r in range(ROW)])
    available_col = list(range(0, COLUMN))
    available_row = list(range(0, ROW))
    test_main_diagonal = [board[row + i][col + i] for i in range(-WIN + 1, WIN) if
                          row + i in available_row and col + i in available_col]
    test_sub_diagonal = [board[row + i][col - i] for i in range(-WIN + 1, WIN) if
                         row + i in available_row and col - i in available_col]
    test_main_diagonal = "".join(ID_TO_SYMBOL[x] for x in test_main_diagonal)
    test_sub_diagonal = "".join(ID_TO_SYMBOL[x] for x in test_sub_diagonal)
    for test in [test_row, test_col, test_main_diagonal, test_sub_diagonal]:
        if test_player * WIN in test:
            return True
    return False


def check_win(col):
    """检查下定一个棋子后，是否获胜
    col 为上一此下的棋子的列数
    返回是否获胜
    """
    row_list = [board[r][col] for r in range(ROW)]
    row_list = [x != 0 for x in row_list]
    row = ROW - 1 - row_list[::-1].index(True)  # 找到最上面（最近所下）的棋子行数
    player = board[row][col]  # 玩家
    return check_coordinate_win(col, row, player)


if __name__ == "__main__":
    log_file = str(random.randint(10000, 99999)) + ".log"
    sys.stdout = Logger(filename=log_file, stream=sys.stdout)

    print_hello()
    while True:
        if check_board_full():
            print("棋盘已满，平局")
        agent_col = agent_put_piece()
        put_piece(agent_col, AGENT)
        if check_win(agent_col):
            print("*****{}*****".format("嘿嘿，我赢了！"))
            break
        player_col = player_put_piece()
        put_piece(player_col, PLAYER)
        if check_win(player_col):
            print("*****{}*****".format("好吧，你赢了！"))
            break

