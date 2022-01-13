import heapq
import random

# ============== heap =============
# (a.k.a. priority queue)
random.seed(1)
heap = [random.randint(0, 10) for i in range(10)]
print(heap)
# heapify
heapq.heapify(heap)
print(heap)
# heappop
minNow = heapq.heappop(heap)
print(minNow, heap)
# heappush
heapq.heappush(heap, 11)
print(heap)




