from typing import Union, TypeVar, Generic, List

K = TypeVar("K")
V = TypeVar("V")


class LinkedNode(Generic[K, V]):
    def __init__(self, key: K, value: Union[V, None]):
        self.key: K = key
        self.value: Union[V, None] = value
        self.next: Union[LinkedNode, None] = None
        self.prev: Union[LinkedNode, None] = None


class LinkedList(Generic[K, V]):
    def __init__(self):
        self.size = 0
        self.head: Union[LinkedNode, None] = None
        self.tail: Union[LinkedNode, None] = None

    def _add_first_node(self, node: LinkedNode) -> bool:
        self.head = self.tail = node
        self.size += 1
        return True

    def _add_head(self, node: LinkedNode):
        node.next = self.head
        self.head.prev = node
        self.head = node
        self.size += 1
        return True

    def _add_tail(self, node: LinkedNode):
        node.prev = self.tail
        self.tail.next = node
        self.tail = node
        self.size += 1
        return True

    def add_head(self, key: K, value: V) -> bool:
        node = LinkedNode(key, value)

        if self.head is None:
            return self._add_first_node(node)

        return self._add_head(node)

    def add_tail(self, key: K, value: V) -> bool:
        node = LinkedNode(key, value)

        if self.tail is None:
            return self._add_first_node(node)

        return self._add_tail(node)

    def add(self, key: K, value: V) -> bool:
        return self.add_tail(key, value)

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

    def remove(self, key: K) -> bool:
        # node = LinkedNode(key, None)
        node = self.find(key)

        if node is None:
            return

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

    def get_all_values(self) -> List[V]:
        result = []
        if self.head is None:
            return result

        current_node = self.head
        while current_node.next is not None:
            result.append(current_node.value)
            current_node = current_node.next

        result.append(current_node.value)
        return result

    def find(self, key: K) -> Union[LinkedNode, None]:
        if self.size == 0:
            return None

        current_node = self.head
        while current_node is not None:
            if current_node.key == key:
                return current_node
            current_node = current_node.next

        return None


# ll = LinkedList()
# for i in [1, 2, 3, 4, 5]:
#     ll.add(i, i)
#
# print("Size: ", ll.size)
#
# print(ll.get_all_values())
# ll.remove(11)
# print(ll.get_all_values())
#
#
# print(ll.pop().key)
# ll.add_head(6, 6)
# print(ll.pop().key)
# ll.add_head(7, 7)
# print(ll.pop().key)
# ll.add_head(8, 8)
# print(ll.pop().key)
# ll.add_head(9, 9)
# print(ll.pop().key)
# ll.add_head(10, 10)
# print(ll.pop().key)
# print(ll.pop().key)
# print(ll.pop().key)
# print(ll.pop().key)
# print(ll.size)
