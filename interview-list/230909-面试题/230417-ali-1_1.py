""" 
鹿儿被问到的题目, 用基本的numpy实现梯度下降的线性回归! 来自GPT生成的结果

"""

import numpy as np

# 输入数据
x_data = np.array([[1.0], [2.0], [3.0]])
y_data = np.array([[2.0], [4.0], [6.0]])

# 定义模型函数
def linear_model(x, w, b):
    return np.dot(x, w) + b

# 定义损失函数
def loss_function(y_pred, y_true):
    return np.mean(np.square(y_pred - y_true))

# 初始化模型参数
w = np.array([[0.0]])
b = np.array([0.0])

# 定义学习率和训练次数
learning_rate = 0.01
num_epochs = 1000

# 模拟梯度下降
for epoch in range(num_epochs):
    # 前向传播
    y_pred = linear_model(x_data, w, b)
    
    # 计算损失
    loss = loss_function(y_pred, y_data)
    
    # 反向传播和更新参数
    dw = np.dot(x_data.T, (y_pred - y_data)) / x_data.shape[0]
    db = np.mean(y_pred - y_data)
    w -= learning_rate * dw
    b -= learning_rate * db
    
    # 每隔100次输出一次损失
    if (epoch+1) % 100 == 0:
        print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, loss))

# 预测新数据
x_test = np.array([[4.0]])
y_test = linear_model(x_test, w, b)
print('预测结果: {:.4f}'.format(y_test[0][0]))
