import time

from order_book import (OrderData, Order, OrderBook)


def build_order(order_data: OrderData) -> Order:
    random_id = int(time.time() * 1e6)
    order = Order(
        random_id,
        order_data.price,
        order_data.volume,
        order_data.side
    )
    return order


def build_order_book(orders_data: list[OrderData]) -> [OrderBook, list[Order]]:
    order_book = OrderBook()
    orders = []
    for order_data in orders_data:
        order = build_order(order_data)
        order_book.execute_order(order)
        orders.append(order)
    return order_book, orders
