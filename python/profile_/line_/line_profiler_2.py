""" 
1] LineProfiler. 自定义一个LineProfiler, 然后add_function/lp
2] 通过 @profile 装饰器, 
    `kernprof -l -v line_profiler_2.py` 可以得到 *.py.lprof 文件. 因为加了 -v 也直接输出答案.
    python -m line_profiler *.py.lprof 对于保存的结果可以这样查看!
"""

from line_profiler import LineProfiler, profile
import random

@profile
def do_other_stuff(numbers):
    s = sum(numbers)

@profile
def do_stuff(numbers):
    do_other_stuff(numbers)
    l = [numbers[i]/43 for i in range(len(numbers))]
    m = ['hello'+str(numbers[i]) for i in range(len(numbers))]

numbers = [random.randint(1,100) for i in range(1000)]
# lp = LineProfiler()
# lp.add_function(do_other_stuff)   # add additional function to profile
# lp_wrapper = lp(do_stuff)
# lp_wrapper(numbers)
# lp.print_stats()
do_stuff(numbers)