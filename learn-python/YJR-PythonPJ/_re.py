
#%%
import re
pat = r"([^,、.有\s]+?)大学"
text = "参加的大学生来自复旦大学、清华大学、中国科技大学还有北京大学等多所大学。"
t = re.findall(pat, text)
print(t[1])

# %%
t
# %%
