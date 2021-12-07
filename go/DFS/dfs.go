package main

import "math"

func max(a,b int) int{
	if a>b {return a}
	return b
}
func min(a,b int) int{
	if a<b {return a}
	return b
}
func abs(x int) int{
	if x>0 {return x}
	return -x
}

// TreeNode node type
type TreeNode struct {
	Val int
	Left *TreeNode
	Right *TreeNode
}
// func list2tree(nums []int) TreeNode {
// 	for 
// }

// =================== DFS ===================================
/* 0094.Binary-Tree-Inorder-Traversal/ 中序遍历一颗二叉树
Given a binary tree, return the inorder traversal of its nodes’ values.
Input: [1,null,2,3]
   1
    \
     2
    /
   3

Output: [1,3,2] */
func inorderTraversal(root *TreeNode) []int {
	result := []int{}
	inorder(root, &result)
	return result
}
func inorder(root *TreeNode, output *[]int) {
	if root!=nil {
		inorder(root.Left, output)
		*output = append(*output, root.Val)
		inorder(root.Right, output)
	}
}

/* 0098.Validate-Binary-Search-Tree/
Given a binary tree, determine if it is a valid binary search tree (BST).
Assume a BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node’s key.
- The right subtree of a node contains only nodes with keys greater than the node’s key.
- Both the left and right subtrees must also be binary search trees. 
    5
   / \
  1   4
     / \
    3   6

Input: [5,1,4,null,null,3,6]
Output: false
Explanation: The root node's value is 5 but its right child's value is 4.*/
func isValidBST(root *TreeNode) bool {
	return isValidbst(root, math.Inf(-1), math.Inf(1))
}
func isValidbst(root *TreeNode, min, max float64) bool {
	// 判断当前节点是否符合要求 (root.Val>min && root.Val<max) 并且左右子树均合法
	if root == nil {
		return true
	}
	v := float64(root.Val)
	return v>min && v<max && isValidbst(root.Left, min, v) && isValidbst(root.Right, v, max)
}

/* 0099.Recover-Binary-Search-Tree/
二叉搜索树中的两个节点被错误地交换。请在不改变其结构的情况下，恢复这棵树。
Input: [3,1,4,null,null,2]

  3
 / \
1   4
   /
  2

Output: [2,1,4,null,null,3]

  2
 / \
1   4
   /
  3 */
// 解法 0 迭代
// 核心是用一个指针 prev 记录中序遍历过程中的上一个节点
func recoverTree(root *TreeNode) {
	var prev, target1, target2 *TreeNode
	_, target1, target2 = inOrderTraverse(root, prev, target1, target2)
	if target1!=nil && target2!=nil {
		target1.Val, target2.Val = target2.Val, target1.Val
	}
}
func inOrderTraverse(root, prev, target1, target2 *TreeNode) (*TreeNode, *TreeNode, *TreeNode) {
	if root==nil {
		return prev, target1, target2
	}
	prev, target1, target2 = inOrderTraverse(root.Left, prev, target1, target2)
	if prev!=nil && prev.Val > root.Val {
		// 记录 1或2 个出错的节点
		if target1 == nil{
			target1 = prev
		}
		target2 = root
	}
	prev = root
	prev, target1, target2 = inOrderTraverse(root.Right, prev, target1, target2)
	return prev, target1, target2
}
/* 二叉搜索树等价于一个递增数列, 我们直接看交换数列两个元素之后的情况, [1,2,3,4,5,6,7]
情况一: 交换不相邻的两个元素 2和6, [1,6,3,4,5,2,7], 此时有两个位置不满足 a[i]<a[i+1] 
情况二: 交换相邻元素 2和3, [1,3,2,4,5,6,7], 此时仅有一个位置不满足
如何去包括这两种情况? 遍历过程中, 当第一次出现 a[i]<a[i+1] 情况时, 记录 t1=i; t2=i+1; 当第二次出现时, 仅更新 t2; 并且根据题意知道不会有第三次错误, 所以可直接 break*/
// 解法一 中序遍历转为列表
func recoverTree1(root *TreeNode) {
	// 中序遍历, 分别将val和节点指针保存到两个列表
	valList, nodeList := []int {}, []*TreeNode{}
	var inorder func(root *TreeNode) 	// 定义内部函数
	inorder = func(root *TreeNode){
		if root ==nil{
			return
		}
		inorder(root.Left)
		valList = append(valList, root.Val)
		nodeList = append(nodeList, root)
		inorder(root.Right)
	}
	inorder(root)
	// 找到排序错误的 1或2 个位置
	var t1, t2 *TreeNode
	for i:=0; i<len(valList)-1; i++{
		if valList[i+1] < valList[i]{
			t2 = nodeList[i+1]
			if t1==nil {		// 第一次遇到
				t1 = nodeList[i]
			} else {		// 第二次遇到
				break
			}
		}
	}
	// swap
	if t1!=nil && t2!=nil {
		t1.Val, t2.Val = t2.Val, t1.Val
	}
}
// 解法二 隐式中序 用stack展开递归
// 用了栈来记录当前节点的「右父亲列表」(注意, 对一个节点, 其中序遍历的下一个点是其右子树中最小的节点, 即不断尝试访问左儿子)
func recoverTree2(root *TreeNode) {
	stack := []*TreeNode{}
	var prev, t1, t2 *TreeNode
	for root!=nil || len(stack)>0 {		// 终止条件 当root和stack均为空说明遍历结束
		// (1) 找到prev后下一个次大的节点, 并实现判断逻辑
		// 不断尝试左儿子(找下一个次大的节点)
		for root!=nil {
			stack = append(stack, root)
			root = root.Left
		}
		root = stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if prev != nil && prev.Val > root.Val {
			t2 = root
			if t1==nil {
				t1 = prev
			} else {
				break
			}
		}
		// (2) 中序遍历逻辑, 当前搜索的节点成为 prev, 并在其右子树中寻找下一个节点
		prev = root
		root = root.Right
	}
	t1.Val, t2.Val = t2.Val, t1.Val
}
func f99(){
	recoverTree1(&TreeNode{})
}

/* 0100.Same-Tree/
Given two binary trees, write a function to check if they are the same or not.
判断两个二叉树是否完全相同
深度优先即可(迭代) */
func isSameTree(p *TreeNode, q *TreeNode) bool {
    if p==nil && q==nil {
        return true
    } else if p !=nil && q!=nil {
        if p.Val==q.Val {
            return isSameTree(p.Left, q.Left) && isSameTree(p.Right, q.Right)
        } 
		return false
    } else {
        return false
    }
}

/* 0101.Symmetric-Tree/
Given a binary tree, check whether it is a mirror of itself (ie, symmetric around its center). */
func isSymmetric(root *TreeNode) bool {
	if root == nil {return true}
	return isSymmetricTwo(root.Left, root.Right)
}
func isSymmetricTwo(left, right *TreeNode) bool {
	if left==nil && right==nil {
		return true
	} else if left!=nil && right!=nil {
		// if left.Val==right.Val{
		// 	return isSymmetricTwo(left.Left, right.Right) && isSymmetricTwo(left.Right, right.Left)
		// } else {
		// 	return false
		// }
		return (left.Val == right.Val) && isSymmetricTwo(left.Left, right.Right) && isSymmetricTwo(left.Right, right.Left)
	}else {
		return false
	}
}

/* 0104.Maximum-Depth-of-Binary-Tree/ 
Given a binary tree, find its maximum depth.
The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.
    3
   / \
  9  20
    /  \
   15   7
return 3 */
// 解法一 深度优先
func maxDepth(root *TreeNode) int {
	if root==nil {return 0}
	return max(maxDepth(root.Left), maxDepth(root.Right)) + 1
}
// 解法二 BFS
func maxDepth2(root *TreeNode) int{
	if root== nil {return 0}
	queue := []*TreeNode{}
	queue = append(queue, root)
	ans := 0
	for len(queue)>0{
		tempQueue := []*TreeNode{}
		for _,node := range queue {
			if node.Left != nil {
				tempQueue = append(tempQueue, node.Left)
			}
			if node.Right !=nil {
				tempQueue = append(tempQueue, node.Right)
			}
		}
		queue = tempQueue
		ans++
	}
	return ans
}

/* 0110.Balanced-Binary-Tree/
判断一棵树是不是平衡二叉树。平衡二叉树的定义是：树中每个节点都满足左右两个子树的高度差 <= 1 的这个条件。 */
func isBalanced(root *TreeNode) bool {
	isBalance, _ := isBalancedHight(root)
	return isBalance
}
func isBalancedHight(root *TreeNode) (bool, int) {
	// 返回这棵子树是否平衡, 以及树高
	if root==nil{
		return true, 0
	}
	isBalance1, h1 := isBalancedHight(root.Left)
	isBalance2, h2 := isBalancedHight(root.Right)
	if !isBalance1 || !isBalance2 || abs(h1-h2)>1 {return false, 0}
	return true, max(h1, h2) +1
}

/* 0111.Minimum-Depth-of-Binary-Tree/
给定一个二叉树，找出其最小深度。最小深度是从根节点到最近叶子节点的最短路径上的节点数量。说明: 叶子节点是指没有子节点的节点。
Given a binary tree, find its minimum depth.
The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.
Note: A leaf is a node with no children. */
func minDepth(root *TreeNode) int {
	if root == nil {return 0}
	if root.Left == nil {return minDepth(root.Right)+1}
	if root.Right == nil {return minDepth(root.Left) +1}
	return min(minDepth(root.Left), minDepth(root.Right)) + 1
}

/* 0112.Path-Sum/
给定一个二叉树和一个目标和，判断该树中是否存在根节点到叶子节点的路径，这条路径上所有节点值相加等于目标和。说明: 叶子节点是指没有子节点的节点。
Given a binary tree and a sum, determine if the tree has a root-to-leaf path such that adding up all the values along the path equals the given sum.
      5
     / \
    4   8
   /   / \
  11  13  4
 /  \      \
7    2      1
sum=20
return true, as there exist a root-to-leaf path 5->4->11->2 which sum is 22.*/
func hasPathSum(root *TreeNode, targetSum int) bool {
    if root==nil{return false}
    if root.Left==nil && root.Right==nil {return root.Val==targetSum}
    return hasPathSum(root.Left, targetSum-root.Val) || hasPathSum(root.Right, targetSum-root.Val)
}

/* 0113.Path-Sum-II/
Given a binary tree and a sum, find all root-to-leaf paths where each path’s sum equals the given sum.
      5
     / \
    4   8
   /   / \
  11  13  4
 /  \    / \
7    2  5   1
sum=22
return [
   [5,4,11,2],
   [5,8,4,5]
] */
/* 注意切片传递的方式! 如果用 *paths = append(*paths, tmp[:])
当输入为[-6,null,-3,-6,0,-6,-5,4,null,null,null,1,7]
-21
应该返回 [[-6,-3,-6,-6]], 但实际上返回了 [[-6,-3,-6,-5]]
参见 https://www.cnblogs.com/f-ck-need-u/p/9854932.html#%E4%BC%A0%E9%80%92slice%E7%BB%99%E5%87%BD%E6%95%B0
这是因为, go中的slice本质上还是包括了len, cap 属性的一个指针, 可表示为 [3/5]0xc42003df10, 传递给函数是浅复制  
  - 若函数内部对slice进行扩容，扩容时生成了一个新的底层数组, 两个 slice 的内存指向就不同了, 不会影响外层slice
  - 若没有进行扩容, 修改了底层数组, 则外层同样引用这一底层数组的slice会被改变
这里的tmp找到路径 [-6,-3,-6,-6] 之后, 应该是外层的函数对于该 slice 所指向的内存做了修改 */
// 解法一 传递slice
func pathSum(root *TreeNode, targetSum int) [][]int {
	paths := [][]int{}
	// 传递数组
	// return pathSumRec2(root, targetSum, paths, []int{})
	
	tmpPath := []int{}
	pathSumRec(root, targetSum, &paths, tmpPath)
	return paths
}
// 方式1: paths 为指针, 无输出
func pathSumRec(node *TreeNode, sum int, paths *[][]int, tmp []int){
	if node==nil {return}
	if node.Left==nil && node.Right==nil{
		if sum==node.Val{
			tmp = append(tmp, node.Val)
			// 传递切片的拷贝
			*paths = append(*paths, append([]int{}, tmp...))
			// *paths = append(*paths, tmp)
		}
		return
	}
	// (3) 两个孩子至少一个不为空
	tmp = append(tmp, node.Val)
	pathSumRec(node.Left, sum-node.Val, paths, tmp)
	pathSumRec(node.Right, sum-node.Val, paths, tmp)
}
// 方式2: 返回 [][]int (当然也是指针)
func pathSumRec2(node *TreeNode, sum int, paths [][]int, tmp []int) [][]int{
	if node==nil {return paths}
	if node.Left==nil && node.Right==nil && sum==node.Val{
		tmp = append(tmp, node.Val)
		paths = append(paths, append([]int{}, tmp...))
		return paths
	}
	tmp = append(tmp, node.Val)
	paths = pathSumRec2(node.Left, sum-node.Val, paths, tmp)
	paths = pathSumRec2(node.Right, sum-node.Val, paths, tmp)
	return paths
}

// 解法二 全局变量, 内部函数
func pathSum2(root *TreeNode, targetSum int) [][]int {
	paths := [][]int{}
	tmp := []int{}
	var dfs func(root *TreeNode, target int)
	dfs = func(node *TreeNode, target int){
		if node == nil{return}
		target -= node.Val
		tmp = append(tmp, node.Val)
		defer func(){
			tmp = tmp[:len(tmp)-1]
		}()
		if node.Left==nil && node.Right==nil && target==0{
			paths = append(paths, append([]int{}, tmp...))
		}
		dfs(node.Left, target)
		dfs(node.Right, target)
	}
	dfs(root, targetSum)
	return paths
}

/* 0114.Flatten-Binary-Tree-to-Linked-List/
给定一个二叉树，原地将它展开为链表。展开后的单链表应该与二叉树 先序遍历 顺序相同。
 */
func flatten2(root *TreeNode) {
	if root == nil{return}
	flatten2(root.Right)
	if root.Left==nil{return}
	flatten2(root.Left)
	p := root.Right
	root.Right = root.Left
	root.Left = nil
	for root.Right != nil{
		root = root.Right
	}
	root.Right = p
}

/* 0116.Populating-Next-Right-Pointers-in-Each-Node/
给定一个 完美二叉树 ，其所有叶子节点都在同一层，每个父节点都有两个子节点。
要求在这棵树的同层所有节点之间建立从左到右的next指针连接 */


// =================== Main ===================================
func main(){
	// f209()
}