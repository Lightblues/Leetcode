""" 
https://www.nowcoder.com/exam/test/92587083/detail?pid=60890580
"""

import sys
import math

for line in sys.stdin:
    n = int(line)
    print(f"{1 / math.comb(n,2):.10f}")