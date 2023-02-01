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
https://oi-wiki.org/string/automaton/

Easonsi @2023 """
class Solution:

    """ 0008. 字符串转换整数 (atoi) #medium #题型. 要求 1] 去除前导空格; 2] 识别 +/-; 3] 前导0; 4] int边界
思路1: #正则 去除前导空格后 '^[\+\-]?\d+' 识别
思路2: #状态机
    状态空间: start; signed; in_number; end
[官答](https://leetcode.cn/problems/string-to-integer-atoi/solution/zi-fu-chuan-zhuan-huan-zheng-shu-atoi-by-leetcode-/)
"""
    def myAtoi(self, s: str) -> int:
        v = int(*re.findall('^[\+\-]?\d+', s.lstrip()))
        return max(min(v, 2**31 - 1), -2**31)
    
    def myAtoi(self, str: str) -> int:
        INT_MAX = 2 ** 31 - 1
        INT_MIN = -2 ** 31

        class Automaton:
            def __init__(self):
                self.state = 'start'
                self.sign = 1
                self.ans = 0
                self.table = {
                    'start': ['start', 'signed', 'in_number', 'end'],
                    'signed': ['end', 'end', 'in_number', 'end'],
                    'in_number': ['end', 'end', 'in_number', 'end'],
                    'end': ['end', 'end', 'end', 'end'],
                }
            def get_col(self, c):
                # 状态转移表的四列分别表遇到了 ' '; +/-; number; other
                if c.isspace():
                    return 0
                if c == '+' or c == '-':
                    return 1
                if c.isdigit():
                    return 2
                return 3
            def get(self, c):
                self.state = self.table[self.state][self.get_col(c)]
                if self.state == 'in_number':
                    self.ans = self.ans * 10 + int(c)
                    self.ans = min(self.ans, INT_MAX) if self.sign == 1 else min(self.ans, -INT_MIN)
                elif self.state == 'signed':
                    self.sign = 1 if c == '+' else -1

        automaton = Automaton()
        for c in str:
            automaton.get(c)
        return automaton.sign * automaton.ans

    """ 0065. 有效数字 #hard 判断一个字符串是否为有效数组, 见 https://leetcode.cn/problems/valid-number/
规则: 可以有前导0
    小数: 1] 可选 +/-; 2] 至少一个点, 不能前后都为空 (至少一侧有数字)
    整数: 1] 可选 +/-; 2] 至少一个数字
    科学计数: 在上面的规则下, 后面可以接 E/e+整数表示科学计数法 
思路1: #自动机 太复杂了
    状态空间: 开始、符号、数字、小数点、前无数字的小数点、尾数（STATE_FRACTION）、e 符号、指数符号位、指数数字
    [官答](https://leetcode.cn/problems/valid-number/solution/you-xiao-shu-zi-by-leetcode-solution-298l/)
思路2: #正则 [here](https://leetcode.cn/problems/valid-number/solution/zheng-ze-biao-da-shi-jie-ti-by-xiao-bai-njjst/)
    按照上述规则: 整数 '^[+-]?\d+'; 小数 '^[+-]?\d+\.\d+$','^[+-]?\.\d+$','^[+-]?\d+\.$'
    合并上面的几个表达, 判断整数/小数 ^[+-]?((\d+\.?)|(\d*\.\d+))$
    再加入科学计数法: ^[+-]?((\d+\.?)|(\d*\.\d+))([eE][+-]?\d+)?$
思路3: 字符串 #大模拟
    根据 e/E 分割, 然后判断小数/整数
    见 [三叶](https://leetcode.cn/problems/valid-number/solution/gong-shui-san-xie-zi-fu-chuan-mo-ni-by-a-7cgc/)
"""
    def isNumber(self, s: str) -> bool:
        # 思路2: #正则
        return re.match('^[+-]?((\d+\.?)|(\d*\.\d+))([eE][+-]?\d+)?$', s) != None

    def isNumber(self, s: str) -> bool:
        from enum import Enum
        State = Enum("State", [
            "STATE_INITIAL",
            "STATE_INT_SIGN",
            "STATE_INTEGER",
            "STATE_POINT",
            "STATE_POINT_WITHOUT_INT",
            "STATE_FRACTION",
            "STATE_EXP",
            "STATE_EXP_SIGN",
            "STATE_EXP_NUMBER",
            "STATE_END",
        ])
        Chartype = Enum("Chartype", [
            "CHAR_NUMBER",
            "CHAR_EXP",
            "CHAR_POINT",
            "CHAR_SIGN",
            "CHAR_ILLEGAL",
        ])

        def toChartype(ch: str) -> Chartype:
            if ch.isdigit():
                return Chartype.CHAR_NUMBER
            elif ch.lower() == "e":
                return Chartype.CHAR_EXP
            elif ch == ".":
                return Chartype.CHAR_POINT
            elif ch == "+" or ch == "-":
                return Chartype.CHAR_SIGN
            else:
                return Chartype.CHAR_ILLEGAL

        transfer = {
            State.STATE_INITIAL: {
                Chartype.CHAR_NUMBER: State.STATE_INTEGER,
                Chartype.CHAR_POINT: State.STATE_POINT_WITHOUT_INT,
                Chartype.CHAR_SIGN: State.STATE_INT_SIGN,
            },
            State.STATE_INT_SIGN: {
                Chartype.CHAR_NUMBER: State.STATE_INTEGER,
                Chartype.CHAR_POINT: State.STATE_POINT_WITHOUT_INT,
            },
            State.STATE_INTEGER: {
                Chartype.CHAR_NUMBER: State.STATE_INTEGER,
                Chartype.CHAR_EXP: State.STATE_EXP,
                Chartype.CHAR_POINT: State.STATE_POINT,
            },
            State.STATE_POINT: {
                Chartype.CHAR_NUMBER: State.STATE_FRACTION,
                Chartype.CHAR_EXP: State.STATE_EXP,
            },
            State.STATE_POINT_WITHOUT_INT: {
                Chartype.CHAR_NUMBER: State.STATE_FRACTION,
            },
            State.STATE_FRACTION: {
                Chartype.CHAR_NUMBER: State.STATE_FRACTION,
                Chartype.CHAR_EXP: State.STATE_EXP,
            },
            State.STATE_EXP: {
                Chartype.CHAR_NUMBER: State.STATE_EXP_NUMBER,
                Chartype.CHAR_SIGN: State.STATE_EXP_SIGN,
            },
            State.STATE_EXP_SIGN: {
                Chartype.CHAR_NUMBER: State.STATE_EXP_NUMBER,
            },
            State.STATE_EXP_NUMBER: {
                Chartype.CHAR_NUMBER: State.STATE_EXP_NUMBER,
            },
        }

        st = State.STATE_INITIAL
        for ch in s:
            typ = toChartype(ch)
            if typ not in transfer[st]:
                return False
            st = transfer[st][typ]

        return st in [State.STATE_INTEGER, State.STATE_POINT, State.STATE_FRACTION, State.STATE_EXP_NUMBER,
                      State.STATE_END]
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
