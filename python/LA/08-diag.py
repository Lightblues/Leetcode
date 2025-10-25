import numpy as np

def make_diagonal(x):
    x = np.array(x, dtype=float)
    return np.diag(x)
    
    
if __name__ == "__main__":
    x = np.array(eval(input()))
    print(make_diagonal(x))
