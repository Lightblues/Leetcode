def testClass(inputs):
    """ 用于接受 ACM 形式的测试用例, 例如
["ATM", "deposit", "withdraw", "deposit", "withdraw", "withdraw"]
[[], [[0,0,1,2,1]], [600], [[0,1,0,1,1]], [600], [550]]
"""
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])()
    for method_name, arg in list(zip(methods, args))[1:]:
        print(getattr(class_name, method_name)(*arg))