import sys
from typing import TypeVar, List, Tuple, Dict, Optional

from helper import (
    # build_order_book,
    build_matching_engine,
    update_matching_engine,
    # update_order_book,
    update_data_to_avl_tree
)
from order_book import OrderBook, PriceLevel, Order, MatchingEngine
from order_book.avl_tree import AVLTree, TreeNode
from order_book.advanced_avl_tree import AdvancedAVLTree

K = TypeVar("K")
V = TypeVar("V")


def check_order_book(inputs, outputs):
    order_book = TestOrderBook()
    matching_engine = TestMatchingEngine(order_book)
    matching_engine, orders = update_matching_engine(matching_engine, inputs)

    ask_price_levels = list(matching_engine.order_book.get_ask_price_levels())
    print("ask_price_levels: ", ask_price_levels)
    print("expected ask_price_levels: ", outputs[0])
    bid_price_levels = list(matching_engine.order_book.get_bid_price_levels())
    print("bid_price_levels: ", bid_price_levels)
    print("expected bid_price_levels: ", outputs[1])

    assert ask_price_levels == outputs[0]
    assert bid_price_levels == outputs[1]


def check_advanced_avl_tree(inputs, outputs):
    avl_tree = TestAdvancedAVLTree[int, int]()
    update_data_to_avl_tree(avl_tree, inputs)

    parents = avl_tree.get_parents()
    print("parents: ", parents)
    print("expected parents: ", outputs["parents"])

    assert parents == outputs["parents"]


class TestOrderBook(OrderBook):
    def __init__(self):
        super().__init__()
        self.bids_tree: TestAdvancedAVLTree[float, PriceLevel] = TestAdvancedAVLTree[float, PriceLevel]()
        self.asks_tree: TestAdvancedAVLTree[float, PriceLevel] = TestAdvancedAVLTree[float, PriceLevel]()

    def get_ask_price_levels(self):
        price_levels = self.asks_tree.get_all_nodes()
        price_levels.reverse()
        price_levels = map(lambda pl: (pl[1].price, pl[1].total_volume), price_levels)
        return price_levels

    def get_bid_price_levels(self):
        price_levels = self.bids_tree.get_all_nodes()
        price_levels.reverse()
        price_levels = map(lambda pl: (pl[1].price, pl[1].total_volume), price_levels)
        return price_levels

    def print_bids(self): # pragma: no cover
        price_levels = self.get_bid_price_levels()
        for pl in price_levels:
            print("Bid ", pl[0], pl[1])

    def print_asks(self): # pragma: no cover
        price_levels = self.get_ask_price_levels()
        for pl in price_levels:
            print("Ask ", pl[0], pl[1])

    def print_book(self): # pragma: no cover
        print("=====================")
        print("Side | Price | Volume")
        self.print_asks()
        print("-----")
        self.print_bids()


class TestMatchingEngine(MatchingEngine):
    def print_filled_orders(self): # pragma: no cover
        print("======Filled Orders=======")
        print("OrderId | Price | Remained | Volume | Filled")
        for order_id, order in self.filled_orders.items():
            order.print_out()


class TestAdvancedAVLTree(AdvancedAVLTree[K, V]):
    def _parents(self, root: TreeNode) -> List[Tuple]:
        results = []
        if root is None:
            return results
        if root.left is not None:
            results += self._parents(root.left)
        results += [(root.key, root.parent.key if root.parent else None)]
        if root.right is not None:
            results += self._parents(root.right)

        return results

    def get_parents(self):
        return self._parents(self.root)

    def print_parents(self): # pragma: no cover
        results = self.get_parents()
        print("Key | ParentKey")
        print(results)

    # Print the tree
    def _print_helper(self, root: TreeNode[K, V], indent: str, last: bool): # pragma: no cover
        if root is not None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(root.key)
            self._print_helper(root.left, indent, False)
            self._print_helper(root.right, indent, True)

    def print_helper(self, indent: str, last: bool): # pragma: no cover
        self._print_helper(self.root, indent, last)

    def _get_all_nodes(self, node: TreeNode[K, V]) -> List[tuple[K, V]]:
        results = []
        if not node:
            return results

        if node.left:
            results += self._get_all_nodes(node.left)
        results += [node.data]
        if node.right:
            results += self._get_all_nodes(node.right)
        return results

    def get_all_nodes(self) -> List[tuple[K, V]]:
        return self._get_all_nodes(self.root)