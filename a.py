
#%%
import torch

a = torch.tensor([1, 2, 3])
n = a.shape[0]
A = torch.tile(a.squeeze(0), (n,1))
A = torch.cumsum(A, dim=1)
A = torch.tril(A)
A

# %%
# 计算 KG 上的 triplet_loss
def triplet_loss(positive_triplets, negative_triplets, margin):
    positive_s, positive_p, positive_o = positive_triplets
    negative_s, negative_p, negative_o = negative_triplets

    # 计算正样本和负样本之间的距离. 
    positive_distance = torch.norm(positive_s - positive_p - positive_o, dim=1)
    negative_distance = torch.norm(negative_s - negative_p - negative_o, dim=1)

    # 计算损失
    losses = torch.relu(positive_distance - negative_distance + margin)
    loss = torch.mean(losses)

    return loss