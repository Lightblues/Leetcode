import pstats
from pstats import SortKey
p = pstats.Stats('restats')
p.strip_dirs().sort_stats(-1).print_stats()

p.sort_stats(SortKey.NAME)
p.print_stats()

p.sort_stats(SortKey.CUMULATIVE).print_stats(10)

p.print_callees()
p.add('restats')