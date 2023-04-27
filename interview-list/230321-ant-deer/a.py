#%%
import heapq

q = [7,11,23,32,16,9,12,45,27]
q = [-i for i in q]
heapq.heapify(q)
q = [-i for i in q]
print(q)

# %%
