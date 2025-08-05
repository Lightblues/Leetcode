/- https://github.com/djvelleman/STG4/
https://adam.math.hhu.de/#/g/djvelleman/stg4
Set Theory Game

# 符号表
\in \mem    ∈
\sub    ⊆
\imp    →
\iff    ↔
\not    ¬
\^c \comp ᶜ
\and ∧
\inter \cap ∩

# tactics
U: Type
x: U
A: Set U
h: x ∈ A

exact h1 h2
have h3: x ∈ B := h1 h2
intro h

by_contra h
rfl 的英文为 reflexivity
x ∉ A 的意思是 x ∈ A → False
-/


/-
# 1) Subset
notes:
1. 类型 & 证明 (imply)
2. intro 语法
  - 对于 P → Q 使用 intro 语法, 可以引入假定 P
  - 对于 ∀ x, P x 形式的命令, 可以引入 x, 例如证明集合的属于关系

https://github.com/djvelleman/STG4/blob/main/Game/Levels/Subset

-- exact: 直接符合定义
Statement (x : U) (A : Set U) (h : x ∈ A) : x ∈ A := by
  exact h
-- exact 连续使用
Statement (x : U) (A B : Set U) (h1 : A ⊆ B) (h2 : x ∈ A) : x ∈ B := by
  exact h1 h2
-- Suppose $A \subseteq B$, $B \subseteq C$, and $x \in A$.  Then $x \in C$.
Statement (x : U) (A B C : Set U)
  (h1 : A ⊆ B) (h2 : B ⊆ C) (h3 : x ∈ A) : x ∈ C := by
    have h4 : x ∈ B := h1 h3
    exact h2 h4
-/


/-
# 2) Complement
notes:
1. 反证法: 利用 by_contra 来引入反命题
  例如, 对于命题 ¬A ⊆ B, 可以用 by_contra h3 来引入的反命题 A ⊆ B, 然后证明 False 即可
2. push_neg 语法, 对于 ¬ ¬ P 形式的命令, 可以简化为 P
  例如, 对于对于命题 x ∈ Aᶜᶜ, 应用一次 [mem_compl_iff] 得到 x ∉ Aᶜ 也即 ¬ x ∈ Aᶜ;
    再应用一次 [mem_compl_iff] 得到 ¬ x ∉ A 实际上是 ¬¬ x ∈ A
    此时可以使用 push_neg 来简化为 x ∈ A
  * `¬¬P` is converted to `P`.
  * `¬(P ∨ Q)` is converted to `¬P ∧ ¬Q`.
  * `¬(P ∧ Q)` is converted to `P → ¬Q`.
  * `¬(P → Q)` is converted to `P ∧ ¬Q`.
  * `¬∀ x, P x` is converted to `∃ x, ¬P x`.
  * `¬∃ x, P x` is converted to `∀ x, ¬P x`.
3. 如何证明一个 iff 的命题?
  逻辑上, iff 就是 = 等于! 例如 x ∈ Aᶜ ↔ x ∉ A 这个命题, 其实就是补集的定义, 因此可用 rfl 来得到证明

https://github.com/djvelleman/STG4/blob/main/Game/Levels/Comp/

-- Suppose $x \in A$ and $x \notin B$.  Then $\neg A \subseteq B$.
Statement {A B : Set U} {x : U} (h1 : x ∈ A) (h2 : x ∉ B) : ¬A ⊆ B := by
  by_contra h3
  have h4 : x ∈ B := h3 h1
  exact h2 h4
-/


/-
# 3) Intersection

-/
