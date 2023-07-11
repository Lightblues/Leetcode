import time

""" @201112 
求解数独 """
t0 = time.time()


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.available = []
        self.value = 0


def rowNum(p, sudoku):
    row = set(sudoku[p.y * 9:(p.y + 1) * 9])
    row.remove(0)
    return row  # set type


def colNum(p, sudoku):
    col = []
    length = len(sudoku)
    for i in range(p.x, length, 9):
        col.append(sudoku[i])
    col = set(col)
    col.remove(0)
    return col  # set type


def blockNum(p, sudoku):
    block_x = p.x // 3
    block_y = p.y // 3
    block = []
    start = block_y * 3 * 9 + block_x * 3
    for i in range(start, start + 3):
        block.append(sudoku[i])
    for i in range(start + 9, start + 9 + 3):
        block.append(sudoku[i])
    for i in range(start + 9 + 9, start + 9 + 9 + 3):
        block.append(sudoku[i])
    block = set(block)
    block.remove(0)
    return block  # set type


def initPoint(sudoku):
    # 输入一个列表表示棋盘，返回一个点列表
    pointList = []
    length = len(sudoku)
    for i in range(length):
        if sudoku[i] == 0:
            p = point(i % 9, i // 9)
            for j in range(1, 10):
                if j not in rowNum(p, sudoku) and j not in colNum(p, sudoku) and j not in blockNum(p, sudoku):
                    p.available.append(j)
            pointList.append(p)
    return pointList


def tryInsert(p, sudoku):
    availNum = p.available
    for v in availNum:
        p.value = v
        if check(p, sudoku):
            sudoku[p.y * 9 + p.x] = p.value
            if len(pointList) <= 0:
                t1 = time.time()
                useTime = t1 - t0
                showSudoku(sudoku)
                print('\nuse Time: %f s' % (useTime))
                # exit()
                return 0
            p2 = pointList.pop()
            tryInsert(p2, sudoku)
            sudoku[p2.y * 9 + p2.x] = 0
            sudoku[p.y * 9 + p.x] = 0
            p2.value = 0
            pointList.append(p2)
        else:
            pass


def check(p, sudoku):
    if p.value == 0:
        print('not assign value to point p!!')
        return False
    if p.value not in rowNum(p, sudoku) and p.value not in colNum(p, sudoku) and p.value not in blockNum(p, sudoku):
        return True
    else:
        return False


def showSudoku(sudoku):
    for j in range(9):
        for i in range(9):
            print('%d ' % (sudoku[j * 9 + i]), end='')
        print('')


# if __name__=='__main__':
sudoku = [
    7, 0, 0, 6, 0, 2, 0, 5, 0,
    0, 0, 5, 0, 0, 0, 8, 0, 1,
    0, 8, 0, 0, 0, 3, 7, 0, 2,
    0, 0, 0, 0, 0, 8, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 3, 9, 7,
    1, 9, 3, 0, 0, 0, 0, 0, 0,
    3, 0, 1, 0, 0, 5, 0, 7, 0,
    0, 7, 0, 0, 1, 6, 5, 0, 0,
    5, 0, 6, 0, 0, 0, 0, 0, 9,

]
pointList = initPoint(sudoku)
showSudoku(sudoku)
print('\n')
p = pointList.pop()
tryInsert(p, sudoku)
