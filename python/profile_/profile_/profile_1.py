
""" 利用profile包来检查函数的性能
doc: https://docs.python.org/3/library/profile.html
- cProfile/profile: 用于检查函数的性能
- pstats: 用于分析结果

不同的使用方式:
1] 直接在代码里面, 通过 cProfile.run('func()') 来运行
    也可以指定保存的文件名, cProfile.run('func()', 'restats')
2] 通过命令行, python -m cProfile -o restats *.py 生成
    1) 然后可以 python -m pstats restats 来查看结果 (help 查看帮助)
    2) 也可以通过 p = pstats.Stats('restats') 来查看结果, 见 [pstats_1.py]
另见 [line_profiler](https://github.com/pyutils/line_profiler)
"""

import cProfile, profile, pstats
import re
# 1] 直接 .run
# cProfile.run('re.compile("foo|bar")')

# 2] 可以设置一个文件名, 保存结果
cProfile.run('re.compile("foo|bar")', 'restats')
# 然后 

# 3] 也可以, python -m cProfile -o restats test.py
