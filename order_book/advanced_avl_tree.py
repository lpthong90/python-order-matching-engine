from typing import Optional, List, Tuple, TypeVar

from order_book.avl_tree import (TreeNode, AVLTree)

K = TypeVar("K")
V = TypeVar("V")


class AdvancedAVLTree(AVLTree[K, V]):
    def __init__(self):
        super().__init__()
        self.min_node: Optional[TreeNode[K, V]] = None
        self.max_node: Optional[TreeNode[K, V]] = None

    def insert_node(self, key: K, value: V):
        node = TreeNode(key, value)
        if self.min_node is None or self.min_node.key > node.key:
            self.min_node = node
        if self.max_node is None or self.max_node.key < node.key:
            self.max_node = node
        self.root = self._insert_node(self.root, node)

    def delete_node(self, key: K):
        node = TreeNode[K, V](key, None)
        if self.min_node is not None and self.min_node.key == node:
            self.min_node = self._get_next_min_node()
        if self.max_node is not None and self.max_node.key == node:
            self.max_node = self._get_next_max_node()
        self.root = self._delete_node(self.root, node)

    @property
    def min_node_value(self):
        if self.root is None:
            return
        if self.root.min_node is None:
            return
        return self.root.min_node.value

    @property
    def max_node_value(self):
        if self.root is None:
            return
        if self.root.max_node is None:
            return
        return self.root.max_node.value

    def _get_next_min_node(self):
        if self.min_node is None:
            return None
        if self.min_node.right is not None:
            return self.min_node.right
        return self.min_node.parent

    def _get_next_max_node(self):
        if self.max_node is None:
            return None
        if self.max_node.left is not None:
            return self.max_node.left
        return self.max_node.parent

    def _insert_node(self, root: TreeNode, node: TreeNode):
        if root is None:
            return node
        elif node.key < root.key:
            root.left = self._insert_node(root.left, node)
            root.left.parent = root
        else:
            root.right = self._insert_node(root.right, node)
            root.right.parent = root

        root.height = 1 + max(root.left_height, root.right_height)

        # Update the balance factor and balance the tree
        balance_factor = root.balance
        if balance_factor > 1:
            if node.key < root.left.key:
                return self._right_rotate(root, root.parent)
            else:
                root.left = self._left_rotate(root.left, root.parent)
                return self._right_rotate(root, root.parent)

        if balance_factor < -1:
            if node.key > root.right.key:
                return self._left_rotate(root, root.parent)
            else:
                root.right = self._right_rotate(root.right, root.parent)
                return self._left_rotate(root, root.parent)

        return root

    def _delete_node(self, root: TreeNode, node: TreeNode) -> TreeNode:
        # Find the node to be deleted and remove it
        if root is None:
            return root
        elif node.key < root.key:
            root.left = self._delete_node(root.left, node)
            if root.left is not None:
                root.left.parent = root
        elif node.key > root.key:
            root.right = self._delete_node(root.right, node)
            if root.right is not None:
                root.right.parent = root
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = root.right.min_node
            root.key = temp.key
            root.value = temp.value
            root.right = self._delete_node(root.right, temp)

        if root is None:
            return root

        # Update the balance factor of nodes
        root.height = 1 + max(root.left_height, root.right_height)
        balance_factor = root.balance

        # Balance the tree
        if balance_factor > 1:
            if root.left.balance >= 0:
                return self._right_rotate(root, root.parent)
            else:
                root.left = self._left_rotate(root.left, root.parent)
                return self._right_rotate(root, root.parent)

        if balance_factor < -1:
            if root.right.balance <= 0:
                return self._left_rotate(root, root.parent)
            else:
                root.right = self._right_rotate(root.right, root.parent)
                return self._left_rotate(root, root.parent)

        return root

    def _left_rotate(self, z: TreeNode[K, V], parent: TreeNode[K, V]) -> TreeNode[K, V]:
        y = z.right
        b = y.left
        y.left = z
        y.parent = parent
        if z is not None:
            z.parent = y
        z.right = b
        if b is not None:
            b.parent = z
        z.height = 1 + max(z.left_height, z.right_height)
        y.height = 1 + max(y.left_height, y.right_height)
        return y

    # Function to perform right rotation
    def _right_rotate(self, z: TreeNode[K, V], parent: TreeNode[K, V]) -> TreeNode[K, V]:
        y = z.left
        b = y.right
        y.right = z
        y.parent = parent
        if z is not None:
            z.parent = y
        z.left = b
        if b is not None:
            b.parent = z
        z.height = 1 + max(z.left_height, z.right_height)
        y.height = 1 + max(y.left_height, y.right_height)
        return y
