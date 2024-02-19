import sys
from typing import TypeVar, Generic, List, Optional

K = TypeVar("K")
V = TypeVar("V")


class TreeNode(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key: K = key
        self.value: V = value

        self.height: int = 1
        self.parent: Optional[TreeNode] = None
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None

    @property
    def balance(self):
        return self.left_height - self.right_height

    @property
    def left_height(self):
        if self.left:
            return self.left.height
        return 0

    @property
    def right_height(self):
        if self.right:
            return self.right.height
        return 0

    @property
    def min_node(self):
        if self.left is None:
            return self
        return self.left.min_node

    @property
    def min_node_value(self):
        if self.min_node is not None:
            return self.min_node.value

    @property
    def next_min_node(self):
        if self.right is not None:
            return self.right
        return self.parent

    @property
    def next_min_node_value(self):
        next_node = self.next_min_node
        if next_node is not None:
            return next_node.value

    @property
    def max_node(self):
        if self.right is None:
            return self
        return self.right.max_node

    @property
    def next_max_node(self):
        if self.left is not None:
            return self.left
        return self.parent

    @property
    def max_node_value(self):
        if self.max_node is not None:
            return self.max_node.value

    @property
    def next_max_node_value(self):
        next_node = self.next_max_node
        if next_node is not None:
            return next_node.value

    @property
    def data(self):
        return self.key, self.value


class AVLTree(Generic[K, V]):
    def __init__(self):
        self.root: Optional[TreeNode[K, V]] = None
        self.min_node: Optional[TreeNode[K, V]] = None

    def insert_node(self, key: K, value: V):
        node = TreeNode(key, value)
        self.root = self._insert_node(self.root, node)

    def delete_node(self, key: K):
        node = TreeNode[K, V](key, None)
        self.root = self._delete_node(self.root, node)

    def find(self, key: K) -> Optional[TreeNode[K, V]]:
        node = TreeNode[K, V](key, None)
        return self._find(self.root, node)

    def find_value(self, key: K) -> Optional[V]:
        node = self.find(key)
        if node is not None:
            return node.value

    def update(self, key: K, value: V):
        node = TreeNode[K, V](key, value)
        self._update(self.root, node)

    def is_empty(self):
        return self.root is None

    def _insert_node(self, root: TreeNode[K, V], node: TreeNode[K, V]):
        if root is None:
            return node
        elif node.key < root.key:
            root.left = self._insert_node(root.left, node)
        else:
            root.right = self._insert_node(root.right, node)

        root.height = 1 + max(root.left_height, root.right_height)

        # Update the balance factor and balance the tree
        balance_factor = root.balance
        if balance_factor > 1:
            if node.key < root.left.key:
                return self._right_rotate(root)
            else:
                root.left = self._left_rotate(root.left)
                return self._right_rotate(root)

        if balance_factor < -1:
            if node.key > root.right.key:
                return self._left_rotate(root)
            else:
                root.right = self._right_rotate(root.right)
                return self._left_rotate(root)

        return root

    # Function to delete a node
    def _delete_node(self, root: TreeNode[K, V], node: TreeNode[K, V]) -> TreeNode[K, V]:
        # Find the node to be deleted and remove it
        if root is None:
            return root
        elif node.key < root.key:
            root.left = self._delete_node(root.left, node)
        elif node.key > root.key:
            root.right = self._delete_node(root.right, node)
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
                return self._right_rotate(root)
            else:
                root.left = self._left_rotate(root.left)
                return self._right_rotate(root)

        if balance_factor < -1:
            if root.right.balance <= 0:
                return self._left_rotate(root)
            else:
                root.right = self._right_rotate(root.right)
                return self._left_rotate(root)

        return root

    # Function to perform left rotation
    def _left_rotate(self, z: TreeNode[K, V]) -> TreeNode[K, V]:
        y = z.right
        t2 = y.left
        y.left = z
        z.right = t2
        z.height = 1 + max(z.left_height, z.right_height)
        y.height = 1 + max(y.left_height, y.right_height)
        return y

    # Function to perform right rotation
    def _right_rotate(self, z: TreeNode[K, V]) -> TreeNode[K, V]:
        y = z.left
        t3 = y.right
        y.right = z
        z.left = t3
        z.height = 1 + max(z.left_height, z.right_height)
        y.height = 1 + max(y.left_height, y.right_height)
        return y

    def _find(self, root: TreeNode[K, V], node: TreeNode[K, V]):
        if root is None:
            return None
        if root.key == node.key:
            return root
        if node.key < root.key and root.left:
            return self._find(root.left, node)
        if root.key < node.key and root.right:
            return self._find(root.right, node)
        return None

    def _update(self, root: TreeNode[K, V], node: TreeNode[K, V]):
        if root.key == node.key:
            root.value = node.value
            return True
        if node.key < root.key and root.left:
            return self._update(root.left, node)
        if root.key < node.key and root.right:
            return self._update(root.right, node)
        return None
