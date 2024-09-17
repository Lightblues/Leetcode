# %%
""" 
==========================================================================================
                                     Excel Column IDs
"""
def convert_base_excel(n):
    """ print the n-th column name of Excel
    n: int
    """
    result = []
    while n > 0:
        n -= 1 # 每一位都要减1
        n, r = divmod(n, 26)
        result.append(chr(r+ ord('A')))
    return ''.join(result[::-1])

# Print Excel column IDs, `A,B,...Z,AA,AB, ...`
for i in range(704):
    print(convert_base_excel(i), end=" ")
# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC 
# %%


# %%
def convert_base_0(n:int, k:int):
    """ convert n to base k (0-indexed)
    """
    if n == 0: return '0'       # 边界情况
    results = []
    while n > 0:
        n, r = divmod(n, k)
        results.append(str(r))
    return ''.join(results[::-1])
for i in range(30):
    print(convert_base_0(i, 7), end=" ")
# 0 1 2 3 4 5 6 10 11 12 13 14 15 16 20 21 22 23 24 25 26 30 31 32 33 34 35 36 40 41 

# %%
""" 
==========================================================================================
                                     torch basics
"""
from typing import Dict
import torch

# 创建张量
x = torch.tensor([1, 2, 3])
y = torch.ones(2, 3)  # 形状为2x3的全1张量
z = torch.rand(2, 2)  # 形状为2x2的随机张量

# 改变形状
x_reshaped = x.view(3, 1)

# 类型转换
x_float = x.to(torch.float32)

# 索引和切片
first_row = y[0, :]



# %%
""" 
==========================================================================================
                                     loss function
"""
import torch
import torch.nn as nn

class CustomMSELoss(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def forward(self, predicted, target):
        loss = torch.mean((predicted - target) ** 2)
        return loss
    
criterion = CustomMSELoss()
predicted = torch.tensor([1., 2, 4], requires_grad=True)    # 进行grad计算的比如是浮点数 (所以这里写了 1. 而非 1)
target = torch.tensor([1, 2, 3])
loss = criterion(predicted, target)
print(f"Loss: {loss}")
loss.backward()     # 反向传播! 
predicted.grad      # 可以看到grad了! 


# %%
""" 
==========================================================================================
                                     torch tensor & grad
"""
a = torch.tensor([7., 0, 0], requires_grad=True)
b = a + 2
print(b) # tensor([9., 2., 2.], grad_fn=<AddBackward0>)
loss = torch.mean(b * b)

b_ = b.data
b_.zero_()
print(b) # tensor([0., 0., 0.], grad_fn=<AddBackward0>)
 
loss.backward()
print(a.grad) # tensor([0., 0., 0.])
# 其实正确的结果应该是：
# tensor([6.0000, 1.3333, 1.3333])

# %%
... 

b_ = b.detach()
b_.zero_()
print(b) # tensor([0., 0., 0.], grad_fn=<AddBackward0>)
# 储存空间共享，修改 b_ , b 的值也变了
 
loss.backward()
# RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation



# %%
""" 
==========================================================================================
                                     optimizer
"""
import torch
from typing import Iterable, Any, Dict
from torch import Tensor

class CustomSGD(torch.optim.Optimizer):
    def __init__(self, params: Iterable[Tensor] | Iterable[Dict[str, Any]], defaults: Dict[str, Any]) -> None:
        super().__init__(params, defaults)
    def __init__(self, params, lr=0.01):
        # 上面的版本加了类型注释, 这是更简单的写法
        defaults = dict(lr=lr)
        super(CustomSGD, self).__init__(params, defaults)

    def step(self, closure=None):
        loss = None
        if closure is not None:
            loss = closure()
        for group in self.param_groups:     # 注意 Optimizer 类会生成一个 params_groups 的list, 每个gp包括了 lr, params 
            lr = group['lr']                # e.g. lr = 0.1
            for p in group['params']:       # p: torch.Tensor
                if p.grad is None:
                    continue
                p.data = p.data - lr * p.grad
                # p.data.add_(-lr, p.grad)      # 另一种高级写法 (不重要)
        return loss

# %%
p_pred = torch.tensor([1., 2, 3], requires_grad=True)
p_target = torch.tensor([0, 2, 3])
loss = torch.sum((p_pred - p_target) ** 2)   # squared error loss! 它的导数是 2*(p_pred - p_target)
loss.backward()

optimizer = CustomSGD([p_pred], {'lr': 0.1})
optimizer.step()
print(p_pred)       # tensor([0.8000, 2.0000, 3.0000], requires_grad=True)

# %%
# 来看一下我们的 SGD 是否可以学习吧
model = torch.nn.Linear(1, 1) # 创建一个简单的线性模型
optimizer = CustomSGD(model.parameters(), dict(lr=0.1))

inputs = torch.tensor([[1.0], [2.0], [3.0]], requires_grad=True)
targets = torch.tensor([[2.0], [4.0], [6.0]])

criterion = torch.nn.MSELoss()

for epoch in range(100):
    optimizer.zero_grad()  # 清除梯度
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    loss.backward()  # 反向传播
    optimizer.step()  # 更新参数
    print(f'Epoch {epoch+1}, Loss: {loss.item()}')




# %%
""" 
==========================================================================================
                                     k-means
"""
import numpy as np

def kmeans(X, n_clusters, n_iters=100, tolerance=1e-4):
    # X: 输入数据，形状为 [n_samples, n_features]

    # 随机初始化中心点
    # centroids: 中心点，形状为 [n_clusters, n_features]
    centroids = X[np.random.choice(X.shape[0], n_clusters, replace=False)]
    for _ in range(n_iters):
        # 计算距离
        # distances: 每个点到每个中心点的距离，形状为 [n_clusters, n_samples]
        distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
        # 分配簇
        # labels: 每个点的簇标签，形状为 [n_samples,]
        labels = np.argmin(distances, axis=0)
        # 更新中心点
        # new_centroids: 新的中心点，形状为 [n_clusters, n_features]
        new_centroids = np.array([X[labels == k].mean(axis=0) for k in range(n_clusters)])
        # 检查收敛
        if np.linalg.norm(new_centroids - centroids) < tolerance:
            break
        centroids = new_centroids
    return labels, centroids

# X: 形状为 [n_samples, n_features]
X = np.random.rand(100, 2)
labels, centroids = kmeans(X, n_clusters=3)
print("Cluster centroids:\n", centroids)

# %%
""" 
==========================================================================================
                                     numpy basic
"""
a = np.array([[1, 2], [3, 4]])
a.shape                 # (2, 2)

# 在特定位置增加一个轴, 注意到原本为2的话可以在3个位置添加
a[np.newaxis,:,:].shape # (1, 2, 2)
a[:,np.newaxis].shape   # (2, 1, 2) 等价于 a[:,np.newaxis,:].shape
a[:,:,np.newaxis].shape # (2, 2, 1)

# 这里的实际上适合切片操作一起使用了, 参见下面
a[1,np.newaxis].shape   # (1, 2)
a[1,np.newaxis]
# %%

# %%
# 1. 用于广播 broadcasting
a = np.array([1, 2, 3])
b = np.array([[4], [5], [6]])
result = a[np.newaxis, :] + b # (3,3)

# %%
# 2. 保持数组维度一致
a = np.array([[1, 2, 3], [4, 5, 6]])
row_sum = a.sum(axis=1)[:, np.newaxis]  # 把第1个维度 (从0开始) 聚合掉了, 通过 newaxis 来还原
row_sum # (2,1)

# %%
# 3. 与切片操作结合使用
a = np.array([[1, 2, 3], [4, 5, 6]])
selected = a[0, np.newaxis, 1:3]    # 等价于 a[[0],1:3]
print(selected) # (1,2)


# %%
# 4. 用在高级索引中
a = np.array([[1, 2, 3], [4, 5, 6]])        # 例如, 我们要取出 第 0,1 行, 第 1,2 列
rows = np.array([0, 1])
cols = np.array([1, 2])

selected = a[rows[:, np.newaxis], cols]     # 注意到对于第0个索引是需要增加一个轴的
print(selected)     # (2,2)
a[rows, cols]       # (2) 区别于这种 a[list, list] 的索引方式, 结果是一个list!

# %%

# %%
nn.Sigmoid