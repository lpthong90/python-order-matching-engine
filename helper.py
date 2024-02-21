import time
from typing import List, Tuple, TypeVar, Optional

from order_book import OrderData, Order, OrderBook, MatchingEngine
from py_simple_trees import AVLTree, AVLNode

K = TypeVar("K")
V = TypeVar("V")


def build_order(order_data: OrderData) -> Order:  # pragma: no cover
    random_id = int(time.time() * 1e6)
    order = Order(
        random_id,
        order_data.price,
        order_data.volume,
        order_data.side
    )
    return order


def build_order_book(orders_data: list[OrderData]) -> [OrderBook, list[Order]]:  # pragma: no cover
    order_book = OrderBook()
    orders = []
    for order_data in orders_data:
        order = build_order(order_data)
        order_book.execute_order(order)
        orders.append(order)
    return order_book, orders


def update_order_book(order_book: OrderBook, orders_data: list[OrderData]) -> [OrderBook, list[Order]]:  # pragma: no cover
    orders = []
    for order_data in orders_data:
        order = build_order(order_data)
        order_book.execute_order(order)
        orders.append(order)
    return order_book, orders


def update_data_to_avl_tree(avl_tree: AVLTree, kv_data: List[Tuple]):  # pragma: no cover
    for action, key, value in kv_data:
        if action == 'insert':
            avl_tree.insert(AVLNode(key, value))
        if action == 'delete':
            avl_tree.remove(AVLNode(key))


def update_matching_engine(matching_engine: MatchingEngine, orders_data: list[OrderData]) -> MatchingEngine:  # pragma: no cover
    orders = []
    for order_data in orders_data:
        order = build_order(order_data)
        matching_engine.execute_order(order)
        orders.append(order)
    return matching_engine, orders


def build_matching_engine(orders_data: list[OrderData], order_book: Optional[OrderBook] = None) -> MatchingEngine:  # pragma: no cover
    matching_engine = MatchingEngine(order_book)
    matching_engine, orders = update_matching_engine(matching_engine, orders_data)
    return matching_engine
