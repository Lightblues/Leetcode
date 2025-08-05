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
1. and 语法: 对于命题 P ∧ Q, 可以用 h.left 来引用 P, 用 h.right 来引用 Q
  /-- Suppose $x \in A$ and $x \in B$.  Then $x \in A$. -/
  Statement (x : U) (A B : Set U) (h : x ∈ A ∧ x ∈ B) : x ∈ A := by
    exact h.left
2. mem_inter_iff 语法: 对于命题 x ∈ A ∩ B, 可以用 mem_inter_iff 来将其转换为 x ∈ A ∧ x ∈ B
  /-- Suppose $x \in A ∩ B$.  Then $x \in B$. -/
  Statement (x : U) (A B : Set U) (h : x ∈ A ∩ B) : x ∈ B := by
    Hint "To start on this proof, try writing out the meaning of intersection in `h`."
    rewrite [mem_inter_iff] at h
    Hint "Now your situation is similar to the previous level."
    exact h.right
3. 应用: 之前提到的 intro 语法
  /-- For any sets $A$ and $B$, $A \cap B \subseteq A$. -/
  Statement (A B : Set U) : A ∩ B ⊆ A := by
    Hint (hidden := true) "Since the goal is a subset statement, you should start by
    introducing an object `x` and the assumption that `x ∈ A ∩ B`."
    intro x h
    rewrite [mem_inter_iff] at h
    exact h.left
4. 证明 and 形式的命题: `And.intro` 语法
  /-- Suppose $x \in A$ and $x \in B$.  Then $x \in A \cap B$. -/
  Statement (x : U) (A B : Set U) (h1 : x ∈ A) (h2 : x ∈ B) : x ∈ A ∩ B := by
    Hint "Writing out the meaning of intersection in the goal will help you see what to do to
    complete this level."
    rewrite [mem_inter_iff]
    Hint "Now you can use `And.intro` to prove the goal."
    Hint (hidden := true) "`exact And.intro h1 h2` will close the goal."
    exact And.intro h1 h2
5. 应用: 证明集合之间的属于. #remark 除了使用 `intro` 来引入新的命题, 也可以用 `apply` 语法来对于 Goal 进行变换, 例如这里倒数第三步
  /-- Suppose $A \subseteq B$ and $A \subseteq C$.  Then $A \subseteq B \cap C$. -/
  Statement (A B C : Set U) (h1 : A ⊆ B) (h2 : A ⊆ C) : A ⊆ B ∩ C := by
    intro x h3
    Hint "Writing out the definition of intersection in the goal will help."
    rewrite [mem_inter_iff]
    Hint "If you had `hB : {x} ∈ B` and `hC : {x} ∈ C`, then `And.intro hB hC`
    would prove the goal.  So there are two ways to proceed.  One possibility is to use
    `have` to introduce the assumptions `{x} ∈ B` and `{x} ∈ C`--that is, if you can see
    how to justify those statements!  Then you can use `And.intro` to prove the goal.
    The second possibility is to use the `apply` tactic.  Recall that if you write
    `apply And.intro`, then Lean will figure out that the
    theorem `And.intro` could be applied to prove the goal, if only you had proofs of
    `{x} ∈ B` and `{x} ∈ C`.  So it will set those two statements as goals, to be proven
    one after the other."
    apply And.intro
    Hint "Your immediate goal now is to prove that `{x} ∈ B`.  Once you close that goal,
    you'll be asked to prove the second goal, `{x} ∈ C`."
    exact h1 h3
    exact h2 h3
6. 交换律: inter_subset_swap. 也即 A ∩ B ⊆ B ∩ A
  /-- For any sets $A$ and $B$, $A \cap B \subseteq B \cap A$. -/
  Statement inter_subset_swap (A B : Set U) : A ∩ B ⊆ B ∩ A := by
    intro x h
    Hint (hidden := true) "It will help you see how to proceed if you
    write out the definition of intersection in both the assumption {h} and the goal.
    Using the `rewrite` tactic isn't necessary; you can just do the rewriting in
    your head rather than asking Lean to do it.  But if it helps you to figure out the
    proof, go ahead and use the `rewrite` tactic."
    rewrite [mem_inter_iff]
    rewrite [mem_inter_iff] at h
    Hint (hidden := true) "Now `And.intro {h}.right {h}.left` proves the goal."
    exact And.intro h.right h.left
7. 等价性 (inter_comm): 这里用到了 Subset.antisymm 来证明集合相等. #remark 注意下面 `exact` 语法需要指定参数
  /-- For any sets $A$ and $B$, $A \cap B = B \cap A$. -/
  Statement inter_comm (A B : Set U) : A ∩ B = B ∩ A := by
    apply Subset.antisymm
    exact inter_subset_swap A B
    exact inter_subset_swap B A
8. 结合律: inter_assoc. 引入 `ext x` 来证明集合相等.
  #remark 另外, 注意到对于 h: x ∈ A ∧ x ∈ B ∩ C, 其外层包含两个命题, 而对于 h.right 根据交集的定义, 其也是一个And命题, 因此 h.right.left 其实就是 x ∈ B
  /-- For any sets $A$, $B$, and $C$, $(A \cap B) \cap C = A \cap (B \cap C)$. -/
  Statement inter_assoc (A B C : Set U) : (A ∩ B) ∩ C = A ∩ (B ∩ C) := by
    Hint "Notice that Lean has written the goal as `A ∩ B ∩ C = A ∩ (B ∩ C)`, with no
    parentheses on the left.  When an intersection of more than two sets is written
    without parentheses, Lean groups the intersections to the left, so this means
    `(A ∩ B) ∩ C = A ∩ (B ∩ C)`.
    To start this proof, use the tactic `ext x`."
    ext x
    Hint "Notice that Lean has introduced the new object `{x} : U` into the proof, and
    your goal is now `{x} ∈ A ∩ B ∩ C ↔ {x} ∈ A ∩ (B ∩ C)`.  Proving this goal will show that
    `A ∩ B ∩ C` and `A ∩ (B ∩ C)` have exactly the same elements, and by the principle of
    extensionality, that will show that the sets are equal."
    Hint (hidden := true) "Since your goal is an \"if and only if\" statement, a good next step
    is `apply Iff.intro`."
    apply Iff.intro
    Hint (hidden := true) "Since your goal is an \"if-then\" statement, a good next step
    is `intro h1`."
    intro h1
    rewrite [mem_inter_iff]
    rewrite [mem_inter_iff] at h1
    Hint (strict := true) (hidden := true) "If you're stuck at this point,
    it may help you see how to proceed if you separate
    out the first half of `{h1}` as a separate assumption.
    You can do this with `have hAB : {x} ∈ A ∩ B := {h1}.left`."
    have hAB : x ∈ A ∩ B := h1.left
    rewrite [mem_inter_iff] at hAB
    apply And.intro
    exact hAB.left
    exact And.intro hAB.right h1.right
    intro h1
    apply And.intro
    exact And.intro h1.left h1.right.left
    exact h1.right.right


# 总结语法
1. intro
  - 对于 P → Q 使用 intro 语法, 可以引入假定 P
  - 对于 ∀ x, P x 形式的命令, 可以引入 x, 例如证明集合的属于关系
2. apply: 反向变换goal
  - 对于 Goal 进行变换, 例如对于 P ∧ Q, 可以用 apply And.intro 来将 Goal 转换为 P 和 Q 两个子 Goal
3. exact: 直接符合定义
  注意 exact 语法也需要参数, 例如 exact inter_subset_swap A B
4. rewrite: 重写一个命题, 例如 mem_inter_iff
5. ext: 对于目标 A = B, 可以用 ext x 来将其变为 x ∈ A ↔ x ∈ B 的形式
-/
