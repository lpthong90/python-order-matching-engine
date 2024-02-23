from typing import TypeVar, List, Tuple

from helper import update_matching_engine
from order_book import OrderBook, MatchingEngine, PriceLevelAVLTree
from py_simple_trees import AVLNode, TraversalType

K = TypeVar("K")
V = TypeVar("V")
AVLBN = TypeVar("AVLBN", bound=AVLNode)


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


class TestOrderBook(OrderBook):
    def __init__(self):
        super().__init__()
        self.bids_tree: TestAVLTree = TestAVLTree()
        self.asks_tree: TestAVLTree = TestAVLTree()

    def get_ask_price_levels(self):
        return map(
            lambda node: (node.value.price, node.value.total_quantity),
            self.asks_tree.traversal(
                traversal_type=TraversalType.IN_ORDER, reverse=True
            ),
        )

    def get_bid_price_levels(self):
        return map(
            lambda node: (node.value.price, node.value.total_quantity),
            self.bids_tree.traversal(
                traversal_type=TraversalType.IN_ORDER, reverse=True
            ),
        )

    def print_bids(self):  # pragma: no cover
        price_levels = self.get_bid_price_levels()
        for pl in price_levels:
            print("Bid ", pl[0], pl[1])

    def print_asks(self):  # pragma: no cover
        price_levels = self.get_ask_price_levels()
        for pl in price_levels:
            print("Ask ", pl[0], pl[1])

    def print_book(self):  # pragma: no cover
        print("=====================")
        print("Side | Price | Volume")
        self.print_asks()
        print("-----")
        self.print_bids()


class TestMatchingEngine(MatchingEngine):
    def print_filled_orders(self):  # pragma: no cover
        print("======Filled Orders=======")
        print("OrderId | Price | Remained | Volume | Filled")
        for order_id, order in self.filled_orders.items():
            order.print_out()


class TestAVLTree(PriceLevelAVLTree):
    def _parents(self, root: AVLNode) -> List[Tuple]:
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

    def print_parents(self):  # pragma: no cover
        results = self.get_parents()
        print("Key | ParentKey")
        print(results)
