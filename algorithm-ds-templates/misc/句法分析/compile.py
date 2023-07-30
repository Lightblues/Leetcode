from easonsi import utils
from easonsi.util.leetcode import *
""" 
0224. 基本计算器 #hard #题型
    要求实现一个解析 +/- 的计算器. 输入字符串形如 ` 2-1 + 22 `, `(1+(4+5+2)-3)+(6+8)`, 也即需要处理空格和括号的情况, 不存在单元的 +/- 符号.
    思路2: 用两个栈分别记录数字和符号(与括号); 按照运算符的优先级出栈
0227. 基本计算器 II / 面试题 16.26. 计算器 #medium
    相较于 0224, 多了乘除算子, 但不需要考虑括号.
    其实也是用栈记录中间结果. 不过这里只有两种优先级, 可以不用栈.
    
1896. 反转表达式值的最少操作次数 #hard #双栈 #语法分析
    给定一个形如 `"1&(0|1)"` 的布尔表达式, 问最少通过多少操作使其的值发生改变, 例如将这个例子的值变为0, 可以将|操作变为&, 或者将其中一个1变为0.
    允许的操作是: 翻转 0/1, 或者翻转&/|
    思路1: 使用 #双栈 记录 操作符和运算元. 运算元记录将节点变为 0/1 所需的最小操作数. 利用 &| 节点的性质得到递推公式.

 """
class Solution:

    


    """ 1896. 反转表达式值的最少操作次数 #hard #双栈 #语法分析
- 关联: 0224. 基本计算器
给定一个形如 `"1&(0|1)"` 的布尔表达式, 问最少通过多少操作使其的值发生改变, 例如将这个例子的值变为0, 可以将|操作变为&, 或者将其中一个1变为0.
允许的操作是: 翻转 0/1, 或者翻转&/|
限制: 表达式长度 1e5
思路1: 使用 #双栈 记录 操作符和运算元. 运算元记录将节点变为 0/1 所需的最小操作数. 利用 &| 节点的性质得到递推公式.
    参考 0224, 为了处理操作和括号语句, 采用双栈来分别存储数字和运算符.
        不同之处在于, 这里不是求表达式的值, 而是问最少操作次数. 为此, 将运算元记录变为 `(x,y)` 表示将该节点变为 0/1 分别所需的最小操作数.
        如何确保 **相同级别的操作符顺序执行**? 这里的策略是遇到布尔值就尝试用掉前面的操作符, 直到遇上左括号.
    显然, 遇到叶子节点, 即布尔值的时候, 记录分别为 (1,0) 和 (0,1)
    关键在于, 遇到一个操作符的时候如何更新?
        例如, 当前为 &节点, 假设两子节点返回的分别为 (x1,y1) (x2,y2)
        在不改变节点为| 的情况下, 要求其值为 0/1, 所需的最少操作数分别为 `min{x1+x2, x1+y2, x2+y1}` (实际上就是 `min{x1, x2}`, 这里应该是为了和or节点保持一致), `x2+y2`, 记为 `x_and, y_and`
        然而, 另一种将表达式值变为 1 的方式是将操作符变为 or, 然后只需要 `y_or` 个操作即可.
        综上, 节点记录的更新公式为 `(min(x_and, x_or + 1), min(y_and, y_or + 1))`
    [官答](https://leetcode.cn/problems/minimum-cost-to-change-the-final-value-of-expression/solution/fan-zhuan-biao-da-shi-zhi-de-zui-shao-ca-s9ln/)
思路2: 
    符合自己一开始的想法: 如果已有了输入字符串对应语法树, 求解是比较简单的 (不一定需要上面的策略). 但问题还是如何构建语法树?
    下面还是用 #双栈 分别存储数字和运算符, 然后定义节点构建二叉树结构.
    还是那个问题, 如何保证 **相同级别的操作符顺序执行**? 可以给操作符定义优先级 (例如 `dict(zip('(&|', (0, 1, 1)))`), 当遇到某一操作符的时候, 将更高或相同优先级的运算符全部用掉. 这一思路比上面的更为通用.
    [here](https://leetcode.cn/problems/minimum-cost-to-change-the-final-value-of-expression/solution/zhong-zhui-biao-da-shi-gou-zao-er-cha-bi-gman/)
"""
    def minOperationsToFlip(self, expression: str) -> int:
        """ https://leetcode.cn/problems/minimum-cost-to-change-the-final-value-of-expression/solution/fan-zhuan-biao-da-shi-zhi-de-zui-shao-ca-s9ln/
        用两个栈来保存运算符, 以及中间结果. 注意, stack_num 中的元素 (x,y) 分别为将该子树的表达式值变为 0/1 所需的最小操作数 """
        # 数字栈
        stack_num = list()
        # 符号栈
        stack_op = list()

        def op_and(x1: int, y1: int, x2: int, y2: int):
            # 不改变 & 节点符号, 使得该节点值为 0/1 的最少操作数
            # 例如, `y1 + y2` 表示通过令左右子树的值都为 1, 来使得结果为 1
            return min(x1 + x2, x1 + y2, y1 + x2), y1 + y2
        def op_or(x1: int, y1: int, x2: int, y2: int):
            return x1 + x2, min(x1 + y2, y1 + x2, y1 + y2)
        
        # 尝试将数字栈顶的两个二元组和符号栈顶的运算符进行运算
        def calc():
            if len(stack_num) >= 2 and stack_op[-1] in ["|", "&"]:
                x1, y1 = stack_num.pop()
                x2, y2 = stack_num.pop()
                # 不改变节点符号 (& |) 的情况下的最小操作数
                x_and, y_and = op_and(x1, y1, x2, y2)
                x_or, y_or = op_or(x1, y1, x2, y2)
                # 注意还需要考虑改变节点符号. 例如下面求将一个 & 节点变为0的操作数为 `min(x_and, x_or + 1)`, 其中 `x_and` 是通过修改子节点使得左右孩子均为1, 而 `x_or + 1` 表示将节点变为 | 节点, 然后让子节点符合需求.
                if (op := stack_op.pop()) == "&":
                    stack_num.append((min(x_and, x_or + 1), min(y_and, y_or + 1)))
                else:
                    stack_num.append((min(x_or, x_and + 1), min(y_or, y_and + 1)))

        for ch in expression:
            if ch in ["(", "|", "&"]:
                stack_op.append(ch)
            # 为了保证相同级别的运算符顺序执行, 会将符号栈中的非左括号的运算符全部运算掉
            elif ch == "0":
                stack_num.append((0, 1))
                calc()
            elif ch == "1":
                stack_num.append((1, 0))
                calc()
            else:
                assert ch == ")"
                # 此时符号栈栈顶一定是左括号
                stack_op.pop()
                calc()
        # 注意我们没有求原本表达式的值; 但由于「动态规划中的状态转移一定是最优的」, 因此我们最终得到的 (x,y) 中一定有一个值为0, 对应着原本的表达式值.
        return max(stack_num[0])

    def minOperationsToFlip(self, expression: str) -> int:
        """ https://leetcode.cn/problems/minimum-cost-to-change-the-final-value-of-expression/solution/zhong-zhui-biao-da-shi-gou-zao-er-cha-bi-gman/
        也只利用双栈来解析表达式, 只是定义了节点和dfs函数, 理解上更为清晰? """
        class MyNode:
            def __init__(self, val='0', left: Optional['MyNode'] = None, right: Optional['MyNode'] = None):
                self.val = val
                self.left = left
                self.right = right

        def dfs(root: Optional['MyNode']) -> Tuple[int, int]:
            """返回(变为0的最小操作次数,变为1的最小操作次数)"""
            if not root:
                return int(1e20), int(1e20)
            if root.val.isdigit():
                return int(root.val == '1'), int(root.val == '0')

            left0, left1 = dfs(root.left)
            right0, right1 = dfs(root.right)
            res0, res1 = int(1e20), int(1e20)

            if root.val == '&':
                res0 = min(res0, left0 + right0, left0 + right1, left1 + right0)
                res1 = min(res1, left1 + right1, left0 + right1 + 1, left1 + right0 + 1)
            else:
                res0 = min(res0, left0 + right0, left0 + right1 + 1, left1 + right0 + 1)
                res1 = min(res1, left1 + right1, left0 + right1, left1 + right0)

            return res0, res1


        weight = dict(zip('(&|', (0, 1, 1)))    # 定义不同符号的优先级
        numStack, optStack = [], []
        expression += ')'       # 加一个哨兵
        for char in expression:
            if char == '(':
                optStack.append(char)
            elif char.isdigit():
                numStack.append(MyNode(char))
            elif char in '&|':
                # 遇到运算符, 将更高或相同优先级的运算符全部用掉
                while optStack and weight[optStack[-1]] >= weight[char]:
                    node2, node1 = numStack.pop(), numStack.pop()
                    numStack.append(MyNode(optStack.pop(), node1, node2))
                optStack.append(char)
            elif char == ')':
                # 遇到左括号
                while optStack and optStack[-1] != '(':
                    ndoe2, node1 = numStack.pop(), numStack.pop()
                    numStack.append(MyNode(optStack.pop(), node1, ndoe2))
                if optStack:
                    optStack.pop()

        root = numStack[0]
        return max(dfs(root))

    
    
    
    
    
    
    def testClass(self, inputs):
        # 用于测试 LeetCode 的类输入
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
sol = Solution()
result = [

]
for r in result:
    print(r)
