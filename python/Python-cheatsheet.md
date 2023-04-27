## Base Python

```python
# list methods
myList.index()
myList.count(a)
myList.append(a)
myList.remove(a)
del(myList[:3])
myList.reverse()    # 反转
myList.extend(l)
myList.pop(-1)
myList.index(0, a)
myList.sort()

# string
s.upper()
s.count('w')
s.replace('e', 'i')
```

## numpy

```python
np.arange(10,25,5)  # 等间隔
np.linspace(0,2,9)
np.full((2,2), 7) # 常数
np.eye(4)

np.random.random((2,2))
np.zeros((2,2))
np.ones((2,2,), dtype=np.int16)
np.empty((2,2)) # 空数组
```

输入输出

```python
np.save('my_array', a)
np.savez('array.npz', a,b)
np.load('my_array.npy')

np.loadtxt('a.txt')
np.genfromtxt('a.csv', delimiter=',')
np.savetxt('a.csv', a, delimiter=',')
```

数组信息

```python
a.shape
len(a)
a.ndim
a.size # 有多少元素
a.dtype
a.dtype.name
a.astype(int)
```

聚合函数

```python
a.max(axis=0)
a.cumsum(axis=1)
a.median()  # 中位数

a.corrcoef() # 相关系数
np.std(b) # 标准差
```

数组复制

```python
h = a.view() # 使用同一数据创建数组视图
np.copy(a) 
```

数组索引

```python
# 条件索引
a[a<2]

# 花式索引
a[[1,0,1], [2,1,0]]
```

数组操作

```python
np.transpose(a)
a.T

a.ravel() # 拉平数组
a.reshape(3, -1)

a.resize((2,6)) # 返回形状为 (2,6) 的新数组
np.append(h,g)
np.insert(a, 1,5)
np.delete(a, [1])

# 合并
np.concatenate((a,b), axis=0)
np.vstack((a,b)) # 横向堆叠
np.r_[a,b]
np.hstack((a,b)) # 纵向堆叠
np.column_stack((a,b))
np.c_[a,b]

# 分割
np.hsplit(a,3) # 纵向 三等分
np.vsplit(a,2) # 横向
```

## Matplotlib

## Scikit-learn

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=1)
```

预处理

```python
# 标准化
from sklearn.preprocessing import StandardScaler

# 归一化
from sklearn.preprocessing import Normalizer
scaler = Normalizer().fit(X_train)
standardized_X_train = scaler.transform(X_train)
standardized_X_test = scaler.transform(X_test)

# 二值化
from sklearn.preprocessing import Binarizer

# 编码分类特征
from sklearn.preprocessing import LabelEncoder
enc = LabelEncoder()
y = enc.fit_transform(y)

# 输入缺失值
from sklearn.preprocessing import Imputer
imp = Imputer(missing_value=0, strategy='mean', axis=0)
imp.fit_transform(X_train)

# 生成多项式特征
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(5)
ploy.fit_transform(X)
```

评估模型性能

```python
# 分类指标
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
confusion_matrix(y_test, y_pred)

# 回归指标
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score # R^2

# 群集指标
from sklearn.metrics import adjusted_rand_score # 调整兰德系数
from sklearn.metrics import homogeneity_score # 同质性
from sklearn.metrics import v_measure_score

# 交叉验证
from sklearn.cross_validation import cross_val_score
```

模型调整

```python
# 栅格搜索
from sklearn.grid_search import GridSearchCV
params = {
    "n_neighbors": np.arange(1,3), 
    "metric": ['euclidean', 'cityblock']
}
grid = GridSearchCV(estimator=knn, param_grid=params)
grid.fit(X_train, y_train)

grid.best_score_
grid.best_estimator_.n_neighbors

# 随机参数优化

from sklearn.grid_search import RandomizedSearchCV

```
