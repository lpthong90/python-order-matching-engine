import sys
from typing import Union, TypeVar, Generic, List

T = TypeVar("T")


class TreeNode(Generic[T]):
    def __init__(self, key: T):
        self.key: T = key

        self.height: int = 1
        self.left: Union[TreeNode, None] = None
        self.right: Union[TreeNode, None] = None

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
        return self._get_min_node()

    @property
    def max_node(self):
        return self._get_max_node()

    def _get_min_node(self):
        if self.left is None:
            return self
        return self._get_min_node(self.left)

    def _get_max_node(self):
        if self.right is None:
            return self
        return self._get_max_node(self.right)


class AVLTree:
    def __init__(self):
        self.root: TreeNode = None

    def _insert_node(self, root: TreeNode, node: TreeNode):
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

    def insert_node(self, node: TreeNode):
        self.root = self._insert_node(self.root, node)

    # Function to delete a node
    def _delete_node(self, root: TreeNode, node: TreeNode):
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

    def delete_node(self, node: TreeNode):
        self.root = self._delete_node(self.root, node)

    # Function to perform left rotation
    def _left_rotate(self, z):
        y = z.right
        t2 = y.left
        y.left = z
        z.right = t2
        z.height = 1 + max(z.left_height, z.right_height)
        y.height = 1 + max(y.left_height, y.right_height)
        return y

    # Function to perform right rotation
    def _right_rotate(self, z):
        y = z.left
        t3 = y.right
        y.right = z
        z.left = t3
        z.height = 1 + max(z.left_height, z.right_height)
        y.height = 1 + max(y.left_height, y.right_height)
        return y

    def _pre_order(self, root):
        if not root:
            return
        print("{0} ".format(root.key), end="")
        self._pre_order(root.left)
        self._pre_order(root.right)

    def find(self, node: TreeNode) -> Union[TreeNode, None]:
        pass

    # Print the tree
    def _print_helper(self, curr_ptr, indent, last):
        if curr_ptr is not None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(curr_ptr.key)
            self._print_helper(curr_ptr.left, indent, False)
            self._print_helper(curr_ptr.right, indent, True)

    def print_helper(self, indent, last):
        self._print_helper(self.root, indent, last)

    def _get_all_nodes(self, node: TreeNode) -> List[TreeNode]:
        results = []
        if not node:
            return results

        if node.left:
            results += self._get_all_nodes(node.left)
        results += [node]
        if node.right:
            results += self._get_all_nodes(node.right)
        return results

    def get_all_nodes(self) -> List[TreeNode]:
        return self._get_all_nodes(self.root)

    @property
    def min_node(self):
        if not self.root:
            return None
        return self.root.min_node

    @property
    def max_node(self):
        if not self.root:
            return None
        return self.root.max_node

# myTree = AVLTree()
# root = None
# nums = [33, 13, 52, 9, 21, 61, 8, 11]
# nodes_map = {}
# for num in nums:
#     nodes_map[num] = TreeNode(num)
#     print("Insert ", num)
#     myTree.insert_node(nodes_map[num])
#     # root = myTree.insert_node(root, num)
#
# myTree.print_helper("", True)
# key = 52 # 13
# myTree.delete_node(nodes_map[key])
# print("After Deletion: ")
# myTree.print_helper("", True)