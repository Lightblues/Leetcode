""" 统计文本中出现的数字, 求和. """

#%% 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#%%
s = r"""
$$
\begin{aligned}
&25.9 \mathrm{MB} \\
&\hline 27.5 \mathrm{MB} \\
&\hline 26.1 \mathrm{MB} \\
&\hline 25.8 \mathrm{MB} \\
&\hline 18.9 \mathrm{MB} \\
&\hline 26.1 \mathrm{MB} \\
&\hline 26.3 \mathrm{MB} \\
&\hline 26.3 \mathrm{MB} \\
&\hline 28.0 \mathrm{MB} \\
&\hline 60.8 \mathrm{MB} \\
&\hline 18.7 \mathrm{MB} \\
&\hline 15.5 \mathrm{MB} \\
&\hline 9.5 \mathrm{MB} \\
&\hline 10.2 \mathrm{MB} \\
&\hline 57.5 \mathrm{MB}
\end{aligned}
$$
"""

#%%
import re

res = re.findall(r'[\d+\.]+', s)
print(sum([float(r) for r in res]))


# %%
loveLin = "100 years"


# %%
print(loveLin)
# %%
