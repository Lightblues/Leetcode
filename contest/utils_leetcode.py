import sys, os

class testClass:
    """ 用于接受 ACM 形式的测试用例, 例如
    ["ATM", "deposit", "withdraw", "deposit", "withdraw", "withdraw"]
    [[], [[0,0,1,2,1]], [600], [[0,1,0,1,1]], [600], [550]]
    """
    def testClass(self, inputs):
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res


""" 用于读取stdin输入 """
try:
    while True:
        line = sys.stdin.readline().strip()
        if line == '':
            break
        lines = line.split()
        print(int(lines[0]) + int(lines[1]))
except:
    pass