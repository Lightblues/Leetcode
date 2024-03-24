#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 从 binorm(0, 1, 0.5) 中抽取 1000 个样本, 绘制直方图
p = 0.3
x = np.random.binomial(1, p, 1000)
plt.hist(x)
mean_, std_ = x.mean(), x.std()
print(f"p: {p}: mean: {mean_}, std: {std_}")

# %%
# 每次从 binorm(0, 1, 0.5) 中抽取 1000 个样本, 计算均值, 重复 1000 次, 绘制直方图
x = np.random.binomial(1, p, (1000, 1000))
x = x.mean(axis=0)
plt.hist(x)
# 绘制均值方差为 (mean_, std_) 的正态分布曲线
# mean_, std_ = x.mean(), x.std()
y = np.random.normal(mean_, std_, 1000)
plt.hist(y, density=False)
plt.hist(x)

# %%
from scipy import stats as sts  
data =  [2,23,4,17,12,12,13,16]
print(sts.scoreatpercentile(data,25)) #25分位数
print(sts.scoreatpercentile(data,75)) #75分位数

# %%
from scipy import stats
import scipy.stats
import numpy as np
import pandas  as pd
import statsmodels
import statsmodels.stats.weightstats

data = [493.01,498.83,494.16,500.39,497.63,499.72,493.41,498.97,501.94,503.45,497.47,494.19,500.99,495.81,499.63,494.91,498.90,502.43,491.34,497.50,505.95,496.56,501.66,492.02,497.68,493.48,505.40,499.21,505.84,499.41,505.65,500.51,489.53,496.55,492.26,498.91,496.65,496.38,497.16,498.91,490.98,499.97,501.21,502.85,494.35,502.96,506.21,497.66,504.66,492.11]
z, pval = statsmodels.stats.weightstats.ztest(data, value=500, alternative = 'smaller')
print(z,pval)
# %%
