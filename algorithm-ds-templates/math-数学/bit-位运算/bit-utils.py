def printBit(x: int):
    # 打印二进制
    return f"{x:b}"

def lowbit(x: int):
    # 获取最低位的 1
    return x & -x

def getSubsets(mask: int):
    # 降序遍历 mask 的非空子集. mask 二进制表示集合
    res = []
    s = mask
    while s:
        res.append(s)
        s = (s-1) & mask
    return res

x = 0b1010
print(f"x={x:b}, lowbit={lowbit(x):b}")
print(f"subsets: {getSubsets(x)}")