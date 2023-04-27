
#%%
class List:
    def __init__(self) -> None:
        self.list = [1,2]
    def __getitem__(self, index):
        return self.list[index]
    

# %%
myL = List()

#%%
2 in myL

# %%
for i in myL:
    print(i)

# %%
bool(myL)

# %%
myL[0]

# %%
