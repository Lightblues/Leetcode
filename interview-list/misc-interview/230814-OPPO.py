""" 
要求实现 SelfAttention, 之后问了attention的优化方案. 
"""
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn import Module


class SelfAttention(Module):
    def __init__(self, hdim=128, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.hdim = hdim
        self.Wq = nn.Linear(hdim, hdim)
        self.Wk = nn.Linear(hdim, hdim)
        self.Wv = nn.Linear(hdim, hdim)
        self.Wo = nn.Linear(hdim, hdim)
    
    def forward(self, x):
        q,k,v = self.Wq(x), self.Wk(x), self.Wv(x)
        att = torch.matmul(q, k.T) / (self.hdim**0.5)
        att = F.softmax(att, dim=-1)
        o = torch.matmul(att, v)
        return o

