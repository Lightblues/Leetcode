from easonsi.util.leetcode import *

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
Easonsi @2023 """


class Poly(collections.Counter):
    def __add__(self, other):
        self.update(other)
        return self

    def __sub__(self, other):
        self.update({k: -v for k, v in other.items()})
        return self

    def __mul__(self, other):
        ans = Poly()
        for k1, v1 in self.items():
            for k2, v2 in other.items():
                ans.update({tuple(sorted(k1 + k2)): v1 * v2})
        return ans

    def evaluate(self, evalmap):
        ans = Poly()
        for k, c in self.items():
            free = []
            for token in k:
                if token in evalmap:
                    c *= evalmap[token]
                else:
                    free.append(token)
            ans[tuple(free)] += c
        return ans

    def to_list(self):
        return ["*".join((str(v),) + k)
                for k, v in sorted(self.items(), key = lambda x: (-len(x[0]), x[0], x[1]))
                if v]


class Solution:
    """  """
    def calculate_template(self, s: str) -> int:
        s = s.replace(' ', '')
        # 预处理
        seq = []
        num = []
        for i,c in enumerate(s):
            if c==' ': continue
            elif c.isdigit():  num.append(c)
            elif c in "()+-*/": 
                # 1.1] 处理负数情况!
                if c=='-' and (i==0 or s[i-1] in "(+-"): seq.append(0)
                if num: seq.append(int(''.join(num)) if num else 0); num = []
                seq.append(c)
            else: raise ValueError(f"Unknown character {c}")
        if num: seq.append(int(''.join(num)))
        
        # 辅助函数: 计算一次运算
        def calc(nums, ops):
            b = nums.pop(); a = nums.pop()
            op = ops.pop()
            if op=='+': nums.append(a+b)
            elif op=='-': nums.append(a-b)
            elif op=='*': nums.append(a*b)
            elif op=='/': nums.append(a//b)
            else: raise ValueError(f"Unknown operator {op}")
        # 定义符号优先级
        op2prio = {'+':1, '-':1, '*':2, '/':2}
        # 
        ops = []
        nums = []   # 1.2] 上面已经处理了负数情况, 这里不需要再加哨兵符号
        for x in seq:
            if type(x)==int: nums.append(x)
            elif x=='(': ops.append(x)
            elif x==')':
                while ops[-1]!='(': calc(nums, ops)
                ops.pop()
            elif x in "+-*/": 
                while ops and ops[-1]!='(' and op2prio[ops[-1]]>=op2prio[x]:
                    calc(nums, ops)
                ops.append(x)
            else: raise ValueError(f"Unknown character {x}")
        while ops: calc(nums, ops)
        return nums[-1]
    
    
    """ 0224. 基本计算器 #hard #题型
要求实现一个解析 +/- 的计算器. 输入字符串形如 ` 2-1 + 22 `, `(1+(4+5+2)-3)+(6+8)`, 也即需要处理空格和括号的情况, 不存在单元的 +/- 符号.
思路1: 将括号表达式展开, 用 #栈 记录符号状态
    [官答](https://leetcode.cn/problems/basic-calculator/solution/ji-ben-ji-suan-qi-by-leetcode-solution-jvir/)
    由于括号表达式只有加减法, 因此考虑将其展开, 只需要计算每一个元素前的符号即可.
    如何处理括号? 可以用 #栈 来记录括号前的符号; 这样, 对于括号内的每一个数字的符号, 只需要 `opStack[-1] * op` 即可, 这里的op是当前 +/- 符号
    技巧: 除了括号以及加减符号固定为1 之外, 数字的长度不确定, 因此相较于用 for训练解析表达式, 用while循环更加方便, 只需要在处理数字的时候内层进行遍历来搜索完整的数字即可.
思路2: #双栈 通用解法 用两个栈分别记录数字和符号(与括号)
    用两个栈分别保存历史的运算符和运算单元 ops, nums. 顺序遍历, 
        1) 出现运算符, 则将栈内比该运算符更高或相同级别的运算符使用掉; 
        2) 将做括号也加入运算符栈, 这样出现右括号的时候, 将第一个匹配到的左括号之前的运算符使用掉.
    细节: 为了防止空栈错误, 在 nums 栈内加入哨兵 `0`
    see [here](https://leetcode.cn/problems/basic-calculator/solution/shuang-zhan-jie-jue-tong-yong-biao-da-sh-olym/)
"""
    def calculate(self, s: str) -> int:
        """ 思路1: 将括号表达式展开, 用栈记录符号状态 """
        opStack = [1]
        op = 1
        ans = 0
        idx = 0
        # 采用while循环而不是for, 这样处理数字的时候更方便
        while idx < len(s):
            if s[idx] == ' ': idx += 1
            elif s[idx] == '(':
                opStack.append(op)  # add current op to stack
                idx += 1
            elif s[idx] == ')':
                op = opStack.pop()  # pop the last op, 并且将当前的符号设置为该括号之前的状态
                idx += 1
            elif s[idx] == '+':
                op = opStack[-1]
                idx += 1
            elif s[idx] == '-':
                op = -opStack[-1]
                idx += 1
        else:
            # 处理数字
                num = 0
                while idx < len(s) and s[idx].isdigit():
                    num = num * 10 + int(s[idx])
                    idx += 1
                ans += num * op
        return ans

    def calculate(self, s: str) -> int:
        # 去除空格, 来处理 ...(-5) 这种情况
        s = s.replace(' ', '')
        # 运算符号优先级
        hashmap = {
            '-': 1,
            '+': 1,
            '*': 2,
            '/': 2,
            '%': 2,
            '^': 3,
        }

        # 存放所有数字
        nums = [0]  # 为了防止第一个数为负数，先往nums加个0
        # 存放所有的操作
        ops = []

        def calc(nums, ops):
            if not nums or len(nums) < 2 or not ops:
                return
            b, a = nums.pop(), nums.pop()
            op = ops.pop()
            if op == '+':
                ans = a + b
            elif op == '-':
                ans = a - b
            elif op == '*':
                ans = a * b
            elif op == '/':
                ans = a // b
            elif op == '^':
                ans = int(pow(a, b))
            elif op == '%':
                ans = a % b
            nums.append(ans)

        n = len(s)
        i = 0
        while i < n:
            c = s[i]
            if c == ' ':
                i += 1
                continue
            # 1. 处理括号
            if c == '(':
                ops.append(c)
            elif c == ')':
                while ops:
                    if ops[-1] != '(':
                        calc(nums, ops)
                    else:
                        ops.pop()
                        break
            else:
                # 2. 处理数字, 入栈 nums
                if c.isdigit():
                    u = 0
                    while i < n and s[i].isdigit():
                        u = u * 10 + int(s[i])
                        i += 1
                    nums.append(u)
                    i = i - 1   # 在最后统一移动 i += 1
                else:
                    # 3. 处理运算符 和括号
                    # 考虑处理首位的 +/- 符号
                    if i > 0 and s[i - 1] in '(+-':
                        nums.append(0)
                    while ops and ops[-1] != '(':
                        # 当遇到一个运算符的时候, 将栈内此前的更高等级的运算符用掉
                        prev = ops[-1]
                        if hashmap[prev] >= hashmap[c]:
                            calc(nums, ops)
                        else:
                            break
                    ops.append(c)
            i += 1

        while ops and ops[-1] != '(':
            calc(nums, ops)
        return nums[-1]

    """ 0227. 基本计算器 II / 面试题 16.26. 计算器 #medium
相较于 0224, 多了乘除算子, 但不需要考虑括号.
思路0: 用一个curr数字来记录乘除的结果, 只有当出现加减的时候才累加到ans中.
    由于没有括号, 这里没有采用栈, 直接遍历.
    如何处理乘除法的优先级? 用curr记录当前数字/乘除结果, 只有遇到加减的时候才累加到ans中. (这样为了处理最后一个数字, 可以在最后加一个哨兵符号 `+`)
思路1: 用 #栈 来保存中间计算结果 [本质可行性在于, 只需要处理两种优先级]
    上面很倔强没有用什么DS, 造成了变量上的复杂: 因为实际上需要记录二元运算符的两个运算元, 还有因为优先级而需要记录的符号.
    这里用栈记录的优势在哪里呢? 我们可以用栈来记录所有的累加元素; 这样, 遇到乘法的时候, 栈顶就是天然的第一个计算元.
    在下面的代码中, 除了栈结构之外, 仅需要记录当前数字num和之前的运算符preOp: 1) 遇到加减法, 直接将第二个运算元num入栈; 2) 遇到乘除法, 对栈顶元素和num进行乘除运算, 并将结果入栈.
    见 [官答](https://leetcode.cn/problems/basic-calculator-ii/solution/ji-ben-ji-suan-qi-ii-by-leetcode-solutio-cm28/)
note: 注意Python中整除运算是向下取整的, 例如 `-5//3 == -2`. 为了实现题目中「优先乘除」的要求, 除了加括号保障运算元都是正数之外, 下面用了 `int` 实现向零取整.
"""
    def calculateB(self, s: str) -> int:
        # 思路0
        ans = 0
        curr = None # 当前数字 (包括乘除操作之后的结果)
        idx = 0
        flag = 1    # 记录正负号
        mul = None  # 记录乘除法的符号
        s += '+'
        while idx < len(s):
            if s[idx] == ' ':
                idx += 1
                continue
            if s[idx] in '+-':
                ans += flag * curr
                flag = 1 if s[idx] == '+' else -1
                mul = None
                idx += 1
            elif s[idx] in '*/':
                mul = s[idx]
                idx += 1
            else:
                num = 0
                while idx < len(s) and s[idx].isdigit():
                    num = num * 10 + int(s[idx])
                    idx += 1
                # curr 记录当前的数字情况, 方便进行加减法以及乘除法
                if mul == "*":
                    curr *= num
                elif mul == '/':
                    curr //= num
                else:
                    curr = num
        return ans

    def calculateB(self, s: str) -> int:
        # 思路1: 用栈来保存
        stack = []
        preSign = '+'
        num = 0

        for c in s+'/':
            if c.isdigit():
                num = 10*num+int(c)
            elif c in '+-*/':
                if preSign == '+':
                    stack.append(num)
                elif preSign == '-':
                    stack.append(-num)
                elif preSign == '*':
                    stack.append(stack.pop()*num)
                else:
                    # 注意, Python中整除运算是向下取整的!! 下面用int来实现向零取整.
                    # 例如: -5//3 == -2, int(-5/3) == -1
                    stack.append(int(stack.pop()/num))
                num = 0
                preSign = c

        return sum(stack)


    """ 0772. 基本计算器 III #hard 实现 +-*/ 运算, 以及括号
注意: 除法要求「向下截断」, 也即向0取整, 可以采用 `int(a/b)`
    """
    
    
    """ 0150. 逆波兰表达式求值 #medium 
所谓「逆波兰表达式」, 就是 #后缀表达式, 也即运算符在操作数的后面.
    """
    def evalRPN(self, tokens: List[str]) -> int:
        # 思路1: 用栈来保存数字, 遇到运算符就计算
        stack = []
        for t in tokens:
            if t in '+-*/':
                b = stack.pop()
                a = stack.pop()
                if t == '+': stack.append(a+b)
                elif t == '-': stack.append(a-b)
                elif t == '*': stack.append(a*b)
                elif t == '/': stack.append(int(a/b))
            else:
                stack.append(int(t))
        return stack[-1]


    """ 0770. 基本计算器 IV #hardhard #语法分析 实现符号表达式的计算
题目见 [here](https://leetcode.cn/problems/basic-calculator-iv/)
[official](https://leetcode.cn/problems/basic-calculator-iv/solution/basic-calculator-iv-by-leetcode/)
    """
    def basicCalculatorIV(self, expression, evalvars, evalints):
        evalmap = dict(zip(evalvars, evalints))

        def combine(left, right, symbol):
            if symbol == '+': return left + right
            if symbol == '-': return left - right
            if symbol == '*': return left * right
            raise

        def make(expr):
            ans = Poly()
            if expr.isdigit():
                ans.update({(): int(expr)})
            else:
                ans[(expr,)] += 1
            return ans

        def parse(expr):
            bucket = []
            symbols = []
            i = 0
            while i < len(expr):
                if expr[i] == '(':
                    bal = 0
                    for j in range(i, len(expr)):
                        if expr[j] == '(': bal += 1
                        if expr[j] == ')': bal -= 1
                        if bal == 0: break
                    bucket.append(parse(expr[i+1:j]))
                    i = j
                elif expr[i].isalnum():
                    for j in range(i, len(expr)):
                        if expr[j] == ' ':
                            bucket.append(make(expr[i:j]))
                            break
                    else:
                        bucket.append(make(expr[i:]))
                    i = j
                elif expr[i] in '+-*':
                    symbols.append(expr[i])
                i += 1

            for i in range(len(symbols) - 1, -1, -1):
                if symbols[i] == '*':
                    bucket[i] = combine(bucket[i], bucket.pop(i+1),
                                        symbols.pop(i))

            if not bucket: return Poly()
            ans = bucket[0]
            for i, symbol in enumerate(symbols, 1):
                ans = combine(ans, bucket[i], symbol)

            return ans

        P = parse(expression).evaluate(evalmap)
        return P.to_list()



    
sol = Solution()
result = [
    # sol.calculate_template(s = "1 + 1"),
    # sol.calculate_template(s = "(1+(4+5+2)-3)+(6+8)"),
    # sol.calculate_template(" 2-1 + 2 "),
    # sol.calculate_template("1-(     -2)"),
    
    sol.calculate_template("6-4/2"),
    sol.calculate_template(s = "2*(5+5*2)/3+(6/2+8)"),
    
    # sol.calculateB("3+2*2"),
    # sol.calculateB(" 3/2 "),
    # sol.calculateB(" 3+5 / 2 "),
    
    # sol.evalRPN(tokens = ["2","1","+","3","*"]),
    
    sol.basicCalculatorIV(expression = "(e + 8) * (e - 8)", evalvars = [], evalints = []),
    sol.basicCalculatorIV(expression = "e + 8 - a + 5", evalvars = ["e"], evalints = [1]),
]
for r in result:
    print(r)
