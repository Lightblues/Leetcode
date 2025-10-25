
""" 基向量变换矩阵
在线性代数中，同一个向量可以在不同的基下表示。给定 R3 空间中两组基向量 B 和 C，实现一个函数来计算从基 C  到基B 的变换矩阵 P。
[[1, 0, 0], [0, 1, 0], [0, 0, 1]]
[[1, 1, 0], [0, 1, 1], [1, 0, 1]]
> 
[[0.5, -0.5, 0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, 0.5]]
"""
import numpy as np

def transform_basis(B: np.ndarray, C: np.ndarray) -> list:
    m = np.linalg.inv(C) @ B
    return m.tolist()


if __name__ == "__main__":
    B = np.array(eval(input()))
    C = np.array(eval(input()))
    print(transform_basis(B, C))


