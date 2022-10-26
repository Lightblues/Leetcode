#%%
""" 
变量并不直接存储值，而是存储值的引用。Python调用函数时，实参到形参都是传递的引用。
"""
nums = [1,2]
def swap(arr: list):
    arr.reverse()
print(f"nums before: {nums}")
swap(nums)
print(f"nums after: {nums}")

# %%
