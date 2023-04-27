
## 3 高维正态分布KL散度

见苏神 [两个多元正态分布的KL散度、巴氏距离和W距离](https://kexue.fm/archives/8512)

对于两个连续的正态分布, 它们KL散度 $D_{K L}(p \| q)=\int p(x) \log_{q(x)}^{p(x)} d x$
对于两个正态分布 $\mathcal{N}\left(\boldsymbol{\mu}_p, \Sigma_p\right)$ 和 $\mathcal{N}\left(\boldsymbol{\mu}_q, \Sigma_q\right)$, 可以通过简单的运算得知他们的 $K L$ 散度为 
$$
D_{K L}(p \| q)={ }_2^1\left[\log \left|\Sigma_q\right| / \left|\Sigma_p\right| -k+\left(\boldsymbol{\mu}_p-\boldsymbol{\mu}_q\right)^T \Sigma_q^{-1}\left(\boldsymbol{\mu}_p-\boldsymbol{\mu}_q\right)+\operatorname{tr}\left\{\Sigma_q^{-1} \Sigma_p\right\}\right]
$$,
其中|·|表示矩阵的行列式, $\operatorname{tr}(\cdot)$ 表示矩阵对角线元素求和, $\log$ 以自然对数 $=$ 为底。
现在给定其中一个正态分布 $\mathrm{q}$ 为 $\mathcal{N}(\mathbf{0}, I)$, 另一个分布 $\mathrm{p}$ 为 $\mathcal{N}\left(\mathbf{0}, \Sigma_p^{\prime}\right)$ ， $\Sigma_p^{\prime}$ 是一个 $\mathrm{k}$ 阶对角阵，试判断这两个正态分布的 $K L$ 散度 $D_{K L}(p \| q)$ 是否大于给定阈们

限制: 每组测试 (k,t) k 矩阵维度 1e3; t 阈值 1e5

思路1: 化简 根据上面的交叉熵公式, 可以化简得到: 
    KL = 1/2 * [-log|prod{pi}| + sum{pi}]
