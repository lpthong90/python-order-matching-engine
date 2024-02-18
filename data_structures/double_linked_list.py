from typing import Union, TypeVar, Generic

T = TypeVar("T")


class LinkedNode(Generic[T]):
    def __init__(self, key):
        self.key: T = key
        self.next: Union[LinkedNode, None] = None
        self.prev: Union[LinkedNode, None] = None


class LinkedList:
    def __init__(self):
        self.size = 0
        self.head: Union[LinkedNode, None] = None
        self.tail: Union[LinkedNode, None] = None

    def _add_first_node(self, node: LinkedNode) -> bool:
        self.head = self.tail = node
        self.size += 1
        return True

    def add_head(self, node: LinkedNode) -> bool:
        if self.head is None:
            return self._add_first_node(node)

        node.next = self.head
        self.head.prev = node
        self.head = node
        self.size += 1
        return True

    def add_tail(self, node: LinkedNode) -> bool:
        if self.tail is None:
            return self._add_first_node(node)

        node.prev = self.tail
        self.tail.next = node
        self.tail = node
        self.size += 1
        return True

    def add(self, node: LinkedNode) -> bool:
        return self.add_tail(node)

    def pop(self) -> LinkedNode:
        if self.size == 0:
            return None

        node = self.head
        self.head = node.next
        self.size -= 1

        if self.head is not None:
            self.head.prev = None

        if self.size == 0:
            self.tail = None

        return node

    def remove(self, node: LinkedNode) -> bool:
        if self.size == 0:
            return False

        if self.size == 1:
            self.head = self.tail = None
            self.size -= 1
            return True

        if self.head is node:
            self.head = node.next
            self.head.prev = None
            self.size -= 1
            return True

        if self.tail is node:
            self.tail = node.prev
            self.tail.next = None
            self.size -= 1
            return True

        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        return True

    def get_all_values(self):
        result = []
        if self.head is None:
            return result

        current_node = self.head
        while current_node.next is not None:
            result.append(current_node.key)
            current_node = current_node.next

        result.append(current_node.key)
        return result


# ll = LinkedList()
#
# node_map = {}
# for i in [1, 2, 3, 4, 5]:
#     node_map[i] = LinkedNode(i)
#     ll.add(node_map[i])
#
# print("Size: ", ll.size)
#
# print(ll.get_all_values())
# ll.remove(node_map[3])
# print(ll.get_all_values())


# print(ll.pop().key)
# ll.add_head(LinkedNode(6))
# print(ll.pop().key)
# ll.add_head(LinkedNode(7))
# print(ll.pop().key)
# ll.add_head(LinkedNode(8))
# print(ll.pop().key)
# ll.add_head(LinkedNode(9))
# print(ll.pop().key)
# ll.add_head(LinkedNode(10))
# print(ll.pop().key)
# print(ll.pop().key)
# print(ll.pop().key)
# print(ll.pop().key)
# print(ll.pop().key)
