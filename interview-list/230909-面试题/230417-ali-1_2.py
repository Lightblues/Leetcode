import torch

# 输入数据
x_data = torch.Tensor([[1.0], [2.0], [3.0]])
y_data = torch.Tensor([[2.0], [4.0], [6.0]])

# 定义模型类
class LinearModel(torch.nn.Module):
    def __init__(self):
        super(LinearModel, self).__init__()
        self.linear = torch.nn.Linear(1, 1)  # 输入维度为1，输出维度为1的线性层
    
    def forward(self, x):
        y_pred = self.linear(x)
        return y_pred

# 实例化模型
model = LinearModel()

# 定义损失函数和优化器
criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 训练模型
num_epochs = 1000
for epoch in range(num_epochs):
    # 前向传播
    y_pred = model(x_data)
    
    # 计算损失
    loss = criterion(y_pred, y_data)
    
    # 反向传播和优化
    optimizer.zero_grad()  # 梯度清零
    loss.backward()  # 反向传播
    optimizer.step()  # 更新参数
    
    # 每隔100次输出一次损失
    if (epoch+1) % 100 == 0:
        print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, loss.item()))

# 预测新数据
x_test = torch.Tensor([[4.0]])
y_test = model(x_test)
print('预测结果: {:.4f}'.format(y_test.item()))

