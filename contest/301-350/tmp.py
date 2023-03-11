
#%%
arr = [1,2,43,4]+ [1,2,3]
brr = [3,2,4] 
for a,b in zip(arr,brr):
    print(f"{a} {b}")

# for i in range(len(arr)):
#     print(f"{arr[i]} {brr[i]}")

#%%
zz = zip(arr,brr)
zz[0]
# %%
